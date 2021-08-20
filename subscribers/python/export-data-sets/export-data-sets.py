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

#This function returns revision_ids corresponding to the data-set-id specified.
def get_revisions(data_set_id):
    
    #Paginate and extract all revisions corresponding to the data-set specified.
    revisions = []
    res = dx.list_data_set_revisions(DataSetId=data_set_id)
    next_token = res.get('NextToken')
    revisions += res.get('Revisions')
    while next_token:
        res = dx.list_data_set_revisions(DataSetId=data_set_id,
                                         NextToken=next_token)
        revisions += res.get('Revisions')
        next_token = res.get('NextToken')

    return revisions


#This function exports assets corresponding to revisions specified into an S3 bucket
def export_revisions(data_set_id,revisions,bucket):
    
    for i in range(0, len(revisions), 5):
        job_ids=[]
        
        #Trigger 5 concurrent export jobs at a time
        for revision in revisions[i:i + 5]:
            create_job_response = dx.create_job(
                    Details={
                        'ExportRevisionsToS3': {
                            "DataSetId": data_set_id,
                            'RevisionDestinations':[ {"RevisionId": revision['Id'], "Bucket": bucket, "KeyPattern": "${Asset.Name}" }]
                    }},Type='EXPORT_REVISIONS_TO_S3'
            )

            job_id=create_job_response['Id']
            job_ids.append(job_id)
            
            #Initiate the job
            print("=> Starting Job: ",job_id, "for revision: ",revision['Id'])
            dx.start_job(JobId=job_id)

        #Wait for all import jobs to finish
        for job in job_ids:
            max_time = time.time() + 60*60 # 1 hour
            #print(job)
            while time.time() < max_time :
                response = dx.get_job(JobId=job_id);
                status = response['State']
                print('STATUS: ',job,'get_job_status'+": {}".format(status))
                if status == "COMPLETED":
                    break
                elif status == "ERROR":
                    print(response)
                    print("Export failed")
                    exit()
                time.sleep(5)
        time.sleep(15)


# This function accepts data_set-ids and region and exports the data into specified S3 bucket. The region of the S3 bucket and data_set must be same.
@click.command()
@click.option('--bucket', '-s')
@click.option('--data-set-ids', '-s')
@click.option('--region', '-s')
def main(bucket,data_set_ids,region):
    global dx,s3
    if not bucket:
        print("No s3 bucket provided")
    elif not data_set_ids:
        print("No data_set_ids provided")
    if not region:
        print("No region provided")
    else:
        #Override region for connections.
        
        dx = boto3.client('dataexchange', region_name=region)
        s3 = boto3.client('s3',region_name=region)
        
        #loop through data_set_ids and extract
        for data_set_id in data_set_ids.split(","):
            print("Extracting revisions for Data set ### {} ###".format(data_set_id))
            revisions = get_revisions(data_set_id)
            export_revisions(data_set_id,revisions,bucket)
    print("Export complete.")
          
if __name__ == '__main__':
    main()