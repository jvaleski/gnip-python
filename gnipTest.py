import unittest
from gnip import *
from string import count
from xml.dom.minidom import parseString
import time
import random

# Be sure to fill these in if you want to run the test cases
TEST_USERNAME = ""
TEST_PASSWORD = ""
TEST_PUBLISHER = ""
TEST_SERVER = "prod.gnipcentral.com"

class GnipTestCase(unittest.TestCase):
    
    def __init__(self,*args):
        unittest.TestCase.__init__(self,*args)
        self.gnip = Gnip(TEST_USERNAME, TEST_PASSWORD, TEST_SERVER)
    
    def setUp(self):
        self.filterXml = '<?xml version="1.0" encoding="UTF-8"' +\
            ' standalone="yes"?>' +\
            '<filter fullData="true" name="test">' + \
            '<rule value="me" type="actor"/>' + \
            '<rule value="you" type="actor"/>' + \
            '<rule value="sally" type="actor"/>' + \
            '</filter>'
        self.rules = [["actor", "me"], ["actor", "you"], ["actor", "sally"]]
        self.filterName = "test"
        self.filterFullData = "false"
        self.success = '<result>Success</result>'

    def tearDown(self):
        self.gnip.delete_filter(TEST_PUBLISHER, self.filterName)

    def testCompressUncompress(self):
        string = "BlahBlah"
        compressed = self.gnip.compress_with_gzip(string)
        uncompressed = self.gnip.decompress_gzip(compressed)
        self.assertEqual(string, uncompressed)

    def testPublishXml(self):
        randVal = str(random.randint(1, 99999999))
        xml = '<?xml version=\'1.0\' encoding=\'utf-8\'?><activities><activity ' + \
             'at="2008-07-02T11:16:16+00:00" action="upload" actor="sally" ' + \
             'regarding="' + randVal + '" source="web" ' + \
             'tags="trains,planes,automobiles" ' + \
             'to="bob" url="http://example.com"/></activities>'
        result = self.gnip.publish_xml(TEST_PUBLISHER, xml)
        self.assertEqual(result, self.success)

    def testPublishActivities(self):
        randVal = str(random.randint(1, 99999999))
        an_activity = activity.Activity(action="upload", actor="sally",
                                regarding=str(randVal),
                                source="web", tags=["trains", "planes", "automobiles"],
                                to="bob", url="http://example.com")
        an_activity.set_at_from_string("2008-07-02T11:16:16+00:00")
        result = self.gnip.publish_activities(TEST_PUBLISHER, [an_activity])
        self.assertEqual(result, self.success)

    def testGetPublisherNotifications(self):
        randVal = str(random.randint(1, 99999999))
        xml = '<?xml version=\'1.0\' encoding=\'utf-8\'?><activities><activity ' + \
             'at="2008-07-02T11:16:16+00:00" action="upload" actor="sally" ' + \
             'regarding="' + randVal + '" source="web" ' + \
             'tags="trains,planes,automobiles" ' + \
             'to="bob" url="http://example.com"/></activities>'
        self.gnip.publish_xml(TEST_PUBLISHER, xml)

        resultActivities = self.gnip.get_publisher_notifications(TEST_PUBLISHER)
        numMatches = 0
        for singleActivity in resultActivities:
            numMatches += count(singleActivity.regarding, randVal)
        self.assert_(0 != numMatches)

    def testGetPublisherNotificationsXml(self):
        randVal = str(random.randint(1, 99999999))
        xml = '<?xml version=\'1.0\' encoding=\'utf-8\'?><activities><activity ' + \
             'at="2008-07-02T11:16:16+00:00" action="upload" actor="sally" ' + \
             'regarding="' + randVal + '" source="web" ' + \
             'tags="trains,planes,automobiles" ' + \
             'to="bob" url="http://example.com"/></activities>'
        self.gnip.publish_xml(TEST_PUBLISHER, xml)

        resultXml = self.gnip.get_publisher_notifications_xml(TEST_PUBLISHER)
        self.assert_(randVal in resultXml)

    def testGetFilterNotifications(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER, a_filter)
        randVal = str(random.randint(1, 99999999))
        xml = '<?xml version=\'1.0\' encoding=\'utf-8\'?><activities><activity ' + \
             'at="2008-07-02T11:16:16+00:00" action="upload" actor="sally" ' + \
             'regarding="' + randVal + '" source="web" ' + \
             'tags="trains,planes,automobiles" ' + \
             'to="bob" url="http://example.com"/></activities>'
        self.gnip.publish_xml(TEST_PUBLISHER, xml)

        resultActivities = self.gnip.get_filter_notifications(TEST_PUBLISHER,
            self.filterName)

        numMatches = 0
        for singleActivity in resultActivities:
            numMatches += count(singleActivity.regarding, randVal)
        self.assert_(0 != numMatches)

    def testGetFilterNotificationsXml(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER, a_filter)
        randVal = str(random.randint(1, 99999999))
        xml = '<?xml version=\'1.0\' encoding=\'utf-8\'?><activities><activity ' + \
             'at="2008-07-02T11:16:16+00:00" action="upload" actor="sally" ' + \
             'regarding="' + randVal + '" source="web" ' + \
             'tags="trains,planes,automobiles" ' + \
             'to="bob" url="http://example.com"/></activities>'
        self.gnip.publish_xml(TEST_PUBLISHER, xml)

        resultXml = self.gnip.get_filter_notifications_xml(TEST_PUBLISHER, self.filterName)
        self.assert_(randVal in resultXml)

    def testUpdateFilter(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER, a_filter)
        a_second_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        a_second_filter.rules.append(["actor", "joe"])
        result = self.gnip.update_filter(TEST_PUBLISHER, a_second_filter)
        self.assertEqual(result, self.success)

    def testUpdateFilterFromXml(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER, a_filter)
        updatedXml = '<filter name="test" fullData="true">' + \
            '<rule type="actor" value="me"/>' + \
            '<rule type="actor" value="you"/>' + \
            '<rule type="actor" value="bob"/>' + \
            '<rule type="actor" value="joe"/>' + \
            '</filter>'
        result = self.gnip.update_filter_from_xml(TEST_PUBLISHER,
            a_filter.name, updatedXml)
        self.assertEqual(result, self.success)

    def testCreateFilter(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER, a_filter)
        result = self.gnip.find_filter_xml(TEST_PUBLISHER, self.filterName)
        self.assert_('sally' in result)

    def testDeleteFilter(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER, a_filter)
        result = self.gnip.delete_filter(TEST_PUBLISHER, self.filterName)
        self.assertEqual(result, self.success)

    def testFindFilter(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER, a_filter)
        resultfilter = self.gnip.find_filter(TEST_PUBLISHER, self.filterName)
        self.assertEqual(resultfilter.name, a_filter.name)

    def testFindFilterXml(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER, a_filter)
        resultXml = self.gnip.find_filter_xml(TEST_PUBLISHER, self.filterName)
        self.assert_("sally" in resultXml)
        
    def testGetPublisher(self):
        pub = self.gnip.get_publisher(TEST_PUBLISHER)
        self.assertEquals(TEST_PUBLISHER, pub.name)
        
    def testGetPublisherXml(self):
        resultXml = self.gnip.get_publisher_xml(TEST_PUBLISHER)
        self.assert_(TEST_PUBLISHER in resultXml)

    def testCreatePublisher(self):
        randVal = str(random.randint(1, 99999999))
        pub = publisher.Publisher(TEST_PUBLISHER + randVal, ['actor', 'tag'])
        self.gnip.create_publisher(pub)
        resultXml = self.gnip.get_publisher_xml(TEST_PUBLISHER + randVal)
        self.assert_(TEST_PUBLISHER + randVal in resultXml)
        
    def testCreatePublisherFromXml(self):
        randVal = str(random.randint(1, 99999999))
        self.publisherXml = '<publisher name="' + TEST_PUBLISHER + randVal + '">' + \
            '<supportedRuleTypes><type>actor</type><type>tag</type>' + \
            '</supportedRuleTypes></publisher>'

        resultXml = self.gnip.create_publisher_from_xml(TEST_PUBLISHER, self.publisherXml)
        resultXml = self.gnip.get_publisher_xml(TEST_PUBLISHER + randVal)
        self.assert_(TEST_PUBLISHER + randVal in resultXml)
        
    def testUpdatePublisher(self):
        pub = publisher.Publisher(TEST_PUBLISHER, ['actor', 'tag'])
        self.gnip.update_publisher(pub)
        resultXml = self.gnip.get_publisher_xml(TEST_PUBLISHER)
        self.assert_('<type>tag</type>' in resultXml)
        
    def testUpdatePublisherFromXml(self):
        self.publisherXml = '<publisher name="' + TEST_PUBLISHER + '">' + \
            '<supportedRuleTypes><type>actor</type>' + \
            '</supportedRuleTypes></publisher>'
        resultXml = self.gnip.update_publisher_from_xml(TEST_PUBLISHER, self.publisherXml)
        resultXml = self.gnip.get_publisher_xml(TEST_PUBLISHER)
        self.assert_('<type>tag</type>' not in resultXml)

if __name__ == '__main__':
    unittest.main()

