```markdown
# Database Design

This document explains the database structure used in the IELTS Writing Tutor Agent.

## Overview

The system uses a MySQL database to store user information and personalized learner reports.

The database is designed around two main tables:

1. `users`
2. `reports`

Each user has one account and one associated report row. The report is updated after each writing submission instead of creating a new row every time.

---

## Users Table

The `users` table stores authentication and profile information.

### Columns

| Column | Description |
|---|---|
| `User-ID` | Unique identifier for each user |
| `username` | The user's login username |
| `name` | The user's display name |
| `password` | The user's password |

### Purpose

This table allows the application to identify each learner and connect their activity to a persistent user profile.

When a user logs in, the system retrieves their user ID. This user ID is then used to load and update their writing report.

---

## Reports Table

The `reports` table stores personalized learner reports.

### Columns

| Column | Description |
|---|---|
| `User-ID` | Foreign key connected to the users table |
| `writing_report` | Compact summary of the learner's writing ability |
| `speaking_report` | Reserved for future speaking evaluation |

### Purpose

Each user has only one row in the `reports` table. This design keeps the database compact and avoids storing repeated feedback entries.

The `writing_report` column is updated after every writing submission.

---

## Why One Report Per User?

The system is designed to maintain a compact learner profile rather than a long history of all submissions.

This has several benefits:

1. Lower storage usage
2. Lower API cost
3. Faster retrieval of learner information
4. A cleaner personalization mechanism

Instead of appending every new evaluation, the system replaces the previous report with a newly summarized report.

---

## Report Update Flow

The report update process works as follows:

1. The user submits a writing answer.
2. The system loads the user's previous writing report from the database.
3. The previous report is sent to the LLM along with the new writing answer.
4. The LLM creates a new compact learner report.
5. The new report replaces the previous report in the database.

This allows the system to remember the learner's progress without storing long conversation histories.

