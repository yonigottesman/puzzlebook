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
        assert 'solution_pdf_page' not in response.text
        assert '"solution"' not in response.text
        assert client.get('/healthz').json() == {'status': 'ok', 'puzzles': 313}
        for path in ['/book.pdf', '/content/classification.json', '/tmp/extracted.json', '/docs', '/openapi.json']:
            assert client.get(path).status_code == 404
        assert client.get('/static/figures/140.png').status_code == 200


def test_hints_are_bilingual_and_loaded_separately():
    from puzzlebook.app import load_hints
    hints = load_hints()
    assert set(hints) == set(range(1, 314))
    with TestClient(create_app()) as client:
        html = client.get('/').text
        assert '"hint_he"' not in html and '"hint_en"' not in html
        for ident in [1, 56, 141, 224, 313]:
            response = client.get(f'/api/puzzles/{ident}/hint')
            assert response.status_code == 200
            assert response.json() == hints[ident].model_dump()
            assert set(response.json()) == {'id', 'hint_he', 'hint_en'}
        assert client.get('/api/puzzles/314/hint').status_code == 404
        assert client.get('/data/hints.json').status_code == 404
