import json
from search_doc import *
from datetime import datetime
import requests

def lambda_handler(event, context):

    mcr = event['mcr']

    response = search_person(mcr)
    if response:
        folder_prefix = datetime.today().strftime('%y%m%d')
        filename = f'{folder_prefix}/{mcr}.html'
        upload_file(filename, 'doctor-profiles', response.text)

    else:
        print('error')

    return {
        'statusCode': 200,
        'body': f'Successfully found {mcr}!',
        'mcr': f'{mcr}'
    }
   
