import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import os

CSV = "contributors_map.csv"
MAP_IMG = "contributors_map.png"

def main():
    if not os.path.exists(CSV):
        print("No contributors_map.csv found.")
        return

    df = pd.read_csv(CSV)
    if df.empty or "lat" not in df.columns or "lon" not in df.columns:
        print("No valid lat/lon data.")
        return

    lats = pd.to_numeric(df["lat"], errors="coerce")
    lons = pd.to_numeric(df["lon"], errors="coerce")
    names = df["login"].fillna("").values

    fig = plt.figure(figsize=(12, 6))
    m = Basemap(projection='robin', lon_0=0, resolution='c')
    m.drawcoastlines()
    m.drawcountries()
    m.fillcontinents(color='lightgray', lake_color='lightblue')
    m.drawmapboundary(fill_color='lightblue')

    # Plot contributor pins
    for lat, lon, name in zip(lats, lons, names):
        if pd.notna(lat) and pd.notna(lon):
            x, y = m(lon, lat)
            m.plot(x, y, 'ro', markersize=7)
            plt.text(x, y, name, fontsize=8, ha='left', va='bottom', color='black', alpha=0.7)

    plt.title("LUFT Contributors Around the World")
    plt.tight_layout()
    plt.savefig(MAP_IMG, bbox_inches='tight', dpi=170)
    print(f"Saved {MAP_IMG}")

if __name__ == "__main__":
    main()
