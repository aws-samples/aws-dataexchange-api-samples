import os
os.environ['AWS_DATA_PATH'] = '/opt/'

from itertools import islice
import boto3
from datetime import datetime
import time
import json

region = os.environ['AWS_REGION']
destination_bucket = os.environ['S3_BUCKET']

if not destination_bucket:
    raise Exception("'S3_BUCKET' environment variable must be defined!")

# Grouper recipe from standard docs: https://docs.python.org/3/library/itertools.html
def grouper(iterable, n):
    iterator = iter(iterable)
    group = tuple(islice(iterator, n))
    while group:
        yield group
        group = tuple(islice(iterator, n))

def handler(event, context):
    dataexchange = boto3.client(
        service_name='dataexchange',
        region_name=region
    )
    s3 = boto3.client(
        service_name='s3',
        region_name=region
    )
    #If the request is from Terraform get the RevisionID, for first revision
    if 'InitialInit' in event:
        data_set_id = event['InitialInit']['data_set_id']
        revision_ids = [event['InitialInit']['RevisionIds']]
        print ("Initial revision retrieval")
        print (event)
    else:
        data_set_id = event['resources'][0]
        revision_ids = event['detail']['RevisionIds']
        print ("Triggered revision retrieval")
        print (event)
    # Used to store the Ids of the Jobs exporting the assets to S3.
    job_ids = set()
    
    for revision_id in revision_ids:
        # Start Jobs to export all the assets to S3.
        # We export in batches of 100 as the StartJob API has a limit of 100.
        revision_assets = dataexchange.list_revision_assets(DataSetId=data_set_id, RevisionId=revision_id)
        assets_chunks = grouper(revision_assets['Assets'], 100)
        for assets_chunk in assets_chunks:
            # Create the Job which exports assets to S3.
            export_job = dataexchange.create_job(
                Type='EXPORT_ASSETS_TO_S3',
                Details={
                    'ExportAssetsToS3': {
                        'DataSetId': data_set_id,
                        'RevisionId': revision_id,
                        'AssetDestinations': [
                            { 'AssetId': asset['Id'], 'Bucket': destination_bucket } for asset in assets_chunk
                        ]
                    }
                }    
            )
            # Start the Job and save the JobId.
            dataexchange.start_job(JobId=export_job['Id'])
            job_ids.add(export_job['Id'])
    
    # Iterate until all remaining workflow have reached a terminal state, or an error is found.
    completed_jobs = set()
    while job_ids != completed_jobs:
        for job_id in job_ids:
            if job_id in completed_jobs:
                continue
            get_job_response = dataexchange.get_job(JobId=job_id)
            if get_job_response['State'] == 'COMPLETED':
                print ("Job {} completed".format(job_id))
                completed_jobs.add(job_id)
            if get_job_response['State'] == 'ERROR':
                job_errors = get_job_response['Errors']
                raise Exception('JobId: {} failed with errors:\n{}'.format(job_id, job_errors))
            # Sleep to ensure we don't get throttled by the GetJob API.
            time.sleep(0.2)
    return {
        'statusCode': 200,
        'body': json.dumps('All jobs completed.')
    }