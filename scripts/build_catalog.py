"""Build the public, spoiler-free catalog from reviewed translations."""
import json
from pathlib import Path
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
source = json.loads((ROOT / 'tmp/extracted.json').read_text())
rows = [line.split('|') for line in (ROOT/'content/hebrew.tsv').read_text().splitlines() if line]
assert len(source) == len(rows) == 313
skills = {
 'arithmetic':'ארבע פעולות חשבון ושברים', 'logic':'הסקה לוגית קונקרטית, ללא נוסחאות',
 'counting':'ספירה שיטתית וחשבון בסיסי','geometry':'צורות בסיסיות ותפיסה מרחבית',
 'games':'משחקים קטנים ובדיקת אפשרויות','percent':'אחוזים ויחסים','parity':'זוגי ואי־זוגי',
 'divisibility':'מחלקים וזוגיות','context':'ידע חיצוני: שפה, כללי משחק או מוסכמות',
 'continuity':'רציפות ומשפט ערך הביניים','logicproof':'הסקה רב־שלבית והוכחה',
 'probability':'הסתברות בסיסית, סימטריה וספירת מקרים','countingproof':'קומבינטוריקה והוכחת חסם',
 'potential':'פונקציות פוטנציאל, אינווריאנטים והוכחת סיום',
 'conditional':'הסתברות מותנית והגדרת מרחב המדגם','graphs':'תורת גרפים: מסלולים, קשירות או צביעה',
 'averaging':'שיטת הממוצעים והשיטה ההסתברותית','gamesproof':'אסטרטגיות משחק והוכחת ניצחון',
 'geometryproof':'גאומטריה והוכחות, כולל חסמים ובניות','expectation':'תוחלת, זמני המתנה או לינאריות התוחלת',
 'sequences':'סדרות חשבוניות וסכומים','algebra':'אלגברה תיכונית ומשוואות',
 'numbertheory':'תורת המספרים: שאריות, גורמים וחלוקה','construction':'בנייה קומבינטורית והוכחת תקפות',
 'algebraproof':'אלגברה, אי־שוויונות והוכחות','induction':'אינדוקציה מתמטית ובנייה רקורסיבית',
 'nim':'תורת משחקים, נים וייצוג בינארי','gamesprobability':'אסטרטגיות והסתברות רב־שלבית',
 'coordinates':'קואורדינטות, סימטריות ואינווריאנטים','information':'מידע, קידוד וקומבינטוריקה',
 'spatial':'גאומטריה מרחבית והטלות','parityproof':'זוגיות, אינווריאנטים והוכחות',
 'randomwalk':'הילוכים אקראיים והסתברות','limits':'גבולות, טורים והתכנסות',
 'probabilitydistribution':'התפלגויות הסתברות בדידות או רציפות','physics':'מכניקה, תנועה והתנגשויות',
 'algorithms':'אלגוריתמים והוכחת נכונות או סיום','infinity':'קבוצות אינסופיות, מנייה או אקסיומת הבחירה',
 'topology':'טופולוגיה וגאומטריה רציפה','polynomials':'פולינומים, מקדמים ובסיסי ספירה',
 'permutations':'תמורות, זוגיות או פירוק למחזורים','coding':'קידוד בינארי וקודים לתיקון שגיאות',
 'linearalgebra':'וקטורים ומערכות משוואות לינאריות',
}
fixes = {
19:[('1 4 ′′','¼ inch'),('2 1 2 ′′','2½ inches')],
117:[('1 3.', '1/3.')],
81:[('1010','10¹⁰')],120:[('49 + 610 + 320','4⁹ + 6¹⁰ + 3²⁰')],
155:[('81n','81ⁿ')],190:[('a!b = c!d','(a!)ᵇ = (c!)ᵈ')],196:[('n2','n²')],
201:[('xxx···','x^(x^(x^(⋯)))')],204:[('229','2²⁹')],
219:[('\x0050 2 \x01','C(50, 2)')],
228:[('x2','x²'),('x4','x⁴'),('x8','x⁸'),('x16','x¹⁶'),('x32','x³²')],
243:[('n3','n³'),('n2','n²')],251:[('2n','2ⁿ'),('Rn','Rⁿ')],255:[('264','2⁶⁴')],
303:[('x1.01','x^1.01'),('y1.01','y^1.01')],305:[('2n','2ⁿ')],
}
public=[]; audit=[]
for p,row in zip(source,rows,strict=True):
    ident,level,title,body,skill=row
    assert int(ident)==p['id']
    assert level in {'easy','medium','hard'} and skill in skills
    assert p.get('solution') and p['body_en'] and body and title
    english=p['body_en']
    for old,new in fixes.get(p['id'],[]): english=english.replace(old,new)
    if p['id'] == 114: english = source[112]['body_en'] + '\n\n' + english
    if p['id'] == 266: english = source[264]['body_en'] + '\n\n' + english
    if p['id'] == 212: english = english.replace('n positive numbers', 'n positive integers')
    if p['id'] == 260: english += '\n\nAssume the team scores another touchdown and has a 50% chance of winning in overtime if tied.'
    if p['id'] == 303: english = english.replace('Prove that after', 'Prove that, with probability 1, after')
    assert not any(ord(c)<32 and c != '\n' for c in english)
    public.append({'id':p['id'],'title_he':title,'title_en':p['title_en'],
        'body_he':body,'body_en':english,'level':level,'source_page':p['source_page'],
        'figures':[f'{p["id"]}.svg' if p['id'] == 248 else f'{p["id"]}.png'] if p['id'] in {140,154,221,248} else []})
    audit.append({'id':p['id'],'title_en':p['title_en'],'level':level,
        'background_required':skills[skill], 'solution_pdf_page':p['solution_pdf_page'],
        'basis':'סיווג ידני לפי הידע והטיעון שבפתרון הספר; רמת הגיל אינה הבטחת הצלחה.'})
(ROOT/'src/puzzlebook/data/puzzles.json').write_text(json.dumps(public,ensure_ascii=False,indent=2)+'\n')
(ROOT/'content/classification.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n')
print(Counter(p['level'] for p in public))
