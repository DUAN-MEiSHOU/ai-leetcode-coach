# AI LeetCode Coach Backend

Phase 3 introduces a minimal FastAPI backend.

## What Works

- `GET /health`
- `POST /api/v1/coach/echo`
- Pydantic request validation
- Local extension CORS support
- Unit tests with Python `unittest`

## Not Included Yet

- DeepSeek integration
- PostgreSQL persistence
- Authentication
- Rate limiting
- Production deployment

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
