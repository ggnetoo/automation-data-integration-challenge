# Workflow Automation

The workflow runs in n8n. After the Python pipeline generates the CSV, it calls an n8n webhook endpoint to trigger the rest of the flow: parse the file, upsert the rows into the database and send a notification with the processing summary.

## Flow

1. **CSV Ready Trigger** (Webhook): Receives a `POST /webhook/csv-ready` from the pipeline after the CSV is generated. Serves as the entry point for the automation.
2. **Read File from Disk**: Reads the CSV from a local path using the file path received in the webhook payload.
3. **Parse CSV**: The Spreadsheet File node parses the binary file into structured rows.
4. **Upsert into PostgreSQL**: The Postgres node inserts or updates the user metrics using `ON CONFLICT`.
5. **Send Webhook Notification**: An HTTP Request node POSTs a JSON summary to the notification endpoint:

```json
{
  "event": "pipeline_completed",
  "processed_users": 10,
  "total_posts": 100
}
```

The `processed_users` and `total_posts` values are computed dynamically from the items that passed through the Read CSV node.

## Trigger design

The PDF allows either a folder watch or a storage service as the trigger. A webhook trigger was chosen because it fits naturally into the existing architecture — the Python pipeline already generates the CSV and can call the n8n endpoint directly after saving the file. This avoids polling and makes the handoff between the pipeline and the automation explicit.

In production this webhook could also be replaced by a Google Drive or S3 event trigger with no changes to the downstream nodes.

## Notes

For a production setup I would add an error branch after the Postgres node so that a failed upsert triggers a separate alert instead of silently stopping the flow. For this challenge the happy path is enough to demonstrate the design.
