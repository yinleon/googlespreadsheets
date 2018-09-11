# Google Spreadsheets
This is a super lightweight wrapper around the Google Sheets API.<br>
It allows users to easily read and write sheets to and from [Pandas](http://pandas.pydata.org/) DataFrames.

This is made public and hosted on PyPi for selfish reasons.

## Installation
`pip install googlespreadsheets`

## API Credentials
The Google Sheets API uses [OAuth2](https://developers.google.com/identity/protocols/OAuth2)
You can get credentials on the Google Cloud API console.

Create a project and go to the Credentials for your project and create New credentials > OAuth client ID > of type Other. In the list of your OAuth 2.0 client IDs click Download JSON for the Client ID you just created. Save the file as client_secrets.json somewhere safe!

From the client_secrets, we can create an access token.
You'll be prompted through this creation in your browser when you instantiate the `GoogleSheets` class for the first time.

This step is easier to do locally in a Python terminal (rather than a Jupyter Notebook or a remote server)!

## Quickstart
```
from googlespreadsheets import GoogleSheets

# initiate a API wrapper using the path to json credentials
goog = GoogleSheets(client_secret=CLIENT_SECRET_FILE, 
                    access_token=AUTHENTICATED_CRED)
                    
googl.list_tabs()

# read a sheet into a Pandas dataframe
df = goog.read_sheet(sheet_id='1kXKWc9p_ZE',
                     tab='Sheet1', 
                     cell_range='A1:E')

# write a Pandas dataframe to a sheet
goog.to_sheet(df, sheet_id='1kXKWc9p_ZE', tab='Sheet2')
```

More details are available in this [Jupyter Notebook](http://nbviewer.jupyter.org/github/yinleon/googlespreadsheets/blob/master/examples/quickstart.ipynb?flush_cache=true)

## Documentation
TBD

## Liscence
MIT

## Author
By Leon Yin
