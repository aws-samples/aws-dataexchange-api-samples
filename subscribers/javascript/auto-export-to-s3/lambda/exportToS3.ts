import { Context, Callback, Handler, ScheduledEvent } from 'aws-lambda';
import { DataExchange } from 'aws-sdk';
import * as Logger from 'bunyan';

// https://aws.amazon.com/blogs/big-data/find-and-acquire-new-data-sets-and-retrieve-new-updates-automatically-using-aws-data-exchange/
interface IDataExchangeDetailType {
  RevisionIds: string[];
}

const logger = Logger.createLogger({
  name: 'AutoExportToS3Lamdba'
});

export const handler: Handler<ScheduledEvent> = async function (event: ScheduledEvent, context: Context, callback: Callback) {
  logger.info({ event }, 'Event passed to AWS Lambda.');

  const s3Bucket = process.env.S3_BUCKET;
  const dataExchangeClient = new DataExchange({
    logger: console
  });

  // The Resources block contains a single entry which is the DataSetId which contains the RevisionIds.
  const dataSetId = event.resources[0];

  // For each new Revision, list and export all Assets to S3.
  for (const revisionId of (event.detail as IDataExchangeDetailType).RevisionIds) {
    let nextToken;

    do {
      const assetsInRevision = await dataExchangeClient.listRevisionAssets({
        DataSetId: dataSetId,
        RevisionId: revisionId,
        NextToken: nextToken,
        MaxResults: 100 // Jobs can currently only import 100 Assets at a time.
      }).promise();

      if (assetsInRevision.Assets.length < 1) {
        break;
      }
  
      const job = await dataExchangeClient.createJob({
        Type: 'EXPORT_ASSETS_TO_S3',
        Details: {
          ExportAssetsToS3: {
            DataSetId: dataSetId,
            RevisionId: revisionId,
            AssetDestinations: assetsInRevision.Assets.map((asset: DataExchange.AssetEntry) => ({
              AssetId: asset.Id,
              Bucket: s3Bucket,
              Key: `${dataSetId}/${revisionId}/${asset.Name}`
            }))
          }
        }
      }).promise();

      await dataExchangeClient.startJob({ JobId: job.Id }).promise();

      const completedJob = await waitForJobCompletion(job.Id, dataExchangeClient);
      logger.info({ completedJob });
    } while (nextToken !== undefined);
  }
};

async function waitForJobCompletion(jobId: string, dataExchangeClient: DataExchange): Promise<DataExchange.GetJobResponse> {
  let job: DataExchange.GetJobResponse;

  do {
    job = await dataExchangeClient.getJob({ JobId: jobId }).promise();

    await sleep(5000);
  } while (job.State === 'WAITING' || job.State === 'IN_PROGRESS');

  if (job.State === 'ERROR') {
    logger.error({ erroredJob: job }, 'Job encountered an error.');
  }

  return job;
}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}
