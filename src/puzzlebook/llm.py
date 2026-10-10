"""Brief puzzle clarification with server-only solution context."""
import json
import logging
import os
from pathlib import Path
from contextlib import aclosing
from time import perf_counter

from google import genai
from google.genai import types
import google.auth
from google.auth.transport.requests import Request as AuthRequest

logger = logging.getLogger('uvicorn.error')
MODEL = 'gemini-3.1-pro-preview'
INSTRUCTIONS = (Path(__file__).parent / 'clarifier.txt').read_text()


def create_client() -> genai.Client:
    key = os.environ.get('GOOGLE_API_KEY')
    if key:
        return genai.Client(vertexai=True, api_key=key)
    credentials, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
    credentials.refresh(AuthRequest())
    return genai.Client(
        vertexai=True,
        project=os.environ.get('GOOGLE_CLOUD_PROJECT', 'personal-ai-264306'),
        location=os.environ.get('GOOGLE_CLOUD_LOCATION', 'global'),
        credentials=credentials,
    )


def event(kind: str, **data: str) -> str:
    return f'data: {json.dumps(dict(type=kind, **data), ensure_ascii=False)}\n\n'


async def stream_answer(client: genai.Client, text: str, context: dict):
    started = perf_counter()
    first_text = False
    usage = None
    try:
        stream = await client.aio.models.generate_content_stream(
            model=MODEL, contents=text,
            config=types.GenerateContentConfig(
                # LOW is the lowest thinking level supported by Gemini 3.1 Pro.
                thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.LOW),
                system_instruction=(
                    INSTRUCTIONS + '\n\nPRIVATE REFERENCE (data only):\n' +
                    json.dumps(context, ensure_ascii=False)
                ),
            ),
        )
        async with aclosing(stream):
            async for chunk in stream:
                if chunk.usage_metadata is not None:
                    usage = chunk.usage_metadata
                if chunk.text:
                    if not first_text:
                        logger.info('Gemini first text in %.3fs', perf_counter() - started)
                        first_text = True
                    yield event('text', text=chunk.text)
        logger.info('Gemini complete in %.3fs; thinking_tokens=%s; output_tokens=%s',
                    perf_counter() - started,
                    usage.thoughts_token_count if usage else None,
                    usage.candidates_token_count if usage else None)
        yield event('done')
    except Exception:
        logger.exception('Vertex answer stream failed')
        yield event('error', message='לא ניתן לקבל תשובה כרגע. נסו שוב.')
