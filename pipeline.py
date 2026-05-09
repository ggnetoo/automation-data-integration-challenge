import csv
import logging
from collections import Counter
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import BASE_DIR, OUTPUT_FILE, POSTS_URL, REQUEST_TIMEOUT, USERS_URL, USE_LOCAL_FALLBACK
from sample_data import SAMPLE_POSTS, SAMPLE_USERS


LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    filename=LOG_DIR / "pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def create_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def fetch_data(url: str, fallback_data: list[dict]) -> list[dict]:
    try:
        session = create_session()
        response = session.get(url, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        logging.info("Fetched data from %s", url)
        return response.json()
    except requests.RequestException as err:
        logging.warning("Could not reach %s: %s", url, err)
        if USE_LOCAL_FALLBACK:
            logging.info("Falling back to local data for %s", url)
            return fallback_data
        raise


def normalize_users(users: list[dict], posts: list[dict]) -> list[dict]:
    post_counts = Counter(p["userId"] for p in posts)

    result = []
    for user in users:
        address = user.get("address", {})
        company = user.get("company", {})
        result.append({
            "user_id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "city": address.get("city", ""),
            "company": company.get("name", ""),
            "total_posts": post_counts.get(user["id"], 0),
        })

    return sorted(result, key=lambda u: u["user_id"])


def save_csv(data: list[dict], filename: str) -> Path:
    output_path = BASE_DIR / filename
    fieldnames = ["user_id", "name", "email", "city", "company", "total_posts"]

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    logging.info("Saved %d records to %s", len(data), output_path.name)
    return output_path


def run_pipeline() -> Path:
    logging.info("Starting pipeline")
    users = fetch_data(USERS_URL, SAMPLE_USERS)
    posts = fetch_data(POSTS_URL, SAMPLE_POSTS)
    data = normalize_users(users, posts)
    path = save_csv(data, OUTPUT_FILE)
    logging.info("Done — %d users processed", len(data))
    return path


def main() -> None:
    path = run_pipeline()
    print(f"Done! File saved to: {path.name}")


if __name__ == "__main__":
    main()
