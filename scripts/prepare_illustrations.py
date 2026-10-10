"""Encode approved PNG artwork for web delivery and build its public URL manifest.

Run: uv run --with pillow python scripts/prepare_illustrations.py
"""
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BUCKET = 'puzzlebook-images-941271455567'
catalog = json.loads((ROOT / 'src/puzzlebook/data/puzzles.json').read_text())
selected = [p for p in catalog if p['level'] == 'easy'][:20]
output = ROOT / 'output/illustrations'
output.mkdir(parents=True, exist_ok=True)
manifest = []
for puzzle in selected:
    ident = puzzle['id']
    source = ROOT / f'docs/illustration-samples/puzzle-{ident:03}-v1.png'
    with Image.open(source) as image:
        image = image.convert('RGB')
        image.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
        name = f'puzzle-{ident:03}-v1.webp'
        image.save(output / name, 'WEBP', quality=88, method=6)
        manifest.append(dict(id=ident, url=f'https://storage.googleapis.com/{BUCKET}/{name}',
                             width=image.width, height=image.height))
(ROOT / 'src/puzzlebook/data/illustrations.json').write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
)
print(f'Prepared {len(manifest)} illustrations; {sum(p.stat().st_size for p in output.glob("*.webp")):,} bytes')
