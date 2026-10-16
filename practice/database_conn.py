"""Postgres connection helper; the URL comes from DATABASE_URL in the .env file."""
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def get_connection():
    url = os.getenv("DATABASE_URL")
    if not url:
        raise RuntimeError("DATABASE_URL is not set in the .env file")
    return psycopg.connect(url)


if __name__ == "__main__":
    with get_connection() as conn:
        print(conn.execute("SELECT current_database(), current_user, version()").fetchone())
