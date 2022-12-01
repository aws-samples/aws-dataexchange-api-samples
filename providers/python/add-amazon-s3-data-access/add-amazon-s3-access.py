#!/usr/bin/env python
import boto3
import click
import time

def create_data_set(dataexchange, data_set_name):
    data_set_creation_response = dataexchange.create_data_set(
        AssetType='S3_DATA_ACCESS',
        Name=data_set_name,
        Description='S3 Data Access data set'
    )
    return data_set_creation_response['Id']

def add_shares(dataexchange, data_set_id, revision_id, bucket, prefix, key):
    # Ensure that all prefixes end with a trailing slash; otherwise, these would not be resolved by Amazon S3
    def format_prefix(p):
        if p.endswith('/'):
            return p            
        return p + '/'

    prefixes = list(map(format_prefix, prefix))

    create_job_response = dataexchange.create_job(
        Details={
            'CreateS3DataAccessFromS3Bucket': {
                'AssetSource': {
                    'Bucket': bucket,
                    'KeyPrefixes': prefixes,
                    'Keys': key
                },
                'DataSetId': data_set_id,
                'RevisionId': revision_id
            }
        },
        Type='CREATE_S3_DATA_ACCESS_FROM_S3_BUCKET'
    )

    job_id = create_job_response['Id']
    job_state = create_job_response['State']

    if (job_state == 'ERROR'):
        raise click.ClickException(f'Data set creation failed with status {job_state}!')

    return job_id

def wait_for_job_to_complete(dataexchange, job_id):
    dataexchange.start_job(JobId=job_id)

    while True:
        job_status_response = dataexchange.get_job(JobId=job_id)
        job_state = job_status_response['State']

        if job_state in ['ABORTED', 'FAILED']:
            raise click.ClickException(f'Data set creation failed with status {job_state}!')
        if job_state == 'COMPLETED':
            return

        click.echo(f'Still waiting for job {job_id} to finish.')
        time.sleep(5)
    

@click.command()
@click.option('--data-set-name', required=True, help='Name of the AWS Data Exchange data set to create.')
@click.option('--bucket', required=True, help='Name of the Amazon S3 bucket that contains the prefixes and keys to share.')
@click.option('--data-set-id', help='If supplied, the data set ID to which the data access will be added. Existing access will be replaced.')
@click.option('--region', default='us-east-1', help='AWS Region of the Amazon S3 bucket, and where the data set will be.')
@click.option('--prefix', default=[], help='Prefix of an Amazon S3 location to share. Multiple values permitted.', multiple=True)
@click.option('--key', default=[], help='Key of an Amazon S3 object to share. Multiple values permitted.', multiple=True)
def main(data_set_name, bucket, data_set_id, region, prefix, key):
    if (len(prefix) + len(key)) > 5:
        raise click.UsageError('No more than a total of 5 prefixes and keys can be provided.')

    dataexchange = boto3.client('dataexchange', region_name=region)

    data_set_id_to_use = create_data_set(dataexchange, data_set_name) if data_set_id is None else data_set_id

    create_revision_response = dataexchange.create_revision(DataSetId=data_set_id_to_use)
    revision_id = create_revision_response['Id']

    job_id = add_shares(dataexchange, data_set_id_to_use, revision_id, bucket, prefix, key)
    wait_for_job_to_complete(dataexchange, job_id)
    finalize_revision_response = dataexchange.update_revision(DataSetId=data_set_id_to_use, RevisionId=revision_id, Finalized=True)

    click.echo(f'Data set {data_set_id_to_use} configured with Amazon S3 data access.')

if __name__ == '__main__':
    main()
