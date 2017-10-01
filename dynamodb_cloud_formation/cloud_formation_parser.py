#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import yaml
from dynamodb_cloud_formation.dynamodb_resource_parser import DynamoDbResourceParser


class CloudFormationParser:
    def __init__(self):
        self.dynamo_db_resources = {}
        self.dynamo_db_resource_list = []
        self.processed = set()

    def load_json(self, filename):
        # load the resource as JSON
        with open(filename) as fileHandle:
            jsonData = json.load(fileHandle)
            return jsonData

    def load_yaml(self, filename):
        # load the resource as YAML
        with open(filename) as fileHandle:
            yamlData = yaml.load(fileHandle)
            return yamlData

    def parse_cloud_formation_template(self, file_name):
        try:
            cloud_formation_json = self.load_yaml(file_name)
        except yaml.scanner.ScannerError:
            cloud_formation_json = self.load_json(file_name)

        resources = cloud_formation_json['Resources']

        # parse all the DynamoDb resources in the cloud formation template
        for resource_id in resources.keys():
            resource = resources[resource_id]
            if resource['Type'] == 'AWS::DynamoDB::Table':
                dynamoDbResource = DynamoDbResourceParser(resource)
                self.dynamo_db_resources[resource_id] = dynamoDbResource

        # build a list of tables in creation order
        for resourceId in self.dynamo_db_resources.keys():
            self.outputTable(resourceId)

        # return the list of tables
        return self.dynamo_db_resource_list

    def outputTable(self, resourceId):
        if resourceId not in self.processed:
            table = self.dynamo_db_resources[resourceId]

            # pre-emptively mark the table as processed to avoid endless recursion
            self.processed.add(resourceId)

            if table.dependency() != "":
                # recursively add the dependency first
                self.outputTable(table.dependency())

            # add the table to our list
            self.dynamo_db_resource_list.append(table)
