import logging
from datetime import datetime, timezone
from pathlib import Path

import psycopg2
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field

from config import DATABASE_URL


BASE_DIR = Path(__file__).resolve().parent
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI(title="Automation Data Integration API", version="1.0.0")


class UserPayload(BaseModel):
    name: str = Field(min_length=2)
    email: EmailStr
    company: str = Field(min_length=2)
    city: str | None = None


def _save_to_db(payload: UserPayload) -> None:
    if not DATABASE_URL:
        logging.info("DATABASE_URL not configured — skipping DB insert")
        return
    try:
        with psycopg2.connect(DATABASE_URL) as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO companies (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                (payload.company,),
            )
            cur.execute(
                """
                INSERT INTO users (external_user_id, name, email, city, company_id)
                SELECT COALESCE((SELECT MAX(external_user_id) FROM users), 0) + 1,
                       %s, %s, %s, c.id
                FROM companies c
                WHERE c.name = %s
                ON CONFLICT (email) DO NOTHING
                """,
                (payload.name, payload.email, payload.city or "", payload.company),
            )
        logging.info("User %s saved to DB", payload.email)
    except psycopg2.Error as err:
        logging.warning("DB insert failed for %s: %s", payload.email, err)


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.post("/webhook/new-user", status_code=201)
def receive_user(payload: UserPayload) -> dict:
    user_record = {
        "name": payload.name,
        "email": payload.email,
        "company": payload.company,
        "city": payload.city,
        "received_at": datetime.now(timezone.utc).isoformat(),
    }
    logging.info("Webhook received user: %s", payload.email)
    _save_to_db(payload)
    return {
        "success": True,
        "message": "User received and ready to be inserted",
        "data": user_record,
    }
