import os
import requests
import csv
import re

README = "README.md"
MAP_CSV = "contributors_map.csv"
REPO = os.getenv("GITHUB_REPOSITORY", "owner/repo")
TOKEN = os.getenv("GITHUB_TOKEN")

def fetch_contributors():
    url = f"https://api.github.com/repos/{REPO}/contributors"
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    contributors = []
    page = 1
    while True:
        resp = requests.get(url, headers=headers, params={"per_page": 100, "page": page})
        if resp.status_code != 200:
            break
        data = resp.json()
        if not data:
            break
        contributors.extend(data)
        page += 1
    return contributors

def fetch_user_location(username):
    url = f"https://api.github.com/users/{username}"
    headers = {"Authorization": f"token {TOKEN}"} if TOKEN else {}
    resp = requests.get(url, headers=headers)
    if resp.status_code != 200:
        return None
    return resp.json().get("location")

def geocode_location(location):
    if not location:
        return None, None
    try:
        geo_resp = requests.get("https://nominatim.openstreetmap.org/search",
                                params={"q": location, "format": "json", "limit": 1},
                                headers={"User-Agent": "LUFT-Contributor-Map"})
        if geo_resp.status_code == 200 and geo_resp.json():
            lat = geo_resp.json()[0]["lat"]
            lon = geo_resp.json()[0]["lon"]
            return lat, lon
    except Exception:
        pass
    return None, None

def update_readme_table(rows):
    try:
        with open(README, "r", encoding="utf-8") as f:
            readme = f.read()
    except FileNotFoundError:
        readme = ""

    table_md = "| Contributor | Location | Latitude | Longitude |\n|-------------|----------|----------|-----------|\n"
    for r in rows:
        table_md += f"| {r['login']} | {r['location'] or ''} | {r['lat'] or ''} | {r['lon'] or ''} |\n"

    marker = "LUFT_CONTRIBUTOR_MAP"
    if marker in readme:
        pattern = re.compile(rf"(<!-- {marker} START -->).*?(<!-- {marker} END -->)", re.DOTALL)
        readme = pattern.sub(rf"\1\n{table_md}\n\2", readme)
    else:
        readme += f"\n<!-- {marker} START -->\n{table_md}\n<!-- {marker} END -->\n"

    with open(README, "w", encoding="utf-8") as f:
        f.write(readme)

def main():
    contributors = fetch_contributors()
    rows = []
    for c in contributors:
        login = c["login"]
        location = fetch_user_location(login)
        lat, lon = geocode_location(location)
        rows.append({"login": login, "location": location, "lat": lat, "lon": lon})

    # Save CSV
    with open(MAP_CSV, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=["login", "location", "lat", "lon"])
        writer.writeheader()
        writer.writerows(rows)

    # Update README
    update_readme_table(rows)

if __name__ == "__main__":
    main()
