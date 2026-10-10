"""Package extracted official solutions for server-only clarification context."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
source = json.loads((ROOT / 'tmp/extracted.json').read_text())
solutions = []
for puzzle in source:
    _, separator, answer = puzzle['solution'].partition('Solution:')
    if not separator or not answer.strip():
        raise ValueError(f'Missing official solution for {puzzle["id"]}')
    solutions.append({'id': puzzle['id'], 'solution': answer.strip()})
if [s['id'] for s in solutions] != list(range(1, 314)):
    raise ValueError('Expected all 313 official solutions')
(ROOT / 'src/puzzlebook/data/solutions.json').write_text(
    json.dumps(solutions, ensure_ascii=False, indent=2) + '\n'
)
