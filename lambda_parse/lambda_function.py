import json
import boto3 
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import base64
from botocore.exceptions import ClientError


def extract_texts(html_file):
    soup = BeautifulSoup(html_file, features="html.parser")
    texts = soup.find_all(text=True)
    return texts

def get_secret():

    secret_name = "opensearch_credentials"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    # In this sample we only handle the specific exceptions for the 'GetSecretValue' API.
    # See https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
    # We rethrow the exception by default.

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return json.loads(secret)
            
            
def extract_practice_info(clinician_html, mcr):
    '''
    extract primary/secondary practice places
    '''
    profile = {}
    profile['mcr'] = mcr
    result = extract_texts(clinician_html)
    
    try:
        full_name = [r for r in result if mcr in r]
        profile['full_name'] = full_name[0][:-10]
    except:
        full_name = 'error'

    try:
        spec_patterns = [
            'Specialty / Entry date into the Register of Specialists', 
            'Sub-Specialty / Entry date into the Register of Specialists'
        ]
        specialty = [result[i+1] for i, s in enumerate(result) if s in spec_patterns]
        specialty = specialty[0].strip()

        primary_hci = [result[i+4] for i, s in enumerate(result) if s=='Primary Place of Practice']
        profile['specialty'] = specialty
        profile['primary'] = primary_hci[0].strip()
    except:
        pass
    
    if 'Secondary Place of Practice' not in result:
        pass 
    else:
        try:
            secondary_hcis = [result[i+4] for i, s in enumerate(result) if s=='Secondary Place of Practice']
            profile['secondary'] = [r.strip() for r in secondary_hcis]
        except:
            # raise Exception()
            pass
    return profile 

def get_from_s3(mcr):
    s3 = boto3.client('s3')
    folder_prefix = datetime.today().strftime('%y%m%d')
    filename = f'{folder_prefix}/{mcr}.html'
    html_object = s3.get_object(Bucket='doctor-profiles', Key=filename)
    html_text = html_object['Body'].read().decode('utf-8')
    profile = extract_practice_info(html_text, mcr)
    return profile


def upload_elasticsearch(doc_profile, mcr):
    now = datetime.now()
    doc_profile['updated_datetime'] = now.strftime("%d/%m/%Y, %H:%M:%S")
    secret = get_secret()
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(doc_profile)
    es_endpoint = 'https://search-mohdocs-2iniqjm32dbswnucm6tes3y4sm.ap-southeast-1.es.amazonaws.com/doctors/_doc/' 
    document_index = es_endpoint + mcr + '_' + now.strftime('%y%m%d')
    response = requests.put(document_index, 
                            headers=headers, 
                            data=data, 
                            auth=(secret['opensearch_user'], secret['opensearch_pw']))
    return None

def lambda_handler(event, context):
    mcr = event['mcr']
    doc_profile = get_from_s3(mcr)
    upload_elasticsearch(doc_profile, mcr)
    return {
        'statusCode': 200,
        'body': f'Successfully added {mcr} to search engine!'
    }

