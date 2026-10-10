"""Measure first visible SSE text, rather than just HTTP response headers."""
import argparse
import json
import statistics
from time import perf_counter

import httpx

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('url')
parser.add_argument('--samples', type=int, default=3)
args = parser.parse_args()
measurements = []
with httpx.Client(timeout=90) as client:
    for _ in range(args.samples):
        started = perf_counter()
        first_text = None
        answer = ''
        completed = False
        with client.stream('POST', args.url.rstrip('/') + '/api/ask',
                           json={'puzzle_id': 2, 'text': 'האם הם נולדו באותה שנה?'}) as response:
            response.raise_for_status()
            headers = perf_counter() - started
            for line in response.iter_lines():
                if not line.startswith('data: '):
                    continue
                event = json.loads(line[6:])
                if event['type'] == 'text' and event['text']:
                    if first_text is None:
                        first_text = perf_counter() - started
                    answer += event['text']
                elif event['type'] == 'done':
                    completed = True
                elif event['type'] == 'error':
                    raise RuntimeError(event['message'])
        if first_text is None or not completed:
            raise RuntimeError('Incomplete answer stream')
        sample = {'headers_s': round(headers, 3), 'ttfs_s': round(first_text, 3),
                  'total_s': round(perf_counter() - started, 3), 'answer': answer}
        measurements.append(sample)
        print(json.dumps(sample, ensure_ascii=False), flush=True)
print(json.dumps({'median_ttfs_s': statistics.median(m['ttfs_s'] for m in measurements)}))
