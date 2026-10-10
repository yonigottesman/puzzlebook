# Puzzlebook

A minimal Hebrew reader for Peter Winkler’s *Mathematical Puzzles, Revised Edition*. One HTML page, a sidebar in book order, difficulty labels, an English-original toggle, and bilingual hints.

## Run

```sh
uv sync
uv run uvicorn puzzlebook.app:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000. Python 3.12 or newer is required.

```sh
uv run pytest
```

## Content and classification

All 313 puzzle statements have Hebrew translations. The preface says 300, but the revised book contains 313 named entries. Full solutions were reviewed to classify the required background:

- **Easy (31):** accessible to ages 10–13 with arithmetic, concrete reasoning, simple counting, or basic shapes.
- **Medium (122):** secondary-school algebra, probability, geometry, or structured multi-step proofs.
- **Hard (160):** specialized concepts or substantial proof machinery, including infinite sets, topology, advanced probability, graph arguments, and invariants.

These labels describe mathematical preparation, not a guarantee that a puzzle will be quickly solved. A surprising elementary puzzle can still be challenging.

`content/hebrew.tsv` contains the reviewed translations and labels. `content/classification.json` records the required background and the solution PDF page for every entry. Only the public statement catalog is included in the initial HTML. The Hint button immediately fetches and shows the bilingual hint in a separate panel. Closing it or selecting another puzzle resets the panel. The Original toggle also switches the hint language. Solutions and private classification records are never served.

Question diagrams are provided for 140, 154, and 221. The two permitted orientations in 248 are redrawn. Mathematical notation lost during PDF extraction is repaired in `scripts/build_catalog.py`. Necessary context is repeated for standalone questions, and assumptions needed for the intended interpretation are made explicit.

To rebuild from the supplied `book.pdf`:

```sh
uv run python scripts/extract_book.py
uv run python scripts/extract_figures.py
uv run python scripts/build_catalog.py
uv run python scripts/extract_hints.py
uv run python scripts/build_hints.py
```

## Implementation

FastAPI application factory, lifespan-loaded Pydantic-validated data, Jinja autoescaping, package-relative file paths, and a narrow static mount. The responsive RTL layout uses plain CSS and vanilla JavaScript in one template; no frontend build is needed. The visual reference, Gitingest, uses Tailwind CSS; this app uses its own restrained styling.

The book supplies 312 alphabetical hints. Puzzle 56 has a short editorial hint because its book entry is missing. `content/hint-sources.json` records provenance; reviewed Hebrew hints are in `content/hints-{first,middle,last}.tsv`. Lost exponents and minor source errors are corrected in `scripts/build_hints.py`.

## Deployment

The private source repository is https://github.com/yonigottesman/puzzlebook.

Deploy with your authenticated Google Cloud CLI:

```sh
bash scripts/deploy.sh
```

The script deploys Cloud Run in `personal-ai-264306`, region `europe-west1`, using the dedicated `puzzlebook-runtime` service account. It uses 0.08 vCPU, 128 MiB memory, request-based CPU allocation, concurrency 1, zero minimum instances, and at most one instance. The container runs as a non-root user and includes only the installed application and its runtime dependencies. The PDF, working files, and content-review records are excluded from the build upload.

GitHub Actions runs the tests on pushes and pull requests. Deployment is performed with the script above.
