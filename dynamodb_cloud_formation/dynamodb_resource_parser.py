#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json

class DynamoDbResourceParser:
	def __init__(self, resourceJson):
		self.json = resourceJson

	def dependency(self):
		if 'DependsOn' in self.json:
			return self.json['DependsOn']
		else:
			return ""

	def tableName(self):
		return " --table-name " + self.json['Properties']['TableName']

	def attributeDefinitions(self):
		
		attributeDefinitions = self.json['Properties']['AttributeDefinitions']
		if len(attributeDefinitions) == 0:
			return ""
		return " --attribute-definitions '" + json.JSONEncoder(sort_keys=True).encode(attributeDefinitions) + "'"
		
	def keySchema(self):
		
		keySchema = self.json['Properties']['KeySchema']
		if len(keySchema) == 0:
			return ""

		return " --key-schema '" + json.JSONEncoder(sort_keys=True).encode(keySchema) + "'"

	def provisionedThroughput(self):
		if 'ProvisionedThroughput' in self.json['Properties']:
			provisionedThroughput = self.json['Properties']['ProvisionedThroughput']

			provisionedThroughput['ReadCapacityUnits'] = int(provisionedThroughput['ReadCapacityUnits'])
			provisionedThroughput['WriteCapacityUnits'] = int(provisionedThroughput['WriteCapacityUnits'])
			return " --provisioned-throughput '" + json.JSONEncoder(sort_keys=True).encode(provisionedThroughput) + "'"
		else: 
			return ""

	def localSecondaryIndexes(self):
		if 'LocalSecondaryIndexes' in self.json['Properties']:
			localSecondaryIndexes = self.json['Properties']['LocalSecondaryIndexes']
			if len(localSecondaryIndexes) == 0:
				return ""

			for index in localSecondaryIndexes:
				if "ProvisionedThroughput" in index:
					provisionedThroughput = index['ProvisionedThroughput']
					provisionedThroughput['ReadCapacityUnits'] = int(provisionedThroughput['ReadCapacityUnits'])
					provisionedThroughput['WriteCapacityUnits'] = int(provisionedThroughput['WriteCapacityUnits'])

			return " --local-secondary-indexes '" + json.JSONEncoder(sort_keys=True).encode(localSecondaryIndexes) + "'"
		else:
			return ""


	def globalSecondaryIndexes(self):
		if 'GlobalSecondaryIndexes' in self.json['Properties']:
			globalSecondaryIndexes = self.json['Properties']['GlobalSecondaryIndexes']
			if len(globalSecondaryIndexes) == 0:
				return ""

			for index in globalSecondaryIndexes:
				if "ProvisionedThroughput" in index:
					provisionedThroughput = index['ProvisionedThroughput']
					provisionedThroughput['ReadCapacityUnits'] = int(provisionedThroughput['ReadCapacityUnits'])
					provisionedThroughput['WriteCapacityUnits'] = int(provisionedThroughput['WriteCapacityUnits'])

			return " --global-secondary-indexes '" + json.JSONEncoder(sort_keys=True).encode(globalSecondaryIndexes) + "'"
		else:
			return ""

	def toCLI(self, region, endpoint_url):
		return 	''.join(('aws dynamodb create-table --region ',
				region,
				' --endpoint-url ',
				endpoint_url,
				self.tableName(),
				self.attributeDefinitions(), 
				self.keySchema(),
				self.localSecondaryIndexes(), 
				self.globalSecondaryIndexes(), 
				self.provisionedThroughput(), 
				"\n"))


