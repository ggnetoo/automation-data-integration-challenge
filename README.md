# Automation & Data Integration Challenge

End-to-end data pipeline that fetches users and posts from a public API, normalizes and joins the data, saves a CSV, models the result in SQL, generates a dashboard in Excel and exposes a webhook endpoint for receiving new users.

## What is included

- Python ETL pipeline with retry logic and logging
- CSV output with processed user metrics
- SQL schema, seed data and analytical queries
- FastAPI webhook endpoint with database insert
- Pre-generated Excel dashboard (`dashboard.xlsx`)
- Workflow automation export for n8n

## Project structure

```text
automation-data-integration-challenge/
  pipeline.py            # ETL pipeline
  webhook_api.py         # FastAPI webhook
  create_dashboard.py    # Excel dashboard generator
  config.py              # Centralized config from env
  sample_data.py         # Local fallback data
  requirements.txt
  processed_users.csv    # Pipeline output
  dashboard.xlsx         # Pre-generated Excel dashboard
  automation_workflow.md
  dashboard_instructions.md
  webhook_payload_example.json
  workflow_export_n8n.json
  sql/
    schema.sql
    insert_data.sql
    queries.sql
  screenshots/
    empty_db.png              # database before workflow runs
    n8n_workflow_executed.png # all 5 nodes green after execution
    dt_data_after_n8n.png    # database populated after workflow
  logs/
    pipeline.log
```

## Prerequisites

- Python 3.10+
- Node.js 18+ (required only for running n8n locally)
- PostgreSQL (required only for the SQL part and webhook DB insert)

## Setup

Copy `.env.example` to `.env` and fill in your values, then install Python dependencies:

```bash
pip install -r requirements.txt
```

## Run the pipeline

```bash
python pipeline.py
```

Generates `processed_users.csv`. Uses the JSONPlaceholder API with a local fallback dataset if the API is unavailable.

## Generate the Excel dashboard

```bash
python create_dashboard.py
```

Generates `dashboard.xlsx` with two bar charts (users per city and posts per company) and a KPI for average posts per user. The aggregated summary tables work as pivot tables — if you prefer native pivot tables in Excel or Google Sheets, `dashboard_instructions.md` has step-by-step instructions.

## Run the webhook API

```bash
uvicorn webhook_api:app --reload
```

Interactive docs available at `http://127.0.0.1:8000/docs`.

Example request:

```text
POST /webhook/new-user
```

```json
{
  "name": "John Doe",
  "email": "john.doe@email.com",
  "company": "ACME Data",
  "city": "Sao Paulo"
}
```

The endpoint validates the payload, logs the event and inserts the user into the database if `DATABASE_URL` is configured in `.env`. If no database is available, it logs a warning and returns the success response anyway.

## Database setup

Run the SQL files in order against a PostgreSQL instance:

```text
sql/schema.sql       -- create tables and indexes
sql/insert_data.sql  -- seed users, companies, posts and metrics
sql/queries.sql      -- analytical queries
```

The model keeps companies in a separate table to avoid duplicated data and makes the aggregation queries simpler to write and maintain.

## Workflow automation

The n8n workflow (`workflow_export_n8n.json`) triggers via webhook after the pipeline generates the CSV, reads the file from disk, upserts the rows to the database and sends a webhook notification with the number of processed users and total posts. See `automation_workflow.md` for design notes.

To run n8n locally:

```bash
npx n8n
```

Then open `http://localhost:5678`, go to **Workflows → Import from file** and select `workflow_export_n8n.json`.

## Design decisions

The pipeline is split into small functions to make each step easy to follow and test independently. Retry logic handles short API outages without failing the whole run. Environment variables keep the configuration separate from the code.

FastAPI was chosen for the webhook because it is lightweight, validates input automatically through Pydantic and generates interactive API documentation out of the box.
