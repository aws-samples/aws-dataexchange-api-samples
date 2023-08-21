#!/usr/bin/env python
import boto3
import click
import time


def create_data_set(dataexchange, data_set_name):
    data_set_creation_response = dataexchange.create_data_set(
        AssetType='REDSHIFT_DATA_SHARE',
        Name=data_set_name,
        Description='Redshift DataShare data set'
    )
    return data_set_creation_response['Id']


def add_shares(dataexchange, data_set_id, revision_id, datashare_arn):
    create_job_details = {
        'ImportAssetsFromRedshiftDataShares': {
            'AssetSources': [
                {
                    'DataShareArn': datashare_arn
                },
            ],
            'DataSetId': data_set_id,
            'RevisionId': revision_id
        }
    }

    create_job_response = dataexchange.create_job(
        Details=create_job_details,
        Type='IMPORT_ASSETS_FROM_REDSHIFT_DATA_SHARES'
    )

    job_id = create_job_response['Id']
    job_state = create_job_response['State']

    if job_state == 'ERROR':
        raise click.ClickException(f'Data set creation failed with status {job_state}!')

    return job_id


def wait_for_job_to_complete(dataexchange, job_id):
    dataexchange.start_job(JobId=job_id)

    while True:
        job_status_response = dataexchange.get_job(JobId=job_id)
        job_state = job_status_response['State']

        if job_state in ['ABORTED', 'FAILED', 'ERROR']:
            print(job_status_response)
            raise click.ClickException(f'Data set creation failed with status {job_state}!')
        if job_state == 'COMPLETED':
            return

        click.echo(f'Still waiting for job {job_id} to finish.')
        time.sleep(5)


@click.command()
@click.option('--data-set-name', required=True, help='Name of the AWS Data Exchange data set to create.')
@click.option('--datashare-arn', required=True,
              help='Amazon Redshift Datashare ARN that contains data to share.')
@click.option('--data-set-id',
              help='If supplied, the data set ID to which the datashare will be added. Existing datashares will be replaced.')
@click.option('--region', default='us-east-1',
              help='AWS Region of the Amazon Redshift Datashare , and where the data set will be. Default value is us-east-1')
def main(data_set_name, data_set_id, region, datashare_arn):

    dataexchange = boto3.client('dataexchange', region_name=region)

    data_set_id_to_use = create_data_set(dataexchange, data_set_name) if data_set_id is None else data_set_id

    create_revision_response = dataexchange.create_revision(DataSetId=data_set_id_to_use)
    revision_id = create_revision_response['Id']

    job_id = add_shares(dataexchange, data_set_id_to_use, revision_id, datashare_arn)
    wait_for_job_to_complete(dataexchange, job_id)
    finalize_revision_response = dataexchange.update_revision(DataSetId=data_set_id_to_use, RevisionId=revision_id,
                                                              Finalized=True)

    click.echo(f'Data set {data_set_id_to_use} configured with Amazon Redshift Datashare.')


if __name__ == '__main__':
    main()
