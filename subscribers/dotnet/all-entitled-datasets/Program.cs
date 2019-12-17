using System;
using System.Threading.Tasks;
using Amazon.DataExchange;
using Amazon.DataExchange.Model;

namespace AwsDataExchangeSample
{
  class Program
  {
    static void Main(string[] args)
    {
      AmazonDataExchangeClient client = new AmazonDataExchangeClient();

      ListDataSetsRequest listDataSetsRequest = new ListDataSetsRequest();
      listDataSetsRequest.Origin = "ENTITLED";

      Task<ListDataSetsResponse> dataSetsRequestTask = client.ListDataSetsAsync(listDataSetsRequest);
      dataSetsRequestTask.Wait();

      foreach (DataSetEntry dataSetEntry in dataSetsRequestTask.Result.DataSets)
      {
        Console.WriteLine("{0}/{1}: {2}\n  {3}",
            dataSetEntry.OriginDetails.ProductId,
            dataSetEntry.Id,
            dataSetEntry.Name,
            dataSetEntry.Description);
      }
    }
  }
}
