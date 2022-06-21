#!/usr/bin/env python

import boto3
import os
import re 
import time
import click
import uuid


dx = boto3.client('dataexchange', region_name='us-east-1')
s3 = boto3.client('s3')


def get_all_revisions(data_set_id):

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


def get_all_assets(data_set_id, revision_id):
    assets = []
    res = dx.list_revision_assets(DataSetId=data_set_id,
                                  RevisionId=revision_id)
    next_token = res.get('NextToken')
    
    assets += res.get('Assets')
    while next_token:
        res = dx.list_revision_assets(DataSetId=data_set_id,
                                      RevisionId=revision_id,
                                      NextToken=next_token)
        assets += res.get('Assets')
        next_token = res.get('NextToken')
        
    return assets


def get_entitled_data_sets():
    data_sets = []
    res = dx.list_data_sets(Origin='ENTITLED')
    next_token = res.get('NextToken')
    
    data_sets += res.get('DataSets')
    while next_token:
        res = dx.list_data_sets(Origin='ENTITLED',
                                NextToken=next_token)
        data_sets += res.get('DataSets')
        next_token = res.get('NextToken')
        
    return data_sets


def export_assets(assets, bucket):
    
    asset_destinations = []

    for asset in assets:
        asset_destinations.append({
            "AssetId": asset.get('Id'),
            "Bucket": bucket,
            "Key": asset.get('Name')
        })

    job = dx.create_job(Type='EXPORT_ASSETS_TO_S3', Details={
        "ExportAssetsToS3": {
            "RevisionId": asset.get("RevisionId"), "DataSetId": asset.get("DataSetId"),
            "AssetDestinations": asset_destinations
        }
    })

    job_id = job.get('Id')
    dx.start_job(JobId=job_id)

    while True:
        job = dx.get_job(JobId=job_id)

        if job.get('State') == 'COMPLETED':
            break
        elif job.get('State') == 'ERROR':
            raise Exception("Job {} failed to complete - {}".format(
                job_id, job.get('Errors')[0].get('Message'))
            )

        time.sleep(1)


def to_url(s):
    s = re.sub(r"[^\w\s]", '', s)
    s = re.sub(r"\s+", '-', s)

    return s


def download_assets(assets, bucket, asset_dir):
    for asset in assets:
        asset_name = asset.get('Name')
        sub_dir = os.path.dirname(asset_name)
        full_dir = os.path.join(asset_dir, sub_dir)

        if not os.path.exists(full_dir):
            os.makedirs(full_dir)

        asset_file = os.path.join(full_dir, os.path.basename(asset_name))

        s3.download_file(bucket, asset_name, asset_file)

        print("Downloaded file {}".format(asset_file))


def make_s3_staging_bucket():
    bucket_name = str(uuid.uuid4())
    s3.create_bucket(Bucket=bucket_name)
    return bucket_name


def remove_s3_bucket(bucket_name):
    s3_resource = boto3.resource('s3')
    bucket = s3_resource.Bucket(bucket_name)
    bucket.objects.all().delete()
    bucket.delete()


@click.command()
@click.option('--s3-bucket', '-s')
def main(s3_bucket):

    if not s3_bucket:
        print("No s3 bucket provided, creating temporary staging bucket")
        temp_bucket = make_s3_staging_bucket()
        print("Created temporary bucket {}".format(temp_bucket))

    try:
        data_sets = get_entitled_data_sets()

        staging_bucket = s3_bucket or temp_bucket

        for ds in data_sets:
            print("Getting all Assets for Data set ### {} ###".format(ds.get('Name')))

            revisions = get_all_revisions(ds.get('Id'))
            for rev in revisions:
                assets = get_all_assets(ds.get('Id'), rev.get('Id'))

                destination_dir = os.path.join(to_url(ds.get('Name')), rev.get('Id'))

                export_assets(assets, staging_bucket)
                download_assets(assets, staging_bucket, destination_dir)

            print("---")
    finally:
        if temp_bucket:
            print("Removing temporary bucket {}".format(temp_bucket))
            remove_s3_bucket(temp_bucket)


if __name__ == '__main__':
    main()