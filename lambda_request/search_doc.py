import requests
import logging
import boto3
from botocore.exceptions import ClientError
import os

def search_person(mcr_number):

    headers = {
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'Origin': 'https://prs.moh.gov.sg',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    data = [
        ('hpe', 'SMC'),
        ('regNo', mcr_number),
        ('psearchParamVO.language', 'eng'),
        ('psearchParamVO.searchBy', 'N'),
        ('psearchParamVO.name', ''),
        ('psearchParamVO.pracPlaceName', ''),
        ('psearchParamVO.rbtnRegister', 'all'),
        ('psearchParamVO.regNo', mcr_number),
        ('selectType', 'all')
    ]


    response = requests.post(
                'https://prs.moh.gov.sg/prs/internet/profSearch/mgetSearchDetails.action', 
                headers=headers, 
                # cookies=cookies, 
                data=data
            )

    return response


def upload_file(file_name, bucket, string_content):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """



    # Upload the file
    s3_client = boto3.client('s3')
    try:

        response = s3_client.put_object(
            Body=string_content, 
            Bucket=bucket,
            Key=file_name
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True