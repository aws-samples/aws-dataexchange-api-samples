package main

import (
    "github.com/aws/aws-sdk-go/aws"
    "github.com/aws/aws-sdk-go/aws/session"
    "github.com/aws/aws-sdk-go/service/dataexchange"
    "fmt"
)

func main() {
    // Initialize a session that the SDK will use to load
    // credentials from the shared credentials file ~/.aws/credentials
    // and region from the shared configuration file ~/.aws/config.
    sess := session.Must(session.NewSessionWithOptions(session.Options{
      SharedConfigState: session.SharedConfigEnable,
    }))
    svc := dataexchange.New(sess)

    dataSetList, err := svc.ListDataSets(&dataexchange.ListDataSetsInput{
      Origin: aws.String("ENTITLED"),
    })

    if err != nil {
      fmt.Println(err.Error())
      return
    }

    for _, dataSet := range dataSetList.DataSets {
      fmt.Printf("%#s/%#s: %#s\n %#s\n", *dataSet.OriginDetails.ProductId, *dataSet.Id, *dataSet.Name, *dataSet.Description)
    }
}
