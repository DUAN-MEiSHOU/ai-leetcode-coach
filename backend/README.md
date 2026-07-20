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

## Not Included Yet

- Real DeepSeek calls until `DEEPSEEK_API_KEY` is configured locally
- PostgreSQL persistence
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
