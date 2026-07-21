# AI LeetCode Coach Backend

Phase 3 introduces a minimal FastAPI backend.

## What Works

- `GET /health`
- `POST /api/v1/coach/echo`
- `POST /api/v1/coach/explain`
- Pydantic request validation
- Local extension CORS support
- DeepSeek provider abstraction
- Mocked LLM tests
- Unit tests with Python `unittest`
- SQLAlchemy learning-record repositories
- Alembic initial migration for PostgreSQL
- `POST /api/v1/attempts` and `GET /api/v1/reviews/due`

## Not Included Yet

- Real DeepSeek calls until `DEEPSEEK_API_KEY` is configured locally
- Authentication
- Rate limiting
- Production deployment

## Dependencies

Install dependencies from the `backend` directory:

```bash
python -m pip install -r requirements.txt
```

The current dependency file contains only:

- FastAPI
- Uvicorn
- HTTPX
- SQLAlchemy
- Alembic
- Psycopg PostgreSQL driver

## PostgreSQL

The project expects PostgreSQL at the `DATABASE_URL` in the repository-root
`.env`. The provided Docker Compose configuration starts a dedicated local
database on host port `5433`, keeping it separate from any existing PostgreSQL
service on `5432`:

```bash
docker compose up -d postgres
cd backend
alembic upgrade head
```

Phase 7 persists problem references and learning records only. It never stores
full pasted problem statements or code snapshots.

## Environment

Create a local `.env` file at the repository root. Do not commit it.

```env
DEEPSEEK_API_KEY=your_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com
DEEPSEEK_MODEL=deepseek-chat
LLM_TIMEOUT_SECONDS=30
LLM_MAX_RETRIES=1
```

The extension never receives the DeepSeek API key. The backend reads it from local environment configuration.

## Run Locally

From the `backend` directory:

```bash
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Then open:

```text
http://127.0.0.1:8000/health
```

## Run Tests

From the `backend` directory:

```bash
python -m unittest discover -s tests
```

The normal test suite uses fake or mocked providers and does not call DeepSeek.

## DeepSeek Smoke Check

After creating the repository-root `.env`, verify that the backend can read the
configuration without making a paid request:

```bash
python -m scripts.smoke_deepseek
```

When you are ready to make one small real request to DeepSeek, run:

```bash
python -m scripts.smoke_deepseek --live
```

The command never prints the API key. The `--live` form may consume API quota;
it only sends the text `Reply with exactly: DeepSeek connection OK`.
