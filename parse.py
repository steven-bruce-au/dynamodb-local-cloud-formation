#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import sys
from dynamodb_cloud_formation.cloud_formation_parser import CloudFormationParser

import argparse

parser = argparse.ArgumentParser(description='Translate AWS Cloud Formation template to AWS CLI commands')
parser.add_argument('filename', metavar='<filename>', 
                   help='The cloud formation template')
parser.add_argument('--region', dest='region',metavar='<region>',default='us-east-1',
                   help='The AWS region to simulate when creating DynamoDB local tables')

parser.add_argument('--endpoint-url', dest='endpoint',metavar='<url>', default='http://localhost:8000',
                   help='The DynamoDB local endpoint url')

args = parser.parse_args()

try:
	cloudFormationParser = CloudFormationParser()

	# iterate through tables in dependency order
	for table in cloudFormationParser.parse_cloud_formation_template(args.filename):
		print table.toCLI(args.region, args.endpoint)

except IOError:
	print "Unable to open cloud formation template: " + args.filename
	sys.exit(-2)
except ValueError:
	print "Unable to parse open cloud formation template: " + args.filename
	sys.exit(-3)

sys.exit(0)
