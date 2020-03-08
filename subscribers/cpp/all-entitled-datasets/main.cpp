#include <iostream>
#include <aws/core/Aws.h>
#include <aws/core/utils/Outcome.h>
#include <aws/dataexchange/DataExchangeClient.h>
#include <aws/dataexchange/model/ListDataSetsRequest.h>

int main(int argc, char** argv)
{
    Aws::SDKOptions options;
    Aws::InitAPI(options);

    {
        Aws::DataExchange::DataExchangeClient client;

        Aws::DataExchange::Model::ListDataSetsRequest list_data_sets_options;
        list_data_sets_options.SetOrigin("ENTITLED");

        auto outcome = client.ListDataSets(list_data_sets_options);

        if (outcome.IsSuccess()) {
            Aws::Vector<Aws::DataExchange::Model::DataSetEntry> data_sets_list = outcome.GetResult().GetDataSets();

            for (auto const &data_set: data_sets_list) {
                std::cout 
                    << data_set.GetOriginDetails().GetProductId() << "/"
                    << data_set.GetId() << ": "
                    << data_set.GetName() << std::endl 
                    << "  " << data_set.GetDescription() 
                    << std::endl;
            }
        } else {
            std::cerr << "ListDataSets error: "
                << outcome.GetError().GetExceptionName() << " - "
                << outcome.GetError().GetMessage() << std::endl;
        }
    }

    Aws::ShutdownAPI(options);
}