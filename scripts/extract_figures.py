"""Extract only the three diagrams appearing in puzzle statements."""
from pathlib import Path
import pymupdf
root = Path(__file__).resolve().parents[1]
book = pymupdf.open(root / 'book.pdf')
target = root / 'src/puzzlebook/static/figures'
target.mkdir(parents=True, exist_ok=True)
for ident, page in {140:33, 154:37, 221:50}.items():
    image = next(b for b in book[page-1].get_text('dict')['blocks'] if b['type']==1)
    book[page-1].get_pixmap(matrix=pymupdf.Matrix(4,4), clip=pymupdf.Rect(image['bbox'])).save(target / f'{ident}.png')
