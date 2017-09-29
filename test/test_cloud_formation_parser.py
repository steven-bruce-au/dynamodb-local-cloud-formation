import unittest
from dynamodb_cloud_formation.cloud_formation_parser import CloudFormationParser


class TestCloudFormationParser(unittest.TestCase):
    def parse(self, templateFileName, expectedTableNames):
        # parse the Cloud Formation Resource
        cloudFormationParser = CloudFormationParser()
        tables = cloudFormationParser.parse_cloud_formation_template(templateFileName, args.type)

        tableNames = list(map((lambda table: table.json['Properties']['TableName']), tables))
        self.assertEqual(tableNames, expectedTableNames)

        # verify parsing of the dynamodb resource

    def test_sample_template(self):
        # ensure that myTableName is constructed before myTableName2
        self.parse('test/data/sample.template', ['myTableName', 'myTableName2'])

    def test_sample_yaml_template(self):
        # ensure that myTableName is constructed before myTableName2
        self.parse('test/data/sample.yaml.template', ['myTableName', 'myTableName2'])


suite = unittest.TestLoader().loadTestsFromTestCase(TestCloudFormationParser)
unittest.TextTestRunner(verbosity=2).run(suite)
