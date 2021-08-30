#!/usr/bin/env python

import boto3
import os
import re 
import time
import click
import uuid
import json
import botocore

dx = boto3.client('dataexchange')
s3 = boto3.client('s3')

#This function returns revision_ids corresponding to the data-set-id specified.
def get_revisions(data_set_id):
    
    #Paginate and extract all revisions corresponding to the data-set specified.
    revisions = []
    #print('Extracting revision-ids for data set',data_set_id)
    try:
        res = dx.list_data_set_revisions(DataSetId=data_set_id)
        next_token = res.get('NextToken')
        revisions += res.get('Revisions')
        while next_token:
            res = dx.list_data_set_revisions(DataSetId=data_set_id,
                                             NextToken=next_token)
            revisions += res.get('Revisions')
            next_token = res.get('NextToken')
    except dx.exceptions.ResourceNotFoundException as error:
        print('The data set does not belong to region specified.')
        exit()
    return revisions


#This function exports assets corresponding to revisions specified into an S3 bucket
def export_revisions(data_set_id,revisions,bucket,key_pattern):
    
    for i in range(0, len(revisions), 5):
        job_ids=[]
        
        #Trigger 5 concurrent export jobs at a time
        for revision in revisions[i:i + 5]:
            create_job_response = dx.create_job(
                    Details={
                        'ExportRevisionsToS3': {
                            "DataSetId": data_set_id,
                            'RevisionDestinations':[ {"RevisionId": revision['Id'], "Bucket": bucket, "KeyPattern": key_pattern}]
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


# This function accepts data_set-ids, region and an optional key-pattern and then exports the data into specified S3 bucket. The region of the S3 bucket and data_set must be same. 
@click.command()
@click.option('--bucket', '-s')
@click.option('--data-set-ids', '-s')
@click.option('--region', '-s')
@click.option('--key-pattern', '-s')
def main(bucket,data_set_ids,region,key_pattern):
    global dx,s3
    if not bucket:
        print("No s3 bucket provided")
    elif not data_set_ids:
        print("No data_set_ids provided")
    if not region:
        print("No region provided")
    else:
        #Override region for connections.
        if not key_pattern:
            key_pattern= "${Revision.Id}/${Asset.Name}" 
        dx = boto3.client('dataexchange', region_name=region)
        s3 = boto3.client('s3', region_name=region)
        print(s3.get_bucket_location(Bucket=bucket))
        location = s3.get_bucket_location(Bucket=bucket)['LocationConstraint']
        if location == None:
            location='us-east-1'

        if region != location.replace("'",""):
            print ('Data set region does not match bucket\'s region. Cross region exports incur additional charges and cross-region exports over 100GB might fail.')
            if input('Do You Want To Continue? (y/n) ') != 'y':
                print('Cancelling export.')
                exit()
        
        #loop through data_set_ids and extract
        for data_set_id in data_set_ids.split(","):
            revisions = get_revisions(data_set_id)
            print("Initiating export for data set {} ".format(data_set_id))
            export_revisions(data_set_id,revisions,bucket,key_pattern)
            print("Export for data set {} is complete".format(data_set_id))
        print("Export complete.")

          
if __name__ == '__main__':
    main()