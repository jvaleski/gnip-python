import sys
sys.path.append("../")

from gnip import *
from gnip.xml_objects import *

from string import count
from xml.dom.minidom import parseString
import unittest
import time
import random
from pyjavaproperties import Properties

class GnipTestCase(unittest.TestCase):
        
    def __init__(self,*args):
        unittest.TestCase.__init__(self, *args)
        index = int(__file__.rfind("/"))
        basedir = __file__[0:index]

        p = Properties()
        p.load(open(basedir + '/gnip_account.properties'))
        p.load(open(basedir + '/test.properties'))
        self.gnip = Gnip(p['gnip.username'], p['gnip.password'], p['gnip.server'])
        self.testpublisher = p['gnip.test.publisher']
        self.testpublisherscope = p['gnip.test.publisher.scope']
        self.success = Result('Success')
        self.filterXml = None
        self.rules = None
        self.filterName = None
        self.filterFullData = None
    
    def setUp(self):
        self.gnip.tunnel_over_post = False
        self.filterXml = \
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>' +\
            '<filter fullData="true" name="test">' + \
            '<rule type="actor">me</rule>' + \
            '<rule type="actor">you</rule>' + \
            '<rule type="actor">bob</rule>' + \
            '</filter>'
        self.rules = [Rule(type="actor", value="me"), Rule(type="actor", value="you"), Rule(type="actor", value="bob")]
        self.filterName = "test"
        self.filterFullData = False
        

    def tearDown(self):
        self.gnip.delete_filter(self.testpublisherscope, self.testpublisher, self.filterName)

