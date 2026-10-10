"""Build bilingual hints separately from the initially visible puzzle catalog."""
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
source=json.loads((ROOT/'tmp/hints-extracted.json').read_text())
rows=[]
for part, first, last in [('first',1,105),('middle',106,210),('last',211,313)]:
    translated=[line.split('|') for line in (ROOT/f'content/hints-{part}.tsv').read_text().splitlines()]
    assert all(len(row)==2 and row[1].strip() for row in translated)
    assert [int(row[0]) for row in translated]==list(range(first,last+1))
    rows.extend(translated)
fixes={
    17:[('playes','players')],40:[('each persons','each person’s')],
    65:[('incribe','inscribe')],141:[('2n × 2n','2ⁿ × 2ⁿ')],
    158:[('high-numered','high-numbered')],301:[('for this puzzles','for this puzzle')],
    159:[('triangulate the sphere', 'triangulate the faces of the polyhedron')],
    184:[('representive','representative')],191:[('being to small','being too small')],
    224:[('xk','x^k')],228:[('x2','x²')],313:[('45◦and','45° and')],
}
assert [p['id'] for p in source]==list(range(1,314))
public=[]; provenance=[]
for p,row in zip(source,rows,strict=True):
    assert p['id']==int(row[0])
    english=p['hint_en']
    for old,new in fixes.get(p['id'],[]): english=english.replace(old,new)
    assert english.strip() and not any(ord(c)<32 for c in english+row[1])
    public.append({'id':p['id'],'hint_en':english,'hint_he':row[1]})
    provenance.append({'id':p['id'],'source':p['source']})
(ROOT/'src/puzzlebook/data/hints.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n')
(ROOT/'content/hint-sources.json').write_text(json.dumps(provenance,indent=2)+'\n')
print('Built',len(public),'bilingual hints')
