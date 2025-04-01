import requests
import os
import pandas as pd
from io import BytesIO
import json
from dotenv import load_dotenv
from mongodb import MongoDBClient

# Load environment variables from .env file
load_dotenv()

class SharePointClient:
    def __init__(self):
        self.tenant_id = os.getenv("TENANT_ID")
        self.client_id = os.getenv("CLIENT_ID")
        self.client_secret = os.getenv("CLIENT_SECRET")
        self.resource_url = os.getenv("RESOURCE")
        self.base_url = f"https://login.microsoftonline.com/{self.tenant_id}/oauth2/v2.0/token"
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.access_token = self.get_access_token()

    def get_access_token(self):
        body = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'scope': f'{self.resource_url}.default'
        }
        response = requests.post(self.base_url, headers=self.headers, data=body)
        response.raise_for_status()
        return response.json().get('access_token')

    def get_site_id(self, site_url):
        full_url = f'https://graph.microsoft.com/v1.0/sites/{site_url}'
        response = requests.get(full_url, headers={'Authorization': f'Bearer {self.access_token}'})
        response.raise_for_status()
        return response.json().get('id')

    def get_drive_id(self, site_id):
        drives_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives'
        response = requests.get(drives_url, headers={'Authorization': f'Bearer {self.access_token}'})
        response.raise_for_status()
        return [(drive['id'], drive['name']) for drive in response.json().get('value', [])]

    def download_file(self, file_url, file_name):
        response = requests.get(file_url, headers={'Authorization': f'Bearer {self.access_token}'})
        response.raise_for_status()
        if file_name.endswith('Screening Valeurs - VIXIS.xlsx'):
            df = pd.read_excel(BytesIO(response.content), usecols="A:S")
            self.transform(df)

    def download_folder_contents(self, site_id, drive_id, folder_id):
        folder_url = f'https://graph.microsoft.com/v1.0/sites/{site_id}/drives/{drive_id}/items/{folder_id}/children'
        response = requests.get(folder_url, headers={'Authorization': f'Bearer {self.access_token}'})
        response.raise_for_status()
        for item in response.json().get('value', []):
            if 'folder' in item:
                self.download_folder_contents(site_id, drive_id, item['id'])
            elif 'file' in item:
                file_url = item['@microsoft.graph.downloadUrl']
                if item['name'].endswith('Screening Valeurs - VIXIS.xlsx'):
                    self.download_file(file_url, item['name'])

    def round_numeric_values(x):
        numeric_value = pd.to_numeric(x, errors='coerce')  # Convert to number if possible
        if pd.notna(numeric_value):  # Check if it's a valid number
            return round(numeric_value, 2)  # Round if it's a number
        return x 
    
    def transform(self, df):
        df.columns = df.iloc[0]  # Assign first row as column names
        df = df[1:].reset_index(drop=True)  # Remove first row from data
        df = df.applymap(lambda x: round(float(x), 2) if str(x).replace('.', '', 1).isdigit() else x)
        json_data = df.to_dict(orient="records")
        json_output = json.dumps(json_data, indent=4)
        mongo_client = MongoDBClient(mongo_url=os.getenv('MONGO_URL'), db_name=os.getenv('DB_NAME'))
        mongo_client.update_collection('stock', json_data)

    def load_data(self):
        site_url = os.getenv("SITE_URL")
        site_id = self.get_site_id(site_url)

        drive_id = os.getenv("DRIVE_ID")
        folder_id = os.getenv("FOLDER_ID")
        self.download_folder_contents(site_id, drive_id, folder_id)


