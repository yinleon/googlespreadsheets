# -*- coding: utf-8 -*-
"""
This is a wrapper for the Google Sheets API to Pandas DataFrames

Author Leon Yin
"""

import httplib2
import os

from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools
import pandas as pd


__all__ = ['GoogleDrive']
__author__ = 'Leon Yin'

def _verify_credential(cred):
    if isinstance(cred, dict):
        return cred
    if os.path.exists(cred):
        return cred
    
    raise ValueError("{} is not a readable file".format(cred))

class GoogleSheets():
    '''
    A wrapper for the Google Sheets API to Pandas DataFrames.
    '''
    
    def __init__(self, client_secret, access_token, 
                 application_name = 'test',
                 api_version = 'v4', 
                 scopes = ['https://www.googleapis.com/auth/spreadsheets']):
        '''
        :input application_name: The name of the regiestered Google Cloud app
        :input clint_secret: the path to the client secret json file.
        :input access_token: the path to the access token json file. This is where it is written if it does not 
        exist.
        :input api_version: which version of the API shoule be formatted v{integer}. Defaults to "v4"
        :input scopes: A list of scopes needed for the API.
        '''
        # For the API
        self._SCOPES = scopes
        self._API_VERSION = api_version
        self._API_SERVICE_NAME = 'sheets'
        self._APPLICATION_NAME = application_name
        self._DISCOVERYURL= ('https://sheets.googleapis.com/$discovery/rest?'
                            'version={}'.format(api_version))
        
        self._CLIENT_SECRET_FILE = _verify_credential(client_secret)
        self._AUTHENTICATED_CRED = _verify_credential(access_token)
        self.credentials = self.get_credentials()

    
    def get_credentials(self):
        '''
        Gets valid user credentials from storage.

        If nothing has been stored, or if the stored credentials are invalid,
        the OAuth2 flow is completed to obtain the new credentials.

        Returns:
            Credentials, the obtained credential.
        '''
        # Where is the credential token stored?
        storage = oauth2client.file.Storage(self._AUTHENTICATED_CRED)
        credentials = storage.get()

        # Create or refresh the credential token is invalid.
        if credentials is None or credentials.invalid:

            flow = client.flow_from_clientsecrets(self._CLIENT_SECRET_FILE, self._SCOPES)
            flow.user_agent = self._APPLICATION_NAME
            credentials = tools.run_flow(flow, storage, flags=None)

            print('Storing credentials to ' + self._AUTHENTICATED_CRED)

        return credentials
    
    
    def get_sheet_id_from_url(self, url):
        '''
        Parses the sheet_id from a url of a Google Sheet.
        '''
        return url.split('/d/')[-1].split('/')[0]

    
    def list_tabs(self, sheet_id):
        '''
        Returns a list of sheet names (tabs) in a spreadsheet ID.
        The ID is here:
        `https://docs.google.com/spreadsheets/d/{HERE!!}`
        without any modifiers like /edit=0
        
        :input: the IF od a Google Sheet the user has access to.
        '''
        # Get Authenticated.
        credentials = self.credentials
        http = credentials.authorize(httplib2.Http())

        # Connect to the API.
        service = discovery.build(
            self._API_SERVICE_NAME, 
            self._API_VERSION, 
            http=http,
            discoveryServiceUrl=self._DISCOVERYURL
        )

        sheet_metadata = service.spreadsheets().get(spreadsheetId=sheet_id).execute()
        sheets = sheet_metadata.get('sheets', '')

        return [sheet.get("properties", {}).get("title", "Sheet1") for sheet in sheets]


    def read_sheet(self, sheet_id, tab, cell_range, dtype=None, 
                   index=None, dateTimeRenderOption=None, fillna=None):
        '''
        Gets a sheet to a pandas dataframe given 
        a sheet_id (string) of a google sheet, 
        tab (string) name and 
        cell_range (string ie A1:E) where data is located
        fillna is what null values are filled with.
        .

        Note that the first row in the range will be the columns of the dataframe.

        try it on this sample spreadsheet:
        https://docs.google.com/spreadsheets/d/1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms/edit

        with

        sheet_2_df(
            id=1BxiMVs0XRA5nFMdKvBdBZjgmUUqptlbs74OgvE2upms,
            sheet='Class Data',
            range='A1:F'
        )
        '''
        # Get Authenticated.
        credentials = self.credentials
        http = credentials.authorize(httplib2.Http())

        # Connect to the API.
        service = discovery.build(
            self._API_SERVICE_NAME, 
            self._API_VERSION, 
            http=http,
            discoveryServiceUrl=self._DISCOVERYURL
        )

        # Construct arguments
        rangeName = '{SHEET}!{RANGE}'.format(SHEET=tab,RANGE=cell_range)

        # Submit the arguments and retrieve results from Sheet
        result = service.spreadsheets().values().get(
            spreadsheetId=sheet_id, 
            range=rangeName,
            dateTimeRenderOption=dateTimeRenderOption
        ).execute()

        values = result.get('values', [])

        if not values:
            df = pd.DataFrame()

        else:
            columns = values[0]
            rows = []
            for row in values[1:]:
                if row:
                    if len(row) < len(columns):
                        diff = len(columns) - len(row)
                        for i in range(diff):
                            row += [ None ]
                        rows.append(row)
                    else:
                        rows.append(row)

            df = pd.DataFrame(
                data=rows,
                columns=columns,
                dtype=dtype,
                index=index
            )
        return df

    def to_sheet(self, df, sheet_id, tab, cell_range, valueInputOption='RAW'):
        '''
        Updates a sheet of a sheetid with 'values' (list of list)
        '''

        values = df.values.tolist()    

        credentials = self.credentials
        http = credentials.authorize(httplib2.Http())

        # Connect to the API.
        service = discovery.build(
            self._API_SERVICE_NAME, 
            self._API_VERSION, 
            http=http,
            discoveryServiceUrl=self._DISCOVERYURL
        )

        # Construct arguments
        rangeName = '{SHEET}!{RANGE}'.format(SHEET=tab,RANGE=cell_range)

        valueRange = {
            "range": rangeName,
            "majorDimension": "ROWS",
            "values": values
        }

        result = service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range = rangeName,
            valueInputOption=valueInputOption,
            body= valueRange      
        ).execute()

        return result
    