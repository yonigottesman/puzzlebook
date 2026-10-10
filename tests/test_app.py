from fastapi.testclient import TestClient
from puzzlebook.app import create_app, load_puzzles, PACKAGE


def test_complete_catalog_and_statement_figures():
    puzzles = load_puzzles()
    assert [p.id for p in puzzles] == list(range(1, 314))
    for p in puzzles:
        for figure in p.figures:
            assert (PACKAGE / 'static/figures' / figure).is_file()
    assert {p.id for p in puzzles if p.figures} == {140, 154, 221, 248}


def test_reader_exposes_only_public_catalog():
    with TestClient(create_app()) as client:
        response = client.get('/')
        assert response.status_code == 200
        assert response.text.count('class="puzzle-link"') == 313
        assert 'body_he' in response.text and 'body_en' in response.text
        assert 'תרגום לעברית של' in response.text
        assert 'id="puzzle-view" aria-labelledby="puzzle-title" hidden' in response.text
        assert 'welcome-family-v2.webp' in response.text
        assert 'solution_pdf_page' not in response.text
        assert '"solution"' not in response.text
        assert client.get('/healthz').json() == {'status': 'ok', 'puzzles': 313}
        for path in ['/book.pdf', '/content/classification.json', '/tmp/extracted.json', '/docs', '/openapi.json']:
            assert client.get(path).status_code == 404
        assert client.get('/static/figures/140.png').status_code == 200


def test_hints_are_bilingual_and_available_immediately():
    from puzzlebook.app import load_hints
    hints = load_hints()
    assert set(hints) == set(range(1, 314))
    with TestClient(create_app()) as client:
        html = client.get('/').text
        import json
        from re import search
        embedded = json.loads(search(r'<script id="hint-data" type="application/json">(.*?)</script>', html, flags=16).group(1))
        assert embedded == [h.model_dump() for h in hints.values()]
        assert 'טוען' not in html and 'מתוך הספר · עמוד' not in html
        for ident in [1, 56, 141, 224, 313]:
            response = client.get(f'/api/puzzles/{ident}/hint')
            assert response.status_code == 200
            assert response.json() == hints[ident].model_dump()
            assert set(response.json()) == {'id', 'hint_he', 'hint_en'}
        assert client.get('/api/puzzles/314/hint').status_code == 404
        assert client.get('/data/hints.json').status_code == 404


def test_first_fifty_puzzles_have_external_illustrations():
    import json
    import re
    from puzzlebook.app import load_illustrations

    puzzles = load_puzzles()
    illustrations = load_illustrations(puzzles)
    assert set(illustrations) == set(range(1, 51)) | {51, 57, 58}
    with TestClient(create_app()) as client:
        html = client.get('/').text
        embedded = json.loads(re.search(
            r'<script id="puzzle-data" type="application/json">(.*?)</script>', html,
            flags=re.DOTALL,
        ).group(1))
        assert [p['id'] for p in embedded if p['illustration']] == list(illustrations)
        assert html.index('id="puzzle-body"') < html.index('id="illustration"') < html.index('id="hint-toggle"')
        for image in illustrations.values():
            assert str(image.url).startswith('https://storage.googleapis.com/puzzlebook-images-941271455567/')