#    def testCompressUncompress(self):
#        string = "BlahBlah"
#        compressed = self.gnip.__compress_with_gzip(string)
#        uncompressed = self.gnip.__decompress_gzip(compressed)
#        self.assertEqual(string, uncompressed)

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
        response = self.gnip.publish_activities(self.testpublisher, activities.Activities([an_activity]))
        self.assertEqual(200, response.code)
        self.assertEqual(self.success, response.result)

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
        a = activities.Activities()
        a.from_xml(xml)
        response = self.gnip.publish_activities(self.testpublisher, a)
        self.assertEqual(200, response.code)
        self.assertEqual(self.success, response.result)

        response = self.gnip.get_publisher_notifications(self.testpublisherscope, self.testpublisher)
        self.assertEquals(200, response.code)

        numMatches = 0
        for singleActivity in response.result.items:
            numMatches += count(singleActivity.activity_id, randVal)
        self.assert_(0 != numMatches)

    def testGetFilterNotifications(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(self.testpublisherscope, self.testpublisher, a_filter)
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
        a = activities.Activities()
        a.from_xml(xml)
        response = self.gnip.publish_activities(self.testpublisher, a)
        self.assertEqual(200, response.code)
        self.assertEqual(self.success, response.result)

        response = self.gnip.get_filter_notifications(self.testpublisherscope, self.testpublisher, self.filterName)
        self.assertEquals(200, response.code)
        
        numMatches = 0
        for singleActivity in response.result.items:
            numMatches += count(singleActivity.activity_id, randVal)
        self.assert_(0 != numMatches)

    def testUpdateFilter(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(self.testpublisherscope, self.testpublisher, a_filter)
        a_second_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        a_second_filter.rules.append(Rule(type="actor", value="joe"))
        response = self.gnip.update_filter(self.testpublisherscope, self.testpublisher, a_second_filter)
        self.assertEqual(200, response.code)
        self.assertEqual(self.success, response.result)

    def testUpdateFilterOverPost(self):
        self.gnip.tunnel_over_post = True
        self.testUpdateFilter()

    def testDeleteRuleFromFilter(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(self.testpublisherscope, self.testpublisher, a_filter)
        expected_rule = Rule(type="actor", value="you")
        response = self.gnip.remove_rule_from_filter(self.testpublisherscope, self.testpublisher, a_filter.name, expected_rule)
        self.assertEqual(200, response.code)
        self.assertEqual(self.success, response.result)

        a_filter_with_new_rule = self.gnip.find_filter(self.testpublisherscope, self.testpublisher, a_filter.name).result
        self.assertFalse(expected_rule in a_filter_with_new_rule.rules)

    def testDeleteRuleFromFilterOverPost(self):
        self.gnip.tunnel_over_post = True
        self.testDeleteRuleFromFilter()

    def testRuleSearchFromFilter(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(self.testpublisherscope, self.testpublisher, a_filter)
        existing_rule = Rule(type="actor", value="you")
        missing_rule = Rule(type="actor", value="jud")
        invalid_rule = Rule(type="", value="")
        response = self.gnip.rule_exists_in_filter(self.testpublisherscope, self.testpublisher, a_filter.name, existing_rule)
        self.assertTrue(response)
        response = self.gnip.rule_exists_in_filter(self.testpublisherscope, self.testpublisher, a_filter.name, missing_rule)
        self.assertFalse(response)
        response = self.gnip.rule_exists_in_filter(self.testpublisherscope, self.testpublisher, a_filter.name, invalid_rule)
        self.assertTrue(response is None)

    def testAddSingleRuleUpdateToFilter(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(self.testpublisherscope, self.testpublisher, a_filter)
        expected_rule = Rule(type="actor", value="jud")
        response = self.gnip.add_rule_to_filter(self.testpublisherscope, self.testpublisher, a_filter.name, expected_rule)
        self.assertEqual(200, response.code)
        self.assertEqual(self.success, response.result)
        a_filter_with_new_rule = self.gnip.find_filter(self.testpublisherscope, self.testpublisher, a_filter.name).result
        self.assertTrue(expected_rule in a_filter_with_new_rule.rules)

    def testAddBatchUpdateOfFilterRules(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(self.testpublisherscope, self.testpublisher, a_filter)
        new_rules = [Rule("actor","jud"), Rule("actor","eddie"), Rule("actor","alex")]
        response = self.gnip.add_rules_to_filter(self.testpublisherscope, self.testpublisher, a_filter.name, new_rules)
        self.assertEqual(200, response.code)
        self.assertEqual(self.success, response.result)
        a_filter_with_new_rule = self.gnip.find_filter(self.testpublisherscope, self.testpublisher, a_filter.name).result
        for new_rule in new_rules:
            self.assertTrue(new_rule in a_filter_with_new_rule.rules)

    def testCreateFilter(self):
        expected_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(self.testpublisherscope, self.testpublisher, expected_filter)
        response = self.gnip.find_filter(self.testpublisherscope, self.testpublisher, self.filterName)
        self.assertEqual(200, response.code)
        self.assertEquals(expected_filter,response.result)

    def testDeleteFilter(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(self.testpublisherscope, self.testpublisher, a_filter)
        response = self.gnip.delete_filter(self.testpublisherscope, self.testpublisher, self.filterName)
        self.assertEqual(200, response.code)
        self.assertEqual(self.success, response.result)

    def testDeleteFilterOverPost(self):
        self.gnip.tunnel_over_post = True
        self.testDeleteFilter()

    def testFindFilter(self):
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.gnip.create_filter(self.testpublisherscope, self.testpublisher, a_filter)
        response = self.gnip.find_filter(self.testpublisherscope, self.testpublisher, self.filterName)
        self.assertEqual(200, response.code)
        self.assertEqual(a_filter.name, response.result.name)
        
    def testGetPublisher(self):
        response = self.gnip.get_publisher(self.testpublisherscope, self.testpublisher)
        self.assertEqual(200, response.code)
        self.assertEquals(self.testpublisher, response.result.name)

#    def testCreatePublisher(self):
#        randVal = str(random.randint(1, 99999999))
#        expected_publisher = publisher.Publisher(self.testpublisher + randVal, ['actor', 'tag'])
#        self.gnip.create_publisher(expected_publisher)
#
#        response = self.gnip.get_publisher(self.testpublisherscope, self.testpublisher + randVal)
#        self.assertEqual(200, response.code)
#        self.assertEquals(expected_publisher, response.result)
        
    def testUpdatePublisher(self):
        expected_publisher = publisher.Publisher(self.testpublisher, ['actor', 'tag'])
        self.gnip.update_publisher(expected_publisher)
        response = self.gnip.get_publisher(self.testpublisherscope, self.testpublisher)
        self.assertEqual(200, response.code)
        self.assertEquals(expected_publisher, response.result)

    def testUpdatePublisherOverPost(self):
        self.gnip.tunnel_over_post = True
        self.testUpdatePublisher()

if __name__ == '__main__':
    unittest.main()

