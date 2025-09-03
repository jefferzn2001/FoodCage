from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "usd_assets"
print("Project root:", ROOT)
print("Assets:", list(ASSETS.rglob("*"))[:10])  # peek first few

# TODOs:
# - Load scenes/cage_composed.usda
# - Sample a grid and save NPZ with (x, y) targets
# - Add a --headless flag and simple CLI


