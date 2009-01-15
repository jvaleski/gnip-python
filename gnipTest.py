import unittest
from gnip import *
from string import count
from xml.dom.minidom import parseString
import time
import random
import place
import payload
import xml_objects

# Be sure to fill these in if you want to run the test cases
TEST_USERNAME = ""
TEST_PASSWORD = ""
TEST_PUBLISHER = ""
TEST_PUBLISHER_SCOPE = "my"
TEST_SERVER = "review.gnipcentral.com"

class GnipTestCase(unittest.TestCase):
    
    def __init__(self,*args):
        unittest.TestCase.__init__(self,*args)
        self.gnip = Gnip(TEST_USERNAME, TEST_PASSWORD, TEST_SERVER)
    
    def setUp(self):
        self.filterXml = '<?xml version="1.0" encoding="UTF-8"' +\
            ' standalone="yes"?>' +\
            '<filter fullData="true" name="test">' + \
            '<rule type="actor">me</rule>' + \
            '<rule type="actor">you</rule>' + \
            '<rule type="actor">bob</rule>' + \
            '</filter>'
        self.rules = [dict(type="actor", value="me"), dict(type="actor", value="you"), dict(type="actor", value="bob")]
        self.filterName = "test"
        self.filterFullData = "false"
        self.success = '<result>Success</result>'

    def tearDown(self):
        self.gnip.delete_filter(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, self.filterName)

    def testCompressUncompress(self):
        string = "BlahBlah"
        compressed = self.gnip.compress_with_gzip(string)
        uncompressed = self.gnip.decompress_gzip(compressed)
        self.assertEqual(string, uncompressed)

    def testPublishXml(self):
        randVal = str(random.randint(1, 99999999))
        xml = '<?xml version=\'1.0\' encoding=\'utf-8\'?><activities><activity>' + \
             '<at>2008-07-02T11:16:16+00:00</at><action>update</action><activityID>' + randVal + '</activityID>' + \
             '<URL>http://example.com</URL><source>web</source><source>website</source>' + \
             '<place><point>1.0 -2.0</point><elev>3.0</elev><floor>4</floor><featuretypetag>city</featuretypetag>' + \
             '<featurename>Boulder</featurename><relationshiptag>center</relationshiptag></place>' + \
             '<place><point>11.0 -12.0</point><elev>13.0</elev><floor>14</floor><featuretypetag>city</featuretypetag>' + \
             '<featurename>Boulder</featurename><relationshiptag>center</relationshiptag></place>' + \
             '<actor>bob</actor><actor>you</actor><destinationURL>http://example.com</destinationURL>' + \
             '<destinationURL>http://example2.com</destinationURL><tag>trains</tag><tag>planes</tag>' + \
             '<to>you</to><to>fred</to><regardingURL>http://regarding.com</regardingURL>' + \
             '<regardingURL>http://regarding2.com</regardingURL>' + \
             '<payload><title>Title</title><body>Body</body><mediaURL>http://media.com</mediaURL>' + \
             '<mediaURL>http://media2.com</mediaURL><raw>raw</raw></payload></activity></activities>'
        result = self.gnip.publish_xml(TEST_PUBLISHER, xml)
        self.assertEqual(result, self.success)

    def testPublishActivities(self):
        randVal = str(random.randint(1, 99999999))
        a_place1 = place.Place(xml_objects.Point(1.0, -2.0), 3, 4, "city", "Boulder", "center")

        a_place2 = place.Place(xml_objects.Point(11.0, -12.0), 13, 14, "city", "Boulder", "center")

        a_payload = payload.Payload(title="Title",
                                    body="Body",
                                    media_urls=[xml_objects.URL(value="http://media1.com", meta_url="http://media1.com/meta"), xml_objects.URL(value="http://media2.com", meta_url="http://media2.com/meta")],
                                    raw="raw")

        an_activity = activity.Activity(action="update",
                                        activity_id=randVal,
                                        url="http://example.com",
                                        sources=["web", "website"],
                                        places=[a_place1, a_place2],
                                        actors=[xml_objects.Actor(value="bob", meta_url="http://bob.com", uid="12345"), xml_objects.Actor(value="me", meta_url="http://me.com", uid="123456")],
                                        destination_urls=[xml_objects.URL(value="http://destination1.com", meta_url="http://destination1.com/meta"), xml_objects.URL(value="http://destination2.com", meta_url="http://destination2.com/meta")],
                                        tags=[xml_objects.Tag(meta_url="http://tag1.com", value="tag1"), xml_objects.Tag(meta_url="http://tag2.com", value="tag2")],
                                        tos=[xml_objects.To(value="you", meta_url="http://you.com"), xml_objects.To(value="fred", meta_url="http://fred.com")],
                                        regarding_urls=[xml_objects.URL(value="http://regarding1.com", meta_url="http://regarding2.com"), xml_objects.URL(value="http://regarding1.com", meta_url="http://regarding2.com")],
                                        payload=a_payload)
        an_activity.set_at_from_string("2008-07-02T11:16:16+00:00")
        result = self.gnip.publish_activities(TEST_PUBLISHER, [an_activity])
        self.assertEqual(result, self.success)

    def testGetPublisherNotifications(self):
        randVal = str(random.randint(1, 99999999))
        xml = '<?xml version=\'1.0\' encoding=\'utf-8\'?><activities><activity>' + \
             '<at>2008-07-02T11:16:16+00:00</at><action>update</action><activityID>' + randVal + '</activityID>' + \
             '<URL>http://example.com</URL><source>web</source><source>website</source>' + \
             '<place><point>1.0 -2.0</point><elev>3.0</elev><floor>4</floor><featuretypetag>city</featuretypetag>' + \
             '<featurename>Boulder</featurename><relationshiptag>center</relationshiptag></place>' + \
             '<place><point>11.0 -12.0</point><elev>13.0</elev><floor>14</floor><featuretypetag>city</featuretypetag>' + \
             '<featurename>Boulder</featurename><relationshiptag>center</relationshiptag></place>' + \
             '<actor>bob</actor><actor>you</actor><destinationURL>http://example.com</destinationURL>' + \
             '<destinationURL>http://example2.com</destinationURL><tag>trains</tag><tag>planes</tag>' + \
             '<to>you</to><to>fred</to><regardingURL>http://regarding.com</regardingURL>' + \
             '<regardingURL>http://regarding2.com</regardingURL>' + \
             '<payload><title>Title</title><body>Body</body><mediaURL>http://media.com</mediaURL>' + \
             '<mediaURL>http://media2.com</mediaURL><raw>raw</raw></payload></activity></activities>'
        self.gnip.publish_xml(TEST_PUBLISHER, xml)

        resultActivities = self.gnip.get_publisher_notifications(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER)
        numMatches = 0
        for singleActivity in resultActivities:
            numMatches += count(singleActivity.activity_id, randVal)
        self.assert_(0 != numMatches)

    def testGetPublisherNotificationsXml(self):
        randVal = str(random.randint(1, 99999999))
        xml = '<?xml version=\'1.0\' encoding=\'utf-8\'?><activities><activity>' + \
             '<at>2008-07-02T11:16:16+00:00</at><action>update</action><activityID>' + randVal + '</activityID>' + \
             '<URL>http://example.com</URL><source>web</source><source>website</source>' + \
             '<place><point>1.0 -2.0</point><elev>3.0</elev><floor>4</floor><featuretypetag>city</featuretypetag>' + \
             '<featurename>Boulder</featurename><relationshiptag>center</relationshiptag></place>' + \
             '<place><point>11.0 -12.0</point><elev>13.0</elev><floor>14</floor><featuretypetag>city</featuretypetag>' + \
             '<featurename>Boulder</featurename><relationshiptag>center</relationshiptag></place>' + \
             '<actor>bob</actor><actor>you</actor><destinationURL>http://example.com</destinationURL>' + \
             '<destinationURL>http://example2.com</destinationURL><tag>trains</tag><tag>planes</tag>' + \
             '<to>you</to><to>fred</to><regardingURL>http://regarding.com</regardingURL>' + \
             '<regardingURL>http://regarding2.com</regardingURL>' + \
             '<payload><title>Title</title><body>Body</body><mediaURL>http://media.com</mediaURL>' + \
             '<mediaURL>http://media2.com</mediaURL><raw>raw</raw></payload></activity></activities>'
        self.gnip.publish_xml(TEST_PUBLISHER, xml)

        resultXml = self.gnip.get_publisher_notifications_xml(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER)
        self.assert_(randVal in resultXml)

    def testGetFilterNotifications(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, a_filter)
        randVal = str(random.randint(1, 99999999))
        xml = '<?xml version=\'1.0\' encoding=\'utf-8\'?><activities><activity>' + \
             '<at>2008-07-02T11:16:16+00:00</at><action>update</action><activityID>' + randVal + '</activityID>' + \
             '<URL>http://example.com</URL><source>web</source><source>website</source>' + \
             '<place><point>1.0 -2.0</point><elev>3.0</elev><floor>4</floor><featuretypetag>city</featuretypetag>' + \
             '<featurename>Boulder</featurename><relationshiptag>center</relationshiptag></place>' + \
             '<place><point>11.0 -12.0</point><elev>13.0</elev><floor>14</floor><featuretypetag>city</featuretypetag>' + \
             '<featurename>Boulder</featurename><relationshiptag>center</relationshiptag></place>' + \
             '<actor>bob</actor><actor>you</actor><destinationURL>http://example.com</destinationURL>' + \
             '<destinationURL>http://example2.com</destinationURL><tag>trains</tag><tag>planes</tag>' + \
             '<to>you</to><to>fred</to><regardingURL>http://regarding.com</regardingURL>' + \
             '<regardingURL>http://regarding2.com</regardingURL>' + \
             '<payload><title>Title</title><body>Body</body><mediaURL>http://media.com</mediaURL>' + \
             '<mediaURL>http://media2.com</mediaURL><raw>raw</raw></payload></activity></activities>'
        self.gnip.publish_xml(TEST_PUBLISHER, xml)

        resultActivities = self.gnip.get_filter_notifications(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, self.filterName)

        numMatches = 0
        for singleActivity in resultActivities:
            numMatches += count(singleActivity.activity_id, randVal)
        self.assert_(0 != numMatches)

    def testGetFilterNotificationsXml(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, a_filter)
        randVal = str(random.randint(1, 99999999))
        xml = '<?xml version=\'1.0\' encoding=\'utf-8\'?><activities><activity>' + \
             '<at>2008-07-02T11:16:16+00:00</at><action>update</action><activityID>' + randVal + '</activityID>' + \
             '<URL>http://example.com</URL><source>web</source><source>website</source>' + \
             '<place><point>1.0 -2.0</point><elev>3.0</elev><floor>4</floor><featuretypetag>city</featuretypetag>' + \
             '<featurename>Boulder</featurename><relationshiptag>center</relationshiptag></place>' + \
             '<place><point>11.0 -12.0</point><elev>13.0</elev><floor>14</floor><featuretypetag>city</featuretypetag>' + \
             '<featurename>Boulder</featurename><relationshiptag>center</relationshiptag></place>' + \
             '<actor>bob</actor><actor>you</actor><destinationURL>http://example.com</destinationURL>' + \
             '<destinationURL>http://example2.com</destinationURL><tag>trains</tag><tag>planes</tag>' + \
             '<to>you</to><to>fred</to><regardingURL>http://regarding.com</regardingURL>' + \
             '<regardingURL>http://regarding2.com</regardingURL>' + \
             '<payload><title>Title</title><body>Body</body><mediaURL>http://media.com</mediaURL>' + \
             '<mediaURL>http://media2.com</mediaURL><raw>raw</raw></payload></activity></activities>'
        self.gnip.publish_xml(TEST_PUBLISHER, xml)

        resultXml = self.gnip.get_filter_notifications_xml(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, self.filterName)
        self.assert_(randVal in resultXml)
        
    def testUpdateFilter(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, a_filter)
        a_second_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        a_second_filter.rules.append(dict(type="actor", value="joe"))
        result = self.gnip.update_filter(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, a_second_filter)
        self.assertEqual(result, self.success)

    def testUpdateFilterFromXml(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, a_filter)
        updatedXml = '<filter name="test" fullData="true">' + \
            '<rule type="actor">me</rule>' + \
            '<rule type="actor">you</rule>' + \
            '<rule type="actor">bob</rule>' + \
            '<rule type="actor">joe</rule>' + \
            '</filter>'
        result = self.gnip.update_filter_from_xml(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, a_filter.name, updatedXml)
        self.assertEqual(result, self.success)

    def testCreateFilter(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, a_filter)
        result = self.gnip.find_filter_xml(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, self.filterName)
        self.assert_('bob' in result)

    def testDeleteFilter(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, a_filter)
        result = self.gnip.delete_filter(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, self.filterName)
        self.assertEqual(result, self.success)

    def testFindFilter(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, a_filter)
        resultfilter = self.gnip.find_filter(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, self.filterName)
        self.assertEqual(resultfilter.name, a_filter.name)

    def testFindFilterXml(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, a_filter)
        resultXml = self.gnip.find_filter_xml(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER, self.filterName)
        self.assert_("bob" in resultXml)
        
    def testGetPublisher(self):
        pub = self.gnip.get_publisher(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER)
        self.assertEquals(TEST_PUBLISHER, pub.name)
        
    def testGetPublisherXml(self):
        resultXml = self.gnip.get_publisher_xml(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER)
        self.assert_(TEST_PUBLISHER in resultXml)

    def testCreatePublisher(self):
        randVal = str(random.randint(1, 99999999))
        pub = publisher.Publisher(TEST_PUBLISHER + randVal, ['actor', 'tag'])
        self.gnip.create_publisher(pub)
        resultXml = self.gnip.get_publisher_xml(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER + randVal)
        self.assert_(TEST_PUBLISHER + randVal in resultXml)
        
    def testCreatePublisherFromXml(self):
        randVal = str(random.randint(1, 99999999))
        self.publisherXml = '<publisher name="' + TEST_PUBLISHER + randVal + '">' + \
            '<supportedRuleTypes><type>actor</type><type>tag</type>' + \
            '</supportedRuleTypes></publisher>'

        resultXml = self.gnip.create_publisher_from_xml(TEST_PUBLISHER, self.publisherXml)
        resultXml = self.gnip.get_publisher_xml(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER + randVal)
        self.assert_(TEST_PUBLISHER + randVal in resultXml)
        
    def testUpdatePublisher(self):
        pub = publisher.Publisher(TEST_PUBLISHER, ['actor', 'tag'])
        self.gnip.update_publisher(pub)
        resultXml = self.gnip.get_publisher_xml(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER)
        self.assert_('<type>tag</type>' in resultXml)
        
    def testUpdatePublisherFromXml(self):
        self.publisherXml = '<publisher name="' + TEST_PUBLISHER + '">' + \
            '<supportedRuleTypes><type>actor</type>' + \
            '</supportedRuleTypes></publisher>'
        resultXml = self.gnip.update_publisher_from_xml(TEST_PUBLISHER, self.publisherXml)
        resultXml = self.gnip.get_publisher_xml(TEST_PUBLISHER_SCOPE, TEST_PUBLISHER)
        self.assert_('<type>tag</type>' not in resultXml)

if __name__ == '__main__':
    unittest.main()

