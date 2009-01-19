import sys
sys.path.append("../")
from gnip import publisher
import unittest

class PublisherTestCase(unittest.TestCase):
    def setUp(self):
        self.rule_types = ['actor', 'tag']
        self.publisherName = "test"
        self.xml = '<publisher name="test"><supportedRuleTypes>' + \
            '<type>actor</type><type>tag</type></supportedRuleTypes></publisher>'

    def tearDown(self):
        pass
    
    def testToXml(self):
        a_publisher = publisher.Publisher(name=self.publisherName, rule_types=self.rule_types)
        self.assertEqual(a_publisher.to_xml(), self.xml)

    def testFromXml(self):
        a_publisher = publisher.Publisher()
        a_publisher.from_xml(self.xml)
        
        self.assertEqual(a_publisher.name, self.publisherName)
        self.assertEqual(a_publisher.rule_types, self.rule_types)
        