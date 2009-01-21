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

    def testPublisherEquals(self):
        publisher1 = publisher.Publisher("foo", ["actor", "to"])
        publisher2 = publisher.Publisher("foo", ["actor", "to"])

        self.assertEquals(publisher1,publisher2)

        publisher1 = publisher.Publisher("foo", ["actor", "to"])
        publisher2 = publisher.Publisher("foo", ["to", "actor"])

        self.assertEquals(publisher1,publisher2)

    def testPublisherNotEquals(self):
        publisher1 = publisher.Publisher("foo", ["actor", "to"])
        publisher2 = publisher.Publisher("bar", ["actor", "to"])
        publisher3 = publisher.Publisher("foo", ["actor"])
        publisher4 = publisher.Publisher("foo", ["actor", "tags"])

        self.assertNotEquals(publisher1, publisher2)
        self.assertNotEquals(publisher1, publisher3)
        self.assertNotEquals(publisher2, publisher3)
        self.assertNotEquals(publisher1, publisher4)

if __name__ == '__main__':
    unittest.main()             
        