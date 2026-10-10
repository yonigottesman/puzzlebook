"""Extract puzzle headings and link each to its solution. Developer-only source."""
import json
import re
from pathlib import Path
import pymupdf

book = pymupdf.open('book.pdf')
def lines(page):
    for block in page.get_text('dict')['blocks']:
        for line in block.get('lines', []):
            spans = line['spans']
            text = ''.join(s['text'] for s in spans).strip()
            if not text or line['bbox'][1] > 680:
                continue
            title = all(s['font'] == 'CMBX12' and 11.9 < s['size'] < 12.1 for s in spans)
            yield text, title

def clean(s):
    return re.sub(r'(?<=\w)-\n(?=\w)', '', s).replace('\n', ' ')
puzzles = []
for pi in range(8,70):
    for text, title in lines(book[pi]):
        if title:
            puzzles.append({'id':len(puzzles)+1,'title_en':text,'source_page':pi-7,'pdf_page':pi+1,'body_en':''})
        elif puzzles and text != 'The Puzzles':
            puzzles[-1]['body_en'] += text+'\n'
for p in puzzles:
    p['body_en']=clean(p['body_en']).strip()
def key(t): return re.sub(r'[^a-z0-9]', '', t.casefold())
by_title={key(p['title_en']):p for p in puzzles}
current=None
for pi in range(84,418):
    for text,title in lines(book[pi]):
        if title:
            current=by_title.get(key(text))
            if current is not None:
                current['solution_pdf_page']=pi+1
                current['solution']=''
        elif current is not None:
            current['solution']+=text+'\n'
for p in puzzles:
    p['solution']=clean(p.get('solution',''))
Path('tmp/extracted.json').write_text(json.dumps(puzzles,ensure_ascii=False,indent=2))
print('Count',len(puzzles),'Missing solutions',[p['title_en'] for p in puzzles if not p['solution']])
for p in puzzles: print(p['id'],p['title_en'],p.get('solution_pdf_page'))
