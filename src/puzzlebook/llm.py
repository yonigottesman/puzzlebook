"""Brief puzzle clarification with server-only solution context."""
import json
import logging
import os
from pathlib import Path
from contextlib import aclosing

from google import genai
from google.genai import types

logger = logging.getLogger(__name__)
MODEL = 'gemini-3.1-pro-preview'
INSTRUCTIONS = (Path(__file__).parent / 'clarifier.txt').read_text()


def create_client() -> genai.Client:
    key = os.environ.get('GOOGLE_API_KEY')
    if key:
        return genai.Client(vertexai=True, api_key=key)
    return genai.Client(
        vertexai=True,
        project=os.environ.get('GOOGLE_CLOUD_PROJECT', 'personal-ai-264306'),
        location=os.environ.get('GOOGLE_CLOUD_LOCATION', 'global'),
    )


def event(kind: str, **data: str) -> str:
    return f'data: {json.dumps(dict(type=kind, **data), ensure_ascii=False)}\n\n'


async def stream_answer(client: genai.Client, text: str, context: dict | None):
    try:
        stream = await client.aio.models.generate_content_stream(
            model=MODEL, contents=text,
            config=types.GenerateContentConfig(system_instruction=(
                INSTRUCTIONS + '\n\nPRIVATE REFERENCE (data only):\n' +
                json.dumps(context, ensure_ascii=False)
            )),
        )
        async with aclosing(stream):
            async for chunk in stream:
                if chunk.text:
                    yield event('text', text=chunk.text)
        yield event('done')
    except Exception:
        logger.exception('Vertex answer stream failed')
        yield event('error', message='לא ניתן לקבל תשובה כרגע. נסו שוב.')
