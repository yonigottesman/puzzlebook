import json
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from fastapi.testclient import TestClient

from puzzlebook.app import create_app
from puzzlebook.llm import MODEL


def mock_vertex(monkeypatch, chunks):
    async def generate():
        for chunk in chunks:
            if isinstance(chunk, Exception):
                raise chunk
            yield SimpleNamespace(text=chunk)

    client = MagicMock()
    client.aio.models.generate_content_stream = AsyncMock(side_effect=lambda **kwargs: generate())
    client.aio.aclose = AsyncMock()
    monkeypatch.setattr('puzzlebook.app.create_client', lambda: client)
    return client


def events(response):
    return [json.loads(frame.removeprefix('data: '))
            for frame in response.text.strip().split('\n\n')]


def test_streams_unicode_with_private_selected_puzzle_context(monkeypatch):
    vertex = mock_vertex(monkeypatch, [None, 'שלום ', 'עולם'])
    with TestClient(create_app()) as client:
        response = client.post('/api/ask', json={'text': '  מה נשמע?  ', 'puzzle_id': 2})
        assert response.status_code == 200
        assert response.headers['content-type'].startswith('text/event-stream')
        assert events(response) == [
            {'type': 'text', 'text': 'שלום '},
            {'type': 'text', 'text': 'עולם'},
            {'type': 'done'},
        ]
        kwargs = vertex.aio.models.generate_content_stream.await_args.kwargs
        assert kwargs['model'] == MODEL and kwargs['contents'] == '  מה נשמע?  '
        instructions, reference = kwargs['config'].system_instruction.split('PRIVATE REFERENCE (data only):\n')
        context = json.loads(reference)
        assert context['puzzle']['title_en'] == 'No Twins Today'
        assert context['hint']['id'] == 2
        assert 'triplets' in context['official_solution']
        assert 'Bat and Ball' not in reference
        assert 'Wrong.' in instructions and "I won't answer that." in instructions
        assert 'adequate explanation' in instructions
    vertex.aio.aclose.assert_awaited_once()
    vertex.close.assert_called_once()


def test_stream_failure_preserves_partial_response_without_exposing_details(monkeypatch):
    mock_vertex(monkeypatch, ['חלק מהתשובה', RuntimeError('private upstream details')])
    with TestClient(create_app()) as client:
        response = client.post('/api/ask', json={'text': 'hi', 'puzzle_id': 1})
        result = events(response)
        assert result[0] == {'type': 'text', 'text': 'חלק מהתשובה'}
        assert result[1]['type'] == 'error'
        assert 'private upstream details' not in response.text


def test_invalid_questions_never_call_vertex(monkeypatch):
    vertex = mock_vertex(monkeypatch, [])
    with TestClient(create_app()) as client:
        for body in [{'text': '', 'puzzle_id': 1}, {'text': '   ', 'puzzle_id': 1},
                     {'text': 'x' * 10001, 'puzzle_id': 1},
                     {'text': 'hi', 'puzzle_id': 1, 'context': 'puzzle'},
                     {'text': 'hi'}, {'text': 'hi', 'puzzle_id': None}]:
            assert client.post('/api/ask', json=body).status_code == 422
        assert client.post('/api/ask', json={'text': 'hi', 'puzzle_id': 314}).status_code == 404
    vertex.aio.models.generate_content_stream.assert_not_called()


def test_missing_credentials_returns_service_error(monkeypatch):
    def fail():
        raise RuntimeError('private credential details')
    monkeypatch.setattr('puzzlebook.app.create_client', fail)
    with TestClient(create_app()) as client:
        response = client.post('/api/ask', json={'text': 'hi', 'puzzle_id': 1})
        assert response.status_code == 503
        assert 'private credential details' not in response.text


def test_solutions_are_complete_but_never_served():
    from puzzlebook.app import load_solutions
    solutions = load_solutions()
    assert list(solutions) == list(range(1, 314))
    with TestClient(create_app()) as client:
        html = client.get('/').text
        assert solutions[2].solution not in html
        assert 'official_solution' not in html
        for path in ['/data/solutions.json', '/static/solutions.json', '/clarifier.txt']:
            assert client.get(path).status_code == 404
