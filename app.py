import os
from dotenv import load_dotenv
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from readtable import read_table
from utils.reformat import reformat

load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = '1cYhJToC6uCt78nh60bjQFaG9HCiG9q3lQAbpZH19G3E'
SAMPLE_RANGE_NAME = 'Маковська'

"""Shows basic usage of the Sheets API.
Prints values from a sample spreadsheet.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    sheet_metadata = sheet.get(spreadsheetId=SAMPLE_SPREADSHEET_ID).execute()
    properties = sheet_metadata.get('sheets')
    sheets = [item.get('properties').get('title') for item in properties]
    data = []
    for i in sheets:
        try:
            data.append(read_table(sheet, SAMPLE_SPREADSHEET_ID, i))
        except:
            print(f"\nerror occurred on {i}\n")
    data = reformat(data)

except HttpError as err:
    print(err)
