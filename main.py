import os
import requests
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaInMemoryUpload

# BambooHR API credentials
BAMBOOHR_SUBDOMAIN = os.getenv('BAMBOOHR_SUBDOMAIN')
api_key = os.getenv('BAMBOOHR_API_KEY')
BAMBOOHR_API_KEY = base64.b64encode(f'{api_key}:x'.encode()).decode()

# Report ID
report_id = '319'  # Replace with the actual report ID

# Google Drive setup
SCOPES = ['https://www.googleapis.com/auth/drive.file']
SERVICE_ACCOUNT_FILE = 'path/to/your/service-account-file.json'

def fetch_bamboohr_report():
    url = f'https://api.bamboohr.com/api/gateway.php/{BAMBOOHR_SUBDOMAIN}/v1/reports/{report_id}?onlyCurrent=true'
    headers = {
        'Accept': 'text/csv',
        'Authorization': f'Basic {BAMBOOHR_API_KEY}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.content

def upload_to_google_drive(file_content, filename):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=credentials)

    file_metadata = {
        'name': filename,
        'mimeType': 'application/vnd.google-apps.spreadsheet'
    }
    media = MediaInMemoryUpload(file_content, mimetype='text/csv')
    file = service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    print(f'File ID: {file.get("id")}')

def main():
    csv_data = fetch_bamboohr_report()
    date_str = datetime.datetime.now().strftime('%Y-%m-%d')
    filename = f'BambooHR_Report_{date_str}.csv'
    upload_to_google_drive(csv_data, filename)

if __name__ == '__main__':
    main()
