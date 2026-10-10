"""A single-page reader with instant bilingual hints."""
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, ConfigDict, Field, HttpUrl, TypeAdapter

PACKAGE = Path(__file__).resolve().parent


class Puzzle(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    id: int = Field(gt=0)
    title_he: str = Field(min_length=1)
    title_en: str = Field(min_length=1)
    body_he: str = Field(min_length=1)
    body_en: str = Field(min_length=1)
    level: Literal['easy', 'medium', 'hard']
    source_page: int = Field(gt=0)
    figures: list[str]


def load_puzzles() -> tuple[Puzzle, ...]:
    puzzles = TypeAdapter(list[Puzzle]).validate_json(
        (PACKAGE / 'data' / 'puzzles.json').read_bytes()
    )
    if len(puzzles) != 313 or [p.id for p in puzzles] != list(range(1, 314)):
        raise ValueError('Catalog must contain all 313 puzzles in book order')
    return tuple(puzzles)


class Hint(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    id: int = Field(gt=0)
    hint_he: str = Field(min_length=1)
    hint_en: str = Field(min_length=1)


def load_hints() -> dict[int, Hint]:
    hints = TypeAdapter(list[Hint]).validate_json(
        (PACKAGE / 'data' / 'hints.json').read_bytes()
    )
    if [hint.id for hint in hints] != list(range(1, 314)):
        raise ValueError('Every puzzle must have a bilingual hint')
    return {hint.id: hint for hint in hints}


class Illustration(BaseModel):
    model_config = ConfigDict(extra='forbid', frozen=True)

    id: int = Field(gt=0)
    url: HttpUrl
    width: int = Field(gt=0)
    height: int = Field(gt=0)


def load_illustrations(puzzles: tuple[Puzzle, ...]) -> dict[int, Illustration]:
    illustrations = TypeAdapter(list[Illustration]).validate_json(
        (PACKAGE / 'data' / 'illustrations.json').read_bytes()
    )
    ids = [i.id for i in illustrations]
    if ids != sorted(set(ids)) or not ids or ids[0] != 1 or not set(ids) <= {p.id for p in puzzles}:
        raise ValueError('Illustrations must have unique valid puzzle IDs in book order, starting with puzzle 1')
    return {i.id: i for i in illustrations}


def create_app() -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        app.state.puzzles = load_puzzles()
        app.state.hints = load_hints()
        app.state.illustrations = load_illustrations(app.state.puzzles)
        yield

    app = FastAPI(title='Puzzlebook', lifespan=lifespan,
                  docs_url=None, redoc_url=None, openapi_url=None)
    templates = Jinja2Templates(directory=PACKAGE / 'templates')
    app.mount('/static', StaticFiles(directory=PACKAGE / 'static'), name='static')

    @app.get('/', response_class=HTMLResponse)
    async def index(request: Request):
        puzzles = [dict(p.model_dump(), illustration=(
            request.app.state.illustrations[p.id].model_dump(mode='json')
            if p.id in request.app.state.illustrations else None
        )) for p in request.app.state.puzzles]
        return templates.TemplateResponse(request=request, name='index.html',
            context={'puzzles': puzzles, 'hints': [h.model_dump() for h in request.app.state.hints.values()], 'levels': {'easy': 'קל', 'medium': 'בינוני', 'hard': 'קשה'}})

    @app.get('/healthz', include_in_schema=False)
    async def health():
        return {'status': 'ok', 'puzzles': len(app.state.puzzles)}

    @app.get('/api/puzzles/{puzzle_id}/hint', response_model=Hint)
    async def hint(puzzle_id: int, request: Request):
        result = request.app.state.hints.get(puzzle_id)
        if result is None:
            raise HTTPException(status_code=404, detail='Puzzle not found')
        return result

    return app


app = create_app()
