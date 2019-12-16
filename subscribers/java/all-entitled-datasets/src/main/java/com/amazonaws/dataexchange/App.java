package com.amazonaws.dataexchange;

import com.amazonaws.services.dataexchange.*;
import com.amazonaws.services.dataexchange.model.*;

public class App {
    public static void main(String[] args) {
        AWSDataExchange client = AWSDataExchangeClientBuilder.defaultClient();

        ListDataSetsRequest request = new ListDataSetsRequest()
                .withOrigin("ENTITLED");

        ListDataSetsResult result = client.listDataSets(request);

        for (DataSetEntry dataSet : result.getDataSets()) {
            System.out.printf("%s/%s: %s\n  %s\n",
                    dataSet.getOriginDetails().getProductId(),
                    dataSet.getId(),
                    dataSet.getName(),
                    dataSet.getDescription());
        }

        System.exit(0);
    }
}
