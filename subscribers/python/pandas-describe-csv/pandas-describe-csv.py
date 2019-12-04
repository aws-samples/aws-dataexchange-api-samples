#!/usr/bin/env python

import click
import boto3
import os
import re 
import time
import tempfile
import uuid
import pandas


dx = boto3.client('dataexchange', region_name='us-east-1')
s3 = boto3.client('s3')


class TemporaryS3Bucket(object):
    def __init__(self):
        bucket_name = str(uuid.uuid4())

        self.bucket_name = bucket_name
        self.s3 = boto3.resource('s3') 

        self.s3.create_bucket(Bucket=bucket_name)

    def __enter__(self):
        return self.bucket_name

    def __exit__(self, type, value, traceback):
        bucket = self.s3.Bucket(self.bucket_name)
        bucket.objects.all().delete()
        bucket.delete()


def export_asset(asset, bucket):
    asset_id = asset.get('Id')

    job = dx.create_job(Type='EXPORT_ASSETS_TO_S3', Details={
        "ExportAssetsToS3": {
            "RevisionId": asset.get("RevisionId"), "DataSetId": asset.get("DataSetId"),
            "AssetDestinations": [{
                "AssetId": asset_id,
                "Bucket": bucket,
                "Key": asset_id
            }]
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


def urlify(s):
    s = re.sub(r"[^\w\s]", '', s)
    s = re.sub(r"\s+", '-', s)

    return s


def parse_asset_arn(arn):
    groups = re.match('.*data-sets/(.*)/revisions/(.*)/assets/(.*)$', arn)

    return {
        "DataSetId": groups[1],
        "RevisionId": groups[2],
        "Id": groups[3]
    }


def dx_csv_to_data_frame(asset):
    with TemporaryS3Bucket() as bucket:
        export_asset(asset, bucket)
        with tempfile.TemporaryDirectory() as temp_dir:
            asset_id = asset.get('Id')
            dest = os.path.join(temp_dir, asset_id)
            s3.download_file(bucket, asset_id, dest)

            return pandas.read_csv(dest)


@click.command()
@click.argument('arn')
def cli(arn):
    asset = parse_asset_arn(arn)
    df = dx_csv_to_data_frame(asset)
    print(df.describe())


if __name__ == '__main__':
    cli()
