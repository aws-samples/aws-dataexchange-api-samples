#!/usr/bin/env python

import boto3
import os
import re 
import time
import click
import uuid
import json

dx = boto3.client('dataexchange')
s3 = boto3.client('s3')

#This function returns revision_ids corresponding to the dataset-id specified.
def get_revision_ids(data_set_id):
    
    #Paginate and extract all revisions corresponding to the dataset specified.
    revisions = []
    res = dx.list_data_set_revisions(DataSetId=data_set_id)
    next_token = res.get('NextToken')
    revisions += res.get('Revisions')
    while next_token:
        res = dx.list_data_set_revisions(DataSetId=data_set_id,
                                         NextToken=next_token)
        revisions += res.get('Revisions')
        next_token = res.get('NextToken')

    #Extract IDs corresponding to the revision
    revision_ids = []
    for rev in revisions:
        revision_ids.append(rev['Id'])
    #print(revision_ids)
    return revision_ids


#This function exports assets corresponding to revision-ids specified into an S3 bucket
def export_revisions(dataset_id,revision_ids,bucket):
    
    for i in range(0, len(revision_ids), 5):
        job_ids=[]
        #Trigger 5 concurrent export jobs at a time
        for revision in revision_ids[i:i + 5]:
            create_job_response = dx.create_job(
                    Details={
                        'ExportRevisionsToS3': {
                            "DataSetId": dataset_id,
                            'RevisionDestinations':[ {"RevisionId": revision, "Bucket": bucket, "KeyPattern": "${Asset.Name}" }]
                    }},Type='EXPORT_REVISIONS_TO_S3'
            )

            job_id=create_job_response['Id']
            job_ids.append(job_id)
            
            #Initiate the job
            print("=> Starting Job: ",job_id, "for revision: ",revision)
            dx.start_job(JobId=job_id)


            
        #Wait for all import jobs to finish
        for job in job_ids:
            max_time = time.time() + 60*60 # 1 hour
            #print(job)
            while time.time() < max_time :
                response = dx.get_job(JobId=job_id);
                status = response['State']
                print('STATUS: ',job,'get_job_status'+": {}".format(status))
                if status == "COMPLETED" or status == "ERROR":
                    break
                time.sleep(5)
        time.sleep(15)


# This function accepts dataset-ids and region and exports the data into specified S3 bucket. The region of the S3 bucket and dataset must be same.
@click.command()
@click.option('--bucket', '-s')
@click.option('--dataset-ids', '-s')
@click.option('--region', '-s')
def main(bucket,dataset_ids,region):
    global dx,s3
    if not bucket:
        print("No s3 bucket provided")
    elif not dataset_ids:
        print("No dataset_ids provided")
    if not region:
        print("No region provided")
    else:
        #Override region for connections.
        
        dx = boto3.client('dataexchange', region_name=region)
        s3 = boto3.client('s3',region_name=region)
        
        #loop through datasetids and extract
        for dataset_id in dataset_ids.split(","):
            print("Extracting revisions for Data set ### {} ###".format(dataset_id))
            revision_ids = get_revision_ids(dataset_id)
            export_revisions(dataset_id,revision_ids,bucket)
    print("Export complete.")
          
if __name__ == '__main__':
    main()