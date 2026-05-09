# Workflow Automation

I would build this workflow in Zapier or n8n. The idea is simple: every time a new CSV is added to a monitored folder, the workflow reads it, sends the rows to the database and notifies the team.

## Option 1: Zapier

1. Trigger: New File in Google Drive Folder.
2. Action: Formatter by Zapier, using the CSV import/parse step.
3. Action: PostgreSQL, using Insert or Update Row for each processed user.
4. Action: Slack or Gmail notification.

Notification message:

```text
Data pipeline executed successfully.
Processed users: 10
Processed posts: 100
```

## Option 2: n8n

1. Google Drive Trigger watches the folder.
2. Spreadsheet File node reads the CSV.
3. Postgres node upserts the users and metrics.
4. Slack or Email node sends a short completion summary.

## Notes

For a production version, I would add an error branch with a notification when the CSV is missing required columns or when the database insert fails. For this challenge, I kept the flow direct and easy to explain.

