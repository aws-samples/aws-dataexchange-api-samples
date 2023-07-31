import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from datetime import date
from datetime import timedelta
from  pyspark.sql.functions import input_file_name
from awsglue.dynamicframe import DynamicFrame

## @params: [JOB_NAME,S3_CLOUDTRAIL_BASE_PATH, S3_WRITE_PATH, GLUE_DATABASE, GLUE_TABLE_NAME, OVERRIDE_S3_READ_PATH, S3_READ_PATH]
args = getResolvedOptions(sys.argv, ['JOB_NAME',
                                     'S3_CLOUDTRAIL_BASE_PATH', 
                                     'S3_WRITE_PATH',
                                     'GLUE_DATABASE',
                                     'GLUE_TABLE_NAME',
                                     'OVERRIDE_S3_READ_PATH',
                                     'S3_READ_PATH'
                                     ])

print("Job Parameters - Start")
print("JOB_NAME : ", args['JOB_NAME'])
print("S3_CLOUDTRAIL_BASE_PATH : ", args['S3_CLOUDTRAIL_BASE_PATH'])
print("S3_WRITE_PATH : ", args['S3_WRITE_PATH'])
print("GLUE_DATABASE : ", args['GLUE_DATABASE'])
print("GLUE_TABLE_NAME : ", args['GLUE_TABLE_NAME'])
print("OVERRIDE_S3_READ_PATH : ", args['OVERRIDE_S3_READ_PATH'])
print("S3_READ_PATH : ", args['S3_READ_PATH'])
print("Job Parameters - End")

##Construct directory for previous day logs:
today = date.today()
previous_day = today - timedelta(days = 1)
print("Process Cloud Trail Logs for : ", previous_day)

year=previous_day.year
month='{:02d}'.format(previous_day.month)
day='{:02d}'.format(previous_day.day)

##s3_read_path

if args['OVERRIDE_S3_READ_PATH'].upper() == 'YES':
    s3_read_path=args['S3_READ_PATH']
else:
    s3_read_path=args['S3_CLOUDTRAIL_BASE_PATH'] + '/' + str(year) + '/' + str(month) + '/' + str(day) + '/' 

print("S3 read path : ", s3_read_path)

sc = SparkContext()

glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

print("Spark Job Start")

#read json filess
dataFrame = spark.read\
    .option("multiline", "true")\
    .json(s3_read_path)
    

dataFrame_files=dataFrame.withColumn("filename", input_file_name())

#For Debug
#dataFrame_files.show()
#dataFrame_files.printSchema()

dataFrame_files.createOrReplaceTempView("logs_json")
spark.sql("describe logs_json").show()

#Transform - Expand Data Types to get needed fields
t2=spark.sql("Select explode(Records), filename from logs_json")
#t2.printSchema()
t2.createOrReplaceTempView("logs_json_2")

t3=spark.sql("Select col,explode(col.resources)as resources, filename from logs_json_2")
t3.createOrReplaceTempView("logs_json_3")

#Filter ADX Accounts
t4=spark.sql("""Select * from logs_json_3 
                    where resources.type = 'AWS::S3::AccessPoint' 
                    and 
                    resources.accountId IN 
                        ('540564263739',
                        '504002150500',
                        '337040091392',
                        '366362662752',
                        '330489627928',
                        '291973504423',
                        '291973504423',
                        '461002523379',
                        '036905324694',
                        '675969394711',
                        '108584782536',
                        '844053218156')""")

t4.createOrReplaceTempView("logs_json_filtered")

#Get required fields
t5=spark.sql("""Select 
    col.eventID,
    col.eventName,
    col.eventTime, 
    col.awsRegion as provider_bucket_region, 
    col.userIdentity.accountId as subscriber_account_id,
    col.sourceIPAddress as subscriber_ip_address,
    col.userAgent as subscriber_user_agent,
    col.requestParameters.bucketName as provider_bucket_name,
    col.requestParameters.`x-amz-request-payer` as x_amz_request_payer,
    col.requestParameters.prefix as prefix,
    col.additionalEventData.bytesTransferredOut as bytes_accessed,
    col.resources.arn as access_point_arn,
    col.tlsDetails.tlsVersion as tls_version,
    array_join(slice(split(filename,'/'), -2, 1),'') as day,
    array_join(slice(split(filename,'/'), -3, 1),'') as month ,
    array_join(slice(split(filename,'/'), -4, 1),'') as year,
    array_join(slice(split(filename,'/'), -5, 1),'') as region
    from logs_json_filtered""")
    
t5.show(truncate = True)
t5_s3_write=DynamicFrame.fromDF(t5, glueContext, "t5_s3_write")

print("Write to S3 Start")

sink_out = glueContext.getSink(connection_type="s3", path=args['S3_WRITE_PATH'],
    enableUpdateCatalog=True, updateBehavior="UPDATE_IN_DATABASE",
    partitionKeys=["year", "month", "day"])
sink_out.setFormat("glueparquet")
sink_out.setCatalogInfo(catalogDatabase=args['GLUE_DATABASE'], catalogTableName=args['GLUE_TABLE_NAME'])
sink_out.writeFrame(t5_s3_write)
print("Write to S3 End")

print("Spark Job End")


    
job.commit()