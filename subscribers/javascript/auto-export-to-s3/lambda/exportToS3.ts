import { Context, Callback, Handler, ScheduledEvent } from 'aws-lambda';
import { DataExchange } from 'aws-sdk';
import Logger from 'bunyan';

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

  // Export each new Revision to S3.
  for (const revisionId of (event.detail as IDataExchangeDetailType).RevisionIds) {
    const job = await dataExchangeClient.createJob({
      Type: 'EXPORT_REVISIONS_TO_S3',
      Details: {
        ExportRevisionsToS3: {
          DataSetId: dataSetId,
          RevisionDestinations: [
            {
              RevisionId: revisionId,
              Bucket: s3Bucket,
              KeyPattern: `${dataSetId}/\${Revision.Id}/\${Asset.Name}`
            }
          ]
        }
      }
    }).promise();

    await dataExchangeClient.startJob({ JobId: job.Id }).promise();

    const completedJob = await waitForJobCompletion(job.Id, dataExchangeClient);
    logger.info({ completedJob });
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

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}
