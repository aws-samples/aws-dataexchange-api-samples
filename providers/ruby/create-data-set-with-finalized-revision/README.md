# All Entitled Data Sets

This sample creates a new Data Set with a finalized revision using data in S3.

To run the sample, set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` and change the values for `s3_bucket_name` and `s3_data_key` used to identify data to add to a revision from S3.

```
$ bundle exec ruby create-data-set-with-finalized-revision.rb 

Created a new Data Set 003686f310ac07ae35e8edd63af7e5b5 called "aws-dataexchange-api-samples test".
Created revision 0ad999457bbc726d76acc4ff6361c9bf
Importing bucket/file.txt from S3 .......... done.
The revision 0ad999457bbc726d76acc4ff6361c9bf has been finalized.
```