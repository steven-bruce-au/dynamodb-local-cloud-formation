# Cloud Formation parser for DynamoDB local

This script converts the DynamoDB resources in a Amazon Web Services Cloud Formation template to a series of [AWS Command Line Interface] commands.

## Prerequisites

  * [Python] 
  * [AWS Command Line Interface] 
  * [AWS DynamoDB Local]

You must also configure the default credentials for use with [AWS Command Line Interface] 
```sh
$ aws configure
```

## Usage
```sh
$ python ./parse.py [-h] [--region <region>] [--endpoint-url <url>] <filename>
```
  - region - The AWS region simulate in DynamoDB Local (default: us-east-1) 
  - endpoint-url - The DynamoDB Local endpoint URL (default: http://localhost:8000)
  - filename - The AWS CloudFormation template to convert
  
## Running the tests

```sh
python -m unittest discover
```

## Putting it all together

Assuming you have DynamoDB Local running on port 8000 you can do the following to build and exexcute the script in one command:

```sh
python ./parse.py test/data/sample.template | sh
```
  

## Example

Consider the following sample cloud formation template with two tables defined. There are two tables:
  * myTableName
  * myTableName2

The second table depends on the first so it will be constructed after the first.

```sh
python ./parse.py test/data/sample.template
```



```sh
{
  "AWSTemplateFormatVersion" : "2010-09-09",
  "Resources" : {
    "myDynamoDBTable" : {
      "Type" : "AWS::DynamoDB::Table",
      "Properties" : {
        "AttributeDefinitions" : [
          {
            "AttributeName" : "Album",
            "AttributeType" : "S"   
          },
          {
            "AttributeName" : "Artist",
            "AttributeType" : "S"
          },
          {
            "AttributeName" : "Sales",
            "AttributeType" : "N"
          }
        ],
        "KeySchema" : [
          {
            "AttributeName" : "Album",
            "KeyType" : "HASH"
          },
          {
            "AttributeName" : "Artist",
            "KeyType" : "RANGE"
          }
        ],
        "ProvisionedThroughput" : {
          "ReadCapacityUnits" : "5",
          "WriteCapacityUnits" : "5"
        },
        "TableName" : "myTableName",
        "GlobalSecondaryIndexes" : [{
          "IndexName" : "myGSI",
          "KeySchema" : [
            {
              "AttributeName" : "Sales",
              "KeyType" : "HASH"
            },
            {
              "AttributeName" : "Artist",
              "KeyType" : "RANGE"
            }
          ],                         
          "Projection" : {
            "NonKeyAttributes" : ["Album"],
            "ProjectionType" : "INCLUDE"
          },
          "ProvisionedThroughput" : {
            "ReadCapacityUnits" : "5",
            "WriteCapacityUnits" : "5"
          }
        }],
        "LocalSecondaryIndexes" :[{
          "IndexName" : "myLSI",
          "KeySchema" : [
            {
              "AttributeName" : "Album",
              "KeyType" : "HASH"
            },
            {
              "AttributeName" : "Sales",
              "KeyType" : "RANGE"
            }
          ],                           
          "Projection" : {
            "NonKeyAttributes" : ["Artist"],
            "ProjectionType" : "INCLUDE"
          }
        }]
      }
    },
	"mySecondDDBTable" : {
	  "Type" : "AWS::DynamoDB::Table",
	  "DependsOn" : "myDynamoDBTable" ,
	  "Properties" : {
	    "AttributeDefinitions" : [
	      {
		"AttributeName" : "ArtistId",
		"AttributeType" : "S"        
	      },
	      {
		"AttributeName" : "Concert",
		"AttributeType" : "S"        
	      },
	      {
		"AttributeName" : "TicketSales",
		"AttributeType" : "S"        
	      }
	    ],
	    "KeySchema" : [
	      {
		"AttributeName" : "ArtistId",
		"KeyType" : "HASH"
	      },
	      {
		"AttributeName" : "Concert",
		"KeyType" : "RANGE"
	      }
	    ],
	    "TableName": "myTableName2",
	    "ProvisionedThroughput" : {
	      "ReadCapacityUnits" : "5",
	      "WriteCapacityUnits" : "5"
	    },
	    "GlobalSecondaryIndexes" : [{
	      "IndexName" : "myGSI",
	      "KeySchema" : [
		{
		  "AttributeName" : "TicketSales",
		  "KeyType" : "HASH"
		}
	      ],                           
	      "Projection" : {
		"ProjectionType" : "KEYS_ONLY"
	      },    
	      "ProvisionedThroughput" : {
		"ReadCapacityUnits" : "5",
		"WriteCapacityUnits" : "5"
	      }
	    }]
	  }
	}

  }
}

```




```sh
aws dynamodb create-table --region us-east-1 --endpoint-url http://localhost:8000 --table-name myTableName --attribute-definitions '[{"AttributeName": "Album", "AttributeType": "S"}, {"AttributeName": "Artist", "AttributeType": "S"}, {"AttributeName": "Sales", "AttributeType": "N"}]' --key-schema '[{"AttributeName": "Album", "KeyType": "HASH"}, {"AttributeName": "Artist", "KeyType": "RANGE"}]' --local-secondary-indexes '[{"IndexName": "myLSI", "KeySchema": [{"AttributeName": "Album", "KeyType": "HASH"}, {"AttributeName": "Sales", "KeyType": "RANGE"}], "Projection": {"NonKeyAttributes": ["Artist"], "ProjectionType": "INCLUDE"}}]' --global-secondary-indexes '[{"IndexName": "myGSI", "KeySchema": [{"AttributeName": "Sales", "KeyType": "HASH"}, {"AttributeName": "Artist", "KeyType": "RANGE"}], "Projection": {"NonKeyAttributes": ["Album"], "ProjectionType": "INCLUDE"}, "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}}]' --provisioned-throughput '{"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}'

aws dynamodb create-table --region us-east-1 --endpoint-url http://localhost:8000 --table-name myTableName2 --attribute-definitions '[{"AttributeName": "ArtistId", "AttributeType": "S"}, {"AttributeName": "Concert", "AttributeType": "S"}, {"AttributeName": "TicketSales", "AttributeType": "S"}]' --key-schema '[{"AttributeName": "ArtistId", "KeyType": "HASH"}, {"AttributeName": "Concert", "KeyType": "RANGE"}]' --global-secondary-indexes '[{"IndexName": "myGSI", "KeySchema": [{"AttributeName": "TicketSales", "KeyType": "HASH"}], "Projection": {"ProjectionType": "KEYS_ONLY"}, "ProvisionedThroughput": {"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}}]' --provisioned-throughput '{"ReadCapacityUnits": 5, "WriteCapacityUnits": 5}'

```
## Known Issues

This script would require further modification to support parameterised DynamoDB resources in a Cloud Formation template.

[AWS Command Line Interface]:http://aws.amazon.com/cli/
[Python]:https://www.python.org/
[AWS DynamoDB Local]:http://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Tools.DynamoDBLocal.html

