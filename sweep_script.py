import datetime
import os.path
import re
from collections import defaultdict
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# --- CONFIGURATION ---
SCOPES = ['https://www.googleapis.com/auth/calendar']
CALENDAR_ID = 'primary'
START_DATE = datetime.datetime(2026, 1, 1).isoformat() + 'Z'
END_DATE = datetime.datetime(2027, 1, 1).isoformat() + 'Z'

def get_clean_key(title):
    """
    Removes numbers, dates, and special characters to find the 'core' name.
    """
    if not title:
        return "no title"
    text = title.lower()
    text = re.sub(r'[^a-z\s]', '', text)
    return " ".join(text.split())

def main():
    # --- AUTHENTICATION ---
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('calendar', 'v3', credentials=creds)

    print(f"--- FETCHING ALL 2026 EVENTS (PAGING THROUGH RESULTS) ---")
    
    all_events = []
    page_token = None
    
    # --- PAGINATION LOOP ---
    while True:
        events_result = service.events().list(
            calendarId=CALENDAR_ID, 
            timeMin=START_DATE, 
            timeMax=END_DATE, 
            singleEvents=True, 
            orderBy='startTime',
            pageToken=page_token  # Ask for the specific page
        ).execute()
        
        items = events_result.get('items', [])
        all_events.extend(items)
        print(f"   ...Fetched {len(items)} events so far...")
        
        page_token = events_result.get('nextPageToken')
        if not page_token:
            break

    if not all_events:
        print("No events found in 2026.")
        return

    # --- GROUPING LOGIC ---
    groups = defaultdict(list)
    for event in all_events:
        original_title = event.get('summary', 'No Title')
        clean_key = get_clean_key(original_title)
        if not clean_key:
            clean_key = original_title
        groups[clean_key].append(event)

    print(f"\nTotal fetched: {len(all_events)} events.")
    print(f"Grouped into {len(groups)} categories.\n")
    print("--- STARTING REVIEW ---")

    for key, event_list in groups.items():
        count = len(event_list)
        example_title = event_list[0].get('summary', 'No Title')
        
        print(f"\nGroup: '{key.upper()}' (found {count} items)")
        print(f"   Example: '{example_title}'")

        choice = input(f"   >>> Delete ALL {count} events in this group? (y/n/q): ").strip().lower()

        if choice == 'y':
            print(f"   Deleting group...", end='', flush=True)
            for item in event_list:
                try:
                    service.events().delete(calendarId=CALENDAR_ID, eventId=item['id']).execute()
                    print(".", end='', flush=True)
                except HttpError as error:
                    # Handle rate limiting or already deleted items
                    print(f"x", end='')
            print(" Done.")
            
        elif choice == 'q':
            break
        else:
            print("   Skipped.")

if __name__ == '__main__':
    main()
