from app.core.config import _normalize_database_url


def test_database_url_handles_bracketed_passwords():
    value = "postgresql://postgres:[PASSWORD]@aws-0-ap-southeast-2.pooler.supabase.com:5432/postgres"
    normalized = _normalize_database_url(value)

    assert normalized.startswith("postgresql+psycopg2://postgres:PASSWORD@aws-0-ap-southeast-2.pooler.supabase.com:5432/postgres")
    assert "[PASSWORD]" not in normalized
    assert "sslmode=require" in normalized
