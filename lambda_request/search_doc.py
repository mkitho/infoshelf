import requests
import logging
import boto3
from botocore.exceptions import ClientError
import os

def search_person(mcr_number):

    cookies = {
        '$Cookie: JSESSIONID': '2oK7OLshFCrATSCFDCn03WOTk0eqhYAl2VC4jMNumdulTCBOp6BQ\\u0021-1221308011\\u00211934151206',
        'Cookie': '\\u0021MU2PDkI7IM+89ApME8YqMNIUGDaB29sdi3x+i6o23+laSM6K3pSktYQ0mmfqw+Ot9E1EGDWC8JCi+A8=',
        'AMCVS_DF38E5285913269B0A495E5A%40AdobeOrg': '1',
        'JSESSIONID': '2oK7OLshFCrATSCFDCn03WOTk0eqhYAl2VC4jMNumdulTCBOp6BQ\\u0021-1221308011\\u00211934151206\\u00211630933662497',
        'AMCV_DF38E5285913269B0A495E5A%40AdobeOrg': '1075005958%7CMCIDTS%7C18877%7CMCMID%7C68291149979862947178044884406081312657%7CMCOPTOUT-1630940892s%7CNONE%7CvVersion%7C4.4.1',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'Origin': 'https://prs.moh.gov.sg',
        'Upgrade-Insecure-Requests': '1',
        'DNT': '1',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://prs.moh.gov.sg/prs/internet/profSearch/mgetSearchSummaryByName.action',
        'Accept-Language': 'en-US,en;q=0.9',
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
        ('selectType', 'all'),
        ('__checkbox_psearchParamVO.cbSpecialty', '0010'),
        ('__checkbox_psearchParamVO.cbSpecialty', '0500'),
        ('__checkbox_psearchParamVO.cbSpecialty', '0510'),
        ('__checkbox_psearchParamVO.cbSpecialty', '0900'),
        ('__checkbox_psearchParamVO.cbSpecialty', '5301'),
        ('__checkbox_psearchParamVO.cbSpecialty', '6000'),
        ('__checkbox_psearchParamVO.cbSpecialty', '1300'),
        ('__checkbox_psearchParamVO.cbSpecialty', '1800'),
        ('__checkbox_psearchParamVO.cbSpecialty', '5720'),
        ('__checkbox_psearchParamVO.cbSpecialty', '1820'),
        ('__checkbox_psearchParamVO.cbSpecialty', '2200'),
        ('__checkbox_psearchParamVO.cbSpecialty', '2210'),
        ('__checkbox_psearchParamVO.cbSpecialty', '2600'),
        ('__checkbox_psearchParamVO.cbSpecialty', '3510'),
        ('__checkbox_psearchParamVO.cbSpecialty', '4120'),
        ('__checkbox_psearchParamVO.cbSpecialty', '3820'),
        ('__checkbox_psearchParamVO.cbSpecialty', '3830'),
        ('__checkbox_psearchParamVO.cbSpecialty', '3840'),
        ('__checkbox_psearchParamVO.cbSpecialty', '4100'),
        ('__checkbox_psearchParamVO.cbSpecialty', '4110'),
        ('__checkbox_psearchParamVO.cbSpecialty', '4130'),
        ('__checkbox_psearchParamVO.cbSpecialty', '4140'),
        ('__checkbox_psearchParamVO.cbSpecialty', '4150'),
        ('__checkbox_psearchParamVO.cbSpecialty', '4600'),
        ('__checkbox_psearchParamVO.cbSpecialty', '4610'),
        ('__checkbox_psearchParamVO.cbSpecialty', '4620'),
        ('__checkbox_psearchParamVO.cbSpecialty', '4660'),
        ('__checkbox_psearchParamVO.cbSpecialty', '4670'),
        ('__checkbox_psearchParamVO.cbSpecialty', '4680'),
        ('__checkbox_psearchParamVO.cbSpecialty', '5302'),
        ('__checkbox_psearchParamVO.cbSpecialty', '5310'),
        ('__checkbox_psearchParamVO.cbSpecialty', '5320'),
        ('__checkbox_psearchParamVO.cbSpecialty', '5330'),
        ('__checkbox_psearchParamVO.cbSpecialty', '5340'),
        ('__checkbox_psearchParamVO.cbSpecialty', '6210'),
        ('__checkbox_psearchParamVO.cbSpecialty', 'SS03'),
        ('__checkbox_psearchParamVO.cbSpecialty', '2610'),
        ('__checkbox_psearchParamVO.cbSpecialty', '3810'),
        ('__checkbox_psearchParamVO.cbSpecialty', 'PC01'),
        ('__checkbox_psearchParamVO.cbSpecialty', 'PG01'),
        ('__checkbox_psearchParamVO.cbSpecialty', 'PHO01'),
        ('__checkbox_psearchParamVO.cbSpecialty', 'PIC01'),
        ('__checkbox_psearchParamVO.cbSpecialty', 'PN01'),
        ('__checkbox_psearchParamVO.cbSpecialty', 'S002'),
        ('__checkbox_psearchParamVO.cbSpecialty', '5710'),
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

    # # If S3 object_name was not specified, use file_name
    # if object_name is None:
    #     object_name = os.path.basename(file_name)

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        # response = s3_client.upload_file(file_name, bucket, object_name)
        response = s3_client.put_object(
            Body=string_content, 
            Bucket=bucket,
            Key=file_name
        )
    except ClientError as e:
        logging.error(e)
        return False
    return True