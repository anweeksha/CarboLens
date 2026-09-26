# CarbonLens API

FastAPI backend for **SU-02 CarbonLens**. This slice connects the app to **Supabase PostgreSQL**. Auth, carbon calculations, recommendations, challenges, and OCR are not implemented yet.

## Configure Supabase (`DATABASE_URL`)

Credentials belong only in `backend/.env` (gitignored). Do not hardcode them.

1. Copy the example file:

   ```powershell
   copy .env.example .env
   ```

2. In the [Supabase dashboard](https://supabase.com/dashboard), open your project → **Project Settings** → **Database**.

3. Copy the PostgreSQL **URI** connection string (Session pooler or Direct connection). It looks like `postgresql://postgres....@...supabase.com:5432/postgres`.

4. Paste it as `DATABASE_URL` in `backend/.env`, replacing `your_supabase_postgresql_connection_string`.

The app loads `.env` via python-dotenv. Existing OS environment variables are not overwritten. A `postgresql://` URI is rewritten to `postgresql+psycopg2://`. For `*.supabase.*` hosts, `sslmode=require` is added if absent.

## Create tables (explicit)

Tables are **not** created automatically on API startup, and existing tables are never dropped.

From `backend/` with the venv active and `DATABASE_URL` set:

```powershell
python -m app.database.init_db
```

## Run

```powershell
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

## Health

```powershell
curl http://127.0.0.1:8000/api/health
curl http://127.0.0.1:8000/api/health/db
```

`GET /api/health/db` returns `{"status":"healthy","database":"connected"}` or HTTP 503 if PostgreSQL is unreachable.
