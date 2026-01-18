
# Schedule Sweep
A Python script to clean up your Google Calendar by grouping similar events and deleting them in bulk.

Unlike standard tools, this script uses "Fuzzy Grouping": it ignores numbers, dates, and punctuation to bundle related events together.

Example: "Gym Session 1", "Gym Session (Jan 12)", and "Gym Session!" are all grouped under "GYM SESSION" so you can delete them all with one click.



## Features
Fuzzy Grouping: Detects similar event titles automatically.

Pagination Support: Fetches thousands of events (bypassing the 250-event limit).

Safety First: Interactive CLI asks for confirmation before deleting any group.

Date Scoped: Currently configured to target 2026 (modifiable).

##  Prerequisite

**1. Python 3.x installed.**

**2. A Google Cloud Project with the Calendar API enabled.**
## Installation

**1. Install Dependencies:** Run the following command in your terminal to install the required Google libraries:

```bash
pip install --upgrade google-api-python-client 
google-auth-httplib2 google-auth-oauthlib
```



**2. Set Up Google Credentials**

- Go to the Google Cloud Console.

- Create a project and enable the Google Calendar API.

- Go to APIs & Services > Credentials.

- Create an OAuth 2.0 Client ID (Application Type: Desktop App).

- Download the JSON file and rename it exactly to: credentials.json

- Important: Move credentials.json into the same folder as this script.
