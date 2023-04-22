#!/usr/bin/python
#Reference: https://stackoverflow.com/questions/38511444/python-download-files-from-google-drive-using-url

import requests
import pandas as pd

def download_file_from_google_drive(id, destination):
    URL = "https://docs.google.com/uc?export=download"

    session = requests.Session()

    response = session.get(URL, params = { 'id' : id }, stream = True)
    token = get_confirm_token(response)

    if token:
        params = { 'id' : id, 'confirm' : token }
        response = session.get(URL, params = params, stream = True)

    save_response_content(response, destination)    

def get_confirm_token(response):
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            return value

    return None

def save_response_content(response, destination):
    CHUNK_SIZE = 32768

    with open(destination, "wb") as f:
        for chunk in response.iter_content(CHUNK_SIZE):
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)

def convert_xlsx_to_csv():
	read_file = pd.read_excel('pursuit.xlsx')
	read_file.to_csv('pursuit.csv', index=None, header=True)

if __name__ == "__main__":
    gid = open('spreadsheet_url.txt').readlines()[0]
    destination = 'pursuit.xlsx'
    download_file_from_google_drive(gid, destination)
    convert_xlsx_to_csv()