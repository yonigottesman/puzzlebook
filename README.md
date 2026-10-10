# Puzzlebook

A minimal Hebrew reader for Peter Winkler’s *Mathematical Puzzles, Revised Edition*. A welcome view at `/` and puzzle views at `/#puzzle-ID`, in one HTML page with a sidebar in book order, difficulty labels, an English-original toggle, and bilingual hints.

## Run

```sh
uv sync
uv run uvicorn puzzlebook.app:app --reload --host 127.0.0.1 --port 8000
```

Open http://127.0.0.1:8000. Python 3.12 or newer is required.

## Questions

Every puzzle view has a question input and a streamed response, shown only when text arrives. The backend uses `google-genai` with Vertex AI and `gemini-3.1-pro-preview`. It supplies the selected puzzle in both languages, its bilingual hint, and its official solution as private context. `src/puzzlebook/clarifier.txt` instructs the model to clarify wording only, avoid hints and spoilers, answer briefly in the user's language, and confirm correct answers only when accompanied by an explanation. Wrong answers and disallowed requests receive a short response without elaboration. The model has no conversation history. Answers are displayed as plain text.

For local development, authenticate once with Application Default Credentials:

```sh
gcloud auth application-default login
uv run uvicorn puzzlebook.app:app --reload --host 127.0.0.1 --port 8000
```

The default project is `personal-ai-264306` and location is `global`; override with `GOOGLE_CLOUD_PROJECT` and `GOOGLE_CLOUD_LOCATION`. On Cloud Run, credentials are supplied automatically by the attached `puzzlebook-runtime` service account, which has the Vertex AI User role (`roles/aiplatform.user`). No API key environment variable is needed. If using Vertex API-key authentication instead, set `GOOGLE_API_KEY` in the server environment. No keys are embedded in the HTML or committed to the repository.

`POST /api/ask` accepts `{"text":"your question","puzzle_id":2}` and returns an SSE stream of JSON text chunks, followed by a completion event or a generic error. The server loads the context by ID; official solutions are never included in the HTML or exposed through a static route. The root has no AI form, and requests without a puzzle ID are rejected before calling the model. Selecting another puzzle clears the question and cancels any ongoing response.

```sh
uv run pytest
```

## Content and classification

All 313 puzzle statements have Hebrew translations. The preface says 300, but the revised book contains 313 named entries. Full solutions were reviewed to classify the required background:

- **Easy (31):** accessible to ages 10–13 with arithmetic, concrete reasoning, simple counting, or basic shapes.
- **Medium (122):** secondary-school algebra, probability, geometry, or structured multi-step proofs.
- **Hard (160):** specialized concepts or substantial proof machinery, including infinite sets, topology, advanced probability, graph arguments, and invariants.

These labels describe mathematical preparation, not a guarantee that a puzzle will be quickly solved. A surprising elementary puzzle can still be challenging.

`content/hebrew.tsv` contains the reviewed translations and labels. `content/classification.json` records the required background and the solution PDF page for every entry. The initial HTML includes the public statement catalog and bilingual hints. The Hint button instantly shows the hint in a separate panel without a network request. Closing it or selecting another puzzle resets the panel. The Original toggle also switches the hint language. Solutions and private classification records are never served.

Question diagrams are provided for 140, 154, and 221. The two permitted orientations in 248 are redrawn. Mathematical notation lost during PDF extraction is repaired in `scripts/build_catalog.py`. Necessary context is repeated for standalone questions, and assumptions needed for the intended interpretation are made explicit.

To rebuild from the supplied `book.pdf`:

```sh
uv run python scripts/extract_book.py
uv run python scripts/extract_figures.py
uv run python scripts/build_catalog.py
uv run python scripts/build_solutions.py
uv run python scripts/extract_hints.py
uv run python scripts/build_hints.py
```

## Implementation

FastAPI application factory, lifespan-loaded Pydantic-validated data, Jinja autoescaping, package-relative file paths, and a narrow static mount. The responsive RTL layout uses plain CSS and vanilla JavaScript in one template; no frontend build is needed. The visual reference, Gitingest, uses Tailwind CSS; this app uses its own restrained styling.

The book supplies 312 alphabetical hints. Puzzle 56 has a short editorial hint because its book entry is missing. `content/hint-sources.json` records provenance; reviewed Hebrew hints are in `content/hints-{first,middle,last}.tsv`. Lost exponents and minor source errors are corrected in `scripts/build_hints.py`.

## Deployment

Live app: https://puzzlebook-941271455567.europe-west1.run.app

The source repository is https://github.com/yonigottesman/puzzlebook.

Deploy with your authenticated Google Cloud CLI:

```sh
bash scripts/deploy.sh
```

The script deploys Cloud Run in `personal-ai-264306`, region `europe-west1`, using the dedicated `puzzlebook-runtime` service account. It uses 0.08 vCPU, 128 MiB memory, request-based CPU allocation, concurrency 1, zero minimum instances, and at most one instance. The container runs as a non-root user and includes only the installed application and its runtime dependencies. The PDF, working files, and content-review records are excluded from the build upload.

GitHub Actions runs tests on pushes and pull requests, then deploys successful pushes to `main` automatically. It uses Workload Identity Federation restricted to this repository's `main` branch, with the `puzzlebook-deploy` account for deployment and the `puzzlebook-build` account for builds. No service-account key is stored in GitHub. Each revision is labeled with its source commit, and the workflow checks the live page after deployment. The service's existing public access is preserved.

## Illustrations

The first 50 puzzles in book order, plus three previously illustrated easy puzzles, have warm, minimal cartoon illustrations below the question text. Artwork is served directly from the public `puzzlebook-images-941271455567` Cloud Storage bucket in `europe-west1`, without passing through FastAPI. The source images were reviewed against the solutions to avoid answer clues. Exact generation prompts and review notes are in `docs/illustration-samples/`; the public URLs and dimensions are in `src/puzzlebook/data/illustrations.json`.

To encode and upload approved local PNG originals:

```sh
bash scripts/publish_illustrations.sh
```

Use `bash scripts/publish_illustrations.sh --partial` to publish completed images while a batch is still being generated.

The script creates compact WebP files with a one-year cache lifetime. Originals and generated output files are excluded from Git and the Cloud Run build. Use a new filename version when replacing an illustration.
