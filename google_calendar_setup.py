# google_calendar_setup.py - Google Calendar Authentication Setup
"""
Google Calendar Setup Guide and Authentication Handler

This script helps you set up Google Calendar integration for the Calendar Agent.
Follow these steps:

1. Go to Google Cloud Console (https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Calendar API
4. Create credentials (OAuth 2.0 Client ID)
5. Download the credentials.json file
6. Run this script to authenticate

"""

import os
import pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def setup_google_calendar():
    """Setup Google Calendar authentication"""
    creds = None
    
    # The file token.pickle stores the user's access and refresh tokens.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Make sure you have credentials.json file in the same directory
            if not os.path.exists('credentials.json'):
                print("""
                ERROR: credentials.json file not found!
                
                Please follow these steps:
                1. Go to https://console.cloud.google.com/
                2. Create a new project or select existing one
                3. Enable Google Calendar API
                4. Go to Credentials → Create Credentials → OAuth 2.0 Client ID
                5. Choose 'Desktop application'
                6. Download the JSON file and rename it to 'credentials.json'
                7. Place it in the same directory as this script
                """)
                return None
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=8000)
        
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    return creds

def test_calendar_connection():
    """Test the Google Calendar connection"""
    creds = setup_google_calendar()
    
    if not creds:
        return False
    
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        # Call the Calendar API to test connection
        print("Testing Google Calendar connection...")
        calendars_result = service.calendarList().list().execute()
        calendars = calendars_result.get('items', [])
        
        if not calendars:
            print('No calendars found.')
            return False
        
        print('✅ Successfully connected to Google Calendar!')
        print(f'Found {len(calendars)} calendar(s):')
        for calendar in calendars:
            print(f'  - {calendar["summary"]} ({calendar["id"]})')
        
        return True
        
    except Exception as e:
        print(f'❌ Error connecting to Google Calendar: {e}')
        return False

def create_sample_event():
    """Create a sample event to test booking functionality"""
    creds = setup_google_calendar()
    
    if not creds:
        return False
    
    try:
        service = build('calendar', 'v3', credentials=creds)
        
        from datetime import datetime, timedelta
        
        # Create a sample event for tomorrow
        tomorrow = datetime.now() + timedelta(days=1)
        start_time = tomorrow.replace(hour=14, minute=0, second=0, microsecond=0)
        end_time = start_time + timedelta(hours=1)
        
        event = {
            'summary': 'Test Event - AI Calendar Agent',
            'description': 'This is a test event created by the AI Calendar Agent',
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'UTC',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'UTC',
            },
        }
        
        event_result = service.events().insert(calendarId='primary', body=event).execute()
        print(f'✅ Sample event created: {event_result.get("htmlLink")}')
        return True
        
    except Exception as e:
        print(f'❌ Error creating sample event: {e}')
        return False

if __name__ == '__main__':
    print("🚀 Google Calendar Setup for AI Calendar Agent")
    print("="*50)
    
    # Test connection
    if test_calendar_connection():
        print("\n🎉 Google Calendar integration is ready!")
        
        # Ask if user wants to create a sample event
        create_sample = input("\nWould you like to create a sample event to test booking? (y/n): ")
        if create_sample.lower() == 'y':
            create_sample_event()
    else:
        print("\n❌ Google Calendar setup failed. Please check your credentials.")
        
    print("\n📝 Next steps:")
    print("1. Start the FastAPI backend: python app.py")
    print("2. Start the Streamlit frontend: streamlit run streamlit_app.py")
    print("3. Test the calendar agent in your browser!")