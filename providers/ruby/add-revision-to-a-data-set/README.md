# Add a New Revision to a Data Set

This sample adds a new finalized revision to a data set using data in S3 by combining the [AWS Marketplace Catalog API](https://docs.aws.amazon.com/marketplace-catalog/latest/api-reference/welcome.html)'s [AddRevisions](https://docs.aws.amazon.com/es_es/data-exchange/latest/userguide/add-revisions.html) change set, and the [AWS Data Exchange API](https://docs.aws.amazon.com/data-exchange/latest/apireference/welcome.html).

To run the sample, set `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_SESSION_TOKEN`, `AWS_REGION` and `ENTITY_ID` that identifies the product that contains a data set to add a revision to. You can enumerate [owned data products](https://console.aws.amazon.com/dataexchange/home?region=us-east-1#/owned/products) using the [enumerate-data-products sample](../enumerate-data-products) to get this ID.

```
$ ENTITY_ID=prod-... bundle exec ruby add-revision-to-a-data-set.rb

6c6becda6a8fb086b945bbf1dca4e1f5: Junto Heartbeat updated 1 minute and 15 seconds ago
Created revision 3e6d60894e5e3bee5c528d0ef5268f71
Importing aws-samples-create-data-set-with-finalized-revision/data.txt from S3 ............. done.
The revision 3e6d60894e5e3bee5c528d0ef5268f71 has been finalized.
Started change set 2jqqse6runsgfz8uej5e2mpq6 ............ done.
Change set 2jqqse6runsgfz8uej5e2mpq6 published.
Done.
```