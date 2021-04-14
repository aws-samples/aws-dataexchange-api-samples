import { DataExchange, DataSetEntry } from '@aws-sdk/client-dataexchange'

const dataexchange = new DataExchange({
  region: process.env.AWS_REGION || 'us-east-1',
  credentials: {
    accessKeyId: process.env.AWS_ACCESS_KEY_ID,
    secretAccessKey: process.env.AWS_SECRET_ACCESS_KEY,
    sessionToken: process.env.AWS_SESSION_TOKEN
  }
});

void async function () {
  const entitledDataSets = await dataexchange.listDataSets({ Origin: 'ENTITLED' });

  entitledDataSets.DataSets.forEach((dataSet: DataSetEntry) => {
    console.log(`${dataSet.OriginDetails.ProductId}/${dataSet.Id}: ${dataSet.Name}\n ${dataSet.Description}`);
  });
}();
