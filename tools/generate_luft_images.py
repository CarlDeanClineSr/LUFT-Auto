import argparse
import os
import sys
import time
import yaml
from dataclasses import dataclass
from typing import Dict, Any, List, Optional

# Optional backends
# - diffusers (local SDXL): pip install torch diffusers transformers accelerate safetensors
# - stability.ai (API):     pip install requests
# - openai images (API):    pip install openai

def ensure_dir(p):
    os.makedirs(p, exist_ok=True)

def slugify(s: str) -> str:
    return "".join(c if c.isalnum() or c in "-_." else "_" for c in s)

@dataclass
class GenItem:
    name: str
    prompt: str
    negative_prompt: Optional[str] = None
    seed: Optional[int] = None
    steps: Optional[int] = None
    guidance_scale: Optional[float] = None
    width: Optional[int] = None
    height: Optional[int] = None

def load_prompts(path: str) -> (Dict[str, Any], List[GenItem]):
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    defaults = data.get("defaults", {})
    items = []
    for it in data.get("items", []):
        items.append(GenItem(
            name=it["name"],
            prompt=it["prompt"],
            negative_prompt=it.get("negative_prompt", defaults.get("negative_prompt")),
            seed=it.get("seed"),
            steps=it.get("steps", defaults.get("steps")),
            guidance_scale=it.get("guidance_scale", defaults.get("guidance_scale")),
            width=it.get("width", defaults.get("width")),
            height=it.get("height", defaults.get("height")),
        ))
    return defaults, items

def gen_diffusers(args, items: List[GenItem]):
    try:
        import torch
        from diffusers import StableDiffusionXLImg2ImgPipeline, StableDiffusionXLPipeline
    except Exception as e:
        print("Please install diffusers backend: pip install torch diffusers transformers accelerate safetensors", file=sys.stderr)
        raise

    model_id = args.model or "stabilityai/stable-diffusion-xl-base-1.0"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    dtype = torch.float16 if torch.cuda.is_available() else torch.float32
    pipe = StableDiffusionXLPipeline.from_pretrained(model_id, torch_dtype=dtype)
    if device == "cuda":
        pipe = pipe.to(device)

    for it in items:
        out_name = slugify(it.name) + ".png"
        out_path = os.path.join(args.outdir, out_name)
        print(f"[diffusers] Generating {out_name} ...")
        g = None
        if it.seed is not None:
            g = torch.Generator(device=device).manual_seed(int(it.seed))
        image = pipe(
            prompt=it.prompt,
            negative_prompt=it.negative_prompt,
            num_inference_steps=int(it.steps or 30),
            guidance_scale=float(it.guidance_scale or 7.0),
            width=int(it.width or 1280),
            height=int(it.height or 720),
            generator=g
        ).images[0]
        image.save(out_path)
        print(f" -> saved {out_path}")

def gen_stability_api(args, items: List[GenItem]):
    import base64
    import requests
    key = os.environ.get("STABILITY_API_KEY")
    if not key:
        raise RuntimeError("Missing STABILITY_API_KEY environment variable.")
    engine = args.model or "stable-diffusion-xl-1024-v1-0"
    url = f"https://api.stability.ai/v1/generation/{engine}/text-to-image"
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    for it in items:
        payload = {
            "text_prompts": [
                {"text": it.prompt, "weight": 1},
                {"text": it.negative_prompt or "", "weight": -1},
            ],
            "cfg_scale": float(it.guidance_scale or 7.0),
            "height": int(it.height or 720),
            "width": int(it.width or 1280),
            "samples": 1,
            "steps": int(it.steps or 30),
            **({"seed": int(it.seed)} if it.seed is not None else {}),
        }
        print(f"[stability] Generating {it.name} ...")
        r = requests.post(url, headers=headers, json=payload, timeout=120)
        r.raise_for_status()
        data = r.json()
        out_name = slugify(it.name) + ".png"
        out_path = os.path.join(args.outdir, out_name)
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(data["artifacts"][0]["base64"]))
        print(f" -> saved {out_path}")

def gen_openai(args, items: List[GenItem]):
    try:
        from openai import OpenAI
    except Exception:
        raise RuntimeError("Please install openai: pip install openai")
    client = OpenAI()
    for it in items:
        print(f"[openai] Generating {it.name} ...")
        resp = client.images.generate(
            model=args.model or "gpt-image-1",
            prompt=it.prompt,
            size=f"{int(it.width or 1280)}x{int(it.height or 720)}",
            n=1
        )
        import base64
        b64 = resp.data[0].b64_json
        out_name = slugify(it.name) + ".png"
        out_path = os.path.join(args.outdir, out_name)
        with open(out_path, "wb") as f:
            f.write(base64.b64decode(b64))
        print(f" -> saved {out_path}")

def main():
    ap = argparse.ArgumentParser(description="Generate LUFT images from prompts.")
    ap.add_argument("--backend", choices=["diffusers", "stability", "openai"], default="diffusers")
    ap.add_argument("--prompts", default="graphics/prompts.yaml")
    ap.add_argument("--outdir", default="graphics/generated")
    ap.add_argument("--model", default=None, help="Model id or engine (optional)")
    args = ap.parse_args()

    ensure_dir(args.outdir)
    defaults, items = load_prompts(args.prompts)

    if args.backend == "diffusers":
        gen_diffusers(args, items)
    elif args.backend == "stability":
        gen_stability_api(args, items)
    elif args.backend == "openai":
        gen_openai(args, items)
    else:
        raise ValueError("Unknown backend")

    print("All done. Open graphics/gallery.md to view references.")

if __name__ == "__main__":
    main()
