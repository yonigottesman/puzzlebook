"""Extract the book's alphabetical hints, keeping solutions separate."""
from pathlib import Path
import json
import re
import pymupdf

ROOT = Path(__file__).resolve().parents[1]
book = pymupdf.open(ROOT / 'book.pdf')
entries = []
current = None

def join(lines):
    out = ''
    for line in lines:
        if out.endswith('-'):
            out = out[:-1] + line
        else:
            out += (' ' if out else '') + line
    return out.strip()

for page_number in range(71,85):
    for block in book[page_number-1].get_text('dict')['blocks']:
        if block['type'] != 0: continue
        for line in block['lines']:
            if line['bbox'][1] > 680: continue
            spans = line['spans']
            first = next((s for s in spans if s['text'].strip()), None)
            if not first: continue
            if first['font'] == 'CMBX10':
                bold = []; body = []; in_title = True
                for span in spans:
                    if span['font'] != 'CMBX10': in_title = False
                    (bold if in_title else body).append(span['text'])
                if current: entries.append(current)
                current = {'title': ''.join(bold).strip(), 'lines': [''.join(body).lstrip(': ')]}
            elif current:
                current['lines'].append(''.join(s['text'] for s in spans))
if current: entries.append(current)
normalize = lambda s: ''.join(c for c in s.casefold() if c.isalnum())
lookup = {}
for entry in entries:
    text = join(entry['lines'])
    text = re.sub(r'\s*\(Chapter\s+\d+\)\s*', '', text).strip()
    lookup[normalize(entry['title'])] = (entry['title'], text)
puzzles = json.loads((ROOT/'src/puzzlebook/data/puzzles.json').read_text())
result=[]; missing=[]
for puzzle in puzzles:
    match = lookup.get(normalize(puzzle['title_en']))
    if not match: missing.append((puzzle['id'],puzzle['title_en']));continue
    result.append({'id':puzzle['id'],'title_en':puzzle['title_en'],'hint_en':match[1]})
# The revised book has no alphabetical entry for this puzzle.
assert missing == [(56, 'Stopping After the Boy')], missing
result.append({'id':56, 'title_en':'Stopping After the Boy',
    'hint_en':'Think about each new birth separately. Does the decision to stop change the chances for that birth?',
    'source':'editorial'})
result.sort(key=lambda x:x['id'])
for hint in result:
    hint.setdefault('source', 'book')
(ROOT/'tmp/hints-extracted.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print('Entries:',len(entries),'Matched:',len(result),'Missing:',missing)
print('Unmatched titles:',[v[0] for k,v in lookup.items() if k not in {normalize(p['title_en']) for p in puzzles}])
