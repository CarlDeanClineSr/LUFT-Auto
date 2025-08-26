# LUFT Image Gallery

This gallery showcases conceptual and AI-generated visuals inspired by LUFT: unification across energy, matter, space, and time, and coherence analysis (e.g., dimuon/quarkonia).

How to generate images
- Install deps: pip install -r requirements-optional.txt
- Generate (OpenAI default): python tools/generate_luft_images.py --prompts graphics/prompts.yaml --outdir graphics/generated
- Alternative backends:
  - Stability API: python tools/generate_luft_images.py --backend stability --prompts graphics/prompts.yaml --outdir graphics/generated
  - Local (diffusers/SDXL): python tools/generate_luft_images.py --backend diffusers --prompts graphics/prompts.yaml --outdir graphics/generated
- The images referenced below will be created in graphics/generated/.

Gallery

## Field Lines and Coherence

![LUFT Field Lines](generated/luft_field_lines.png)
Caption: Emergent field lines and resonance nodes across a lattice—coherence regime sweep.

![Coherence Spectrum](generated/luft_coherence_spectrum.png)
Caption: Frequency-coincidence spectrum mapped to spatial harmonics.

## Dimuon / Quarkonia

![Dimuon Coherence Map](generated/luft_dimuon_map.png)
Caption: Conceptual dimuon/quarkonia coherence mapping with feature-flagged resolution bands.

## Lattice, Geometry, and Time

![Lattice Resonance](generated/luft_lattice_resonance.png)
Caption: Lattice geometry with quantized resonance shells and temporal phasing.

![Space-Time Manifold](generated/luft_spacetime_manifold.png)
Caption: Manifold visualization of space-time curvature under energy flow.

## Helio and Cosmic Context

![HelioSync Streams](generated/luft_heliosync_streams.png)
Caption: HelioSync-inspired data streams, solar wind interfaces, and monitoring overlays.

![Cosmic Background](generated/luft_cmb_overlay.png)
Caption: CMB-style background with overlayed LUFT resonance fingerprints.

Notes
- These images are conceptual, for communication and ideation. They are not empirical outputs.
- Re-generate with different seeds in graphics/prompts.yaml to explore variations.
