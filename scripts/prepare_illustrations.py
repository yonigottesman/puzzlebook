"""Encode approved PNG artwork for web delivery and build its public URL manifest.

Run: uv run --with pillow python scripts/prepare_illustrations.py
"""
import argparse
import json
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
BUCKET = 'puzzlebook-images-941271455567'
catalog = json.loads((ROOT / 'src/puzzlebook/data/puzzles.json').read_text())
parser = argparse.ArgumentParser()
parser.add_argument('--partial', action='store_true', help='Publish completed artwork while generation continues')
args = parser.parse_args()
selected = catalog
output = ROOT / 'output/illustrations'
output.mkdir(parents=True, exist_ok=True)
manifest = []
for puzzle in selected:
    ident = puzzle['id']
    sources = sorted((ROOT / 'docs/illustration-samples').glob(f'puzzle-{ident:03}-v*.png'),
                     key=lambda path: int(path.stem.rsplit('-v', 1)[1]))
    if not sources:
        if args.partial:
            continue
        raise FileNotFoundError(f'Missing illustration for puzzle {ident}')
    source = sources[-1]
    name = f'{source.stem}.webp'
    destination = output / name
    if not destination.exists() or source.stat().st_mtime > destination.stat().st_mtime:
        with Image.open(source) as image:
            if image.mode == 'RGBA':
                background = Image.new('RGBA', image.size, '#fffdf5')
                image = Image.alpha_composite(background, image)
            image = image.convert('RGB')
            image.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
            image.save(destination, 'WEBP', quality=88, method=6)
    with Image.open(destination) as image:
        manifest.append(dict(id=ident, url=f'https://storage.googleapis.com/{BUCKET}/{name}',
                             width=image.width, height=image.height))
(ROOT / 'src/puzzlebook/data/illustrations.json').write_text(
    json.dumps(manifest, ensure_ascii=False, indent=2) + '\n'
)
welcome = ROOT / 'docs/illustration-samples/welcome-family-v2.png'
welcome_output = output / 'welcome-family-v2.webp'
if welcome.exists() and (not welcome_output.exists() or welcome.stat().st_mtime > welcome_output.stat().st_mtime):
    with Image.open(welcome) as image:
        image = image.convert('RGB')
        image.thumbnail((1200, 1200), Image.Resampling.LANCZOS)
        image.save(welcome_output, 'WEBP', quality=88, method=6)
print(f'Prepared {len(manifest)} illustrations; {sum(p.stat().st_size for p in output.glob("*.webp")):,} bytes')
