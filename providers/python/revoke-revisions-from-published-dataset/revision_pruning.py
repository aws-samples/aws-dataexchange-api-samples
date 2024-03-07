#!/usr/bin/env python
import datetime
from pprint import pprint
import boto3
import click


@click.command()
@click.option('--data-set-id', help='dataset ID which needs to be pruned.')
@click.option('--revision-id', help='revision ID which needs to be revoked and all underlying assets deleted.')
@click.option('--region', default='us-east-1', help='AWS Region of the dataset.')
def main(data_set_id, revision_id, region):
    client = boto3.client('dataexchange', region_name=region)
    assets = client.list_revision_assets(
        DataSetId=data_set_id,
        RevisionId=revision_id
    )
    asset_ids = [d['Id'] for d in assets['Assets']]
    asset_names = [d['Name'] for d in assets['Assets']]
    print("Name of Assets that will be deleted once the revision is revoked: ")
    pprint(asset_names)
    # revoke the revision
    revoke_response = client.revoke_revision(
        DataSetId=data_set_id,
        RevisionId=revision_id,
        RevocationComment='revoking on ' + str(datetime.datetime.now())
    )
    pprint('revoke status of revision ' + revoke_response['Id'] + ' is ' + str(revoke_response['Revoked']))
    # delete all underlying assets
    for asset_id in asset_ids:
        client.delete_asset(
            AssetId=asset_id,
            DataSetId=data_set_id,
            RevisionId=revision_id
        )


if __name__ == '__main__':
    main()
