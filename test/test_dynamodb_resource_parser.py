import unittest
import json
from dynamodb_cloud_formation.dynamodb_resource_parser import DynamoDbResourceParser


class TestDynamoDbResourceParser(unittest.TestCase):

    def loadTextFile(self, filename):
        # load the contents of a text file
        file = open(filename, 'r')
        text = file.read()
        file.close()
        return text

    def loadJson(self, filename):
        # load the resource as JSON
        with open(filename) as fileHandle:
            jsonData = json.load(fileHandle)
            return jsonData

    def parse(self, resourceFileName, expectedCliFileName):

        # load test data
        expected = self.loadTextFile(expectedCliFileName)
        resourceJson = self.loadJson(resourceFileName)

        # parse the Cloud Formation Resource
        dynamoDbResource = DynamoDbResourceParser(resourceJson)
        command = dynamoDbResource.toCLI('us-east-1','http://localhost:8000')

        # verify parsing of the dynamodb resource
        self.assertEqual(command, expected, ''.join(('Error parsing DynamoDb configuration for: ',
                                            resourceFileName,
                                            '\nexpected: ',
                                            expected,
                                            '\nactual  : ',
                                            command,
                                            '')))

    def test_album_sales(self):
        # execute the test for the album_sales table
        self.parse('test/data/album_sales.json', 'test/data/album_sales.cli')




suite = unittest.TestLoader().loadTestsFromTestCase(TestDynamoDbResourceParser)
unittest.TextTestRunner(verbosity=2).run(suite)