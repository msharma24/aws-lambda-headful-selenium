import boto3
import logging
import os
import uuid


logger = logging.getLogger(name=__name__)
env_level = os.environ.get("LOG_LEVEL")
log_level = logging.INFO if not env_level else env_level
logger.setLevel(log_level)

def submit_batch_job(JOB_DEFINITION, JOB_QUEUE,JOB_NAME_UUID,ARGS):
    client = boto3.client('batch')
    response = client.submit_job (
            jobDefinition=JOB_DEFINITION,
            jobName =f"SELENIUM_{JOB_NAME_UUID}",
            jobQueue=JOB_QUEUE,
            containerOverrides={
                'environment': [
                    {
                    'name': 'ARGS',
                    'value': ARGS
                    }
                    ]
                   
                }

    )

    return response



def lambda_handler(event,context):
    JOB_DEFINITION=os.environ.get('JOB_DEFINITION')
    JOB_QUEUE=os.environ.get('JOB_QUEUE')
    JOB_NAME_UUID = uuid.uuid1()
    S3_BUCKET = os.environ.get('SOURCE_S3_BUCKET')


    S3_OBJECT_KEY = event['detail']['requestParameters']['key']
    print(S3_OBJECT_KEY)
    print(S3_OBJECT_KEY)
    FILE_PATH = f"/tmp/{S3_OBJECT_KEY.split('/')[0]}"

    s3 = boto3.client('s3')
    s3.download_file(S3_BUCKET,S3_OBJECT_KEY,FILE_PATH)

    with open(f'{FILE_PATH}', 'r') as file:
        ARGS = file.read().replace('\n', '')
    print(ARGS)

    response = submit_batch_job(JOB_DEFINITION, JOB_QUEUE,JOB_NAME_UUID, ARGS)
    print(f"Response from the submit_batch_job function {response}")
    logging.info(f"Submitted Batch Job with ID {response['jobId']}")
    
    
