# Read/Write Batch to DynamoDB from CLI
* You should already be authenticated from `~/.aws` or `IAM Policy`.
* Region can be in `config` file or overridden from CLI or an env. variable
  
## Insert batch to table from AWS CLI

```
aws dynamodb batch-write-item --request-items file://put.json --region us-east-2
```
## Get batch of items from AWS CLI

```
aws dynamodb batch-get-item --request-items file://get.json --region us-east-2
```

## Additional jars to add to /lib in PDI
- aws-java-sdk-dynamodb-1.11.524.jar
- aws-java-sdk-core-1.11.524.jar
- joda-time-2.9.9.jar
```
 https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk-dynamodb/1.11.524
 https://mvnrepository.com/artifact/com.amazonaws/aws-java-sdk-core/1.11.524
 https://mvnrepository.com/artifact/joda-time/joda-time/2.9.9
````
