import unittest
import datetime
import activity
from xml.dom.minidom import parseString

class ActivityTestCase(unittest.TestCase):
    def setUp(self):
        self.xml_without_payload = open("activity_without_payload.xml").read()
        self.xml_with_payload = open("activity_with_payload.xml").read()
        
        self.testTimeStringValue = "2001-01-01T01:01:00.000Z"
        self.testActionValue = "the_action"
        self.testRuleType = "actor"
        self.testRuleValue = "the_actor"
        self.testActorMetaURL = "actor_metaURL"
        self.testActorValue = "the_actor"
        self.testTitleValue = "the_title"
        self.testBodyValue = "the_body"
        self.testDestURLMetaURL = "destURL_metaURL"
        self.testDestURLValue = "the_destURL"
        self.testSourceValue = "the_source"
        self.testToValue = "the_to"
        self.testToMetaURL = "to_metaURL"
        self.testGeoValue = "the_geo"
        self.testRegardingURLMetaURL = "regardingURL_metaURL"
        self.testRegardingURLValue = "the_regardingURL"
        self.testMediaURLMetaURL1 = "mediaURL_metaURL_1"
        self.testMediaUrlValue1 = "the_mediaURL_1"
        self.testMediaURLMetaURL2 = "mediaURL_metaURL_2"
        self.testMediaUrlValue2 = "the_mediaURL_2" 
        self.testTagMetaURL1 = "tag_metaURL_1"
        self.testTagValue1 = "tag_metaURL_1"
        self.testTagMetaURL2 = "tag_metaURL_2"
        self.testTagValue2 = "tag_metaURL_2"   
        self.testRaw = "the_raw"   
        

    def tearDown(self):
        pass

    def testTimeStringConversionFromDatetime(self):
        currentTime = datetime.datetime.now()
        activity1 = activity.Activity(at=currentTime)
        self.assertEqual(activity1.at, currentTime)

        timeString1 = activity1.get_at_as_string()
        activity2 = activity.Activity()
        activity2.set_at_from_string(timeString1)
        timeString2 = activity2.get_at_as_string()
        self.assertEqual(timeString1, timeString2)

    def testTimeStringConversionFromString(self):
        activity1 = activity.Activity()
        activity1.set_at_from_string(self.testTimeStringValue)
        activity2 = activity.Activity(at=activity1.at)
        self.assertEqual(activity2.get_at_as_string(), self.testTimeStringValue)

    def testFromXmlWithoutPayload(self):
        an_activity = activity.Activity()
        an_activity.from_xml(self.xml_without_payload)

        self.assertEqual(an_activity.get_at_as_string(), self.testTimeStringValue)
        self.assertEqual(an_activity.action["value"], self.testActionValue)
        self.assertEqual(an_activity.rule["type"], self.testRuleType)
        self.assertEqual(an_activity.rule["value"], self.testRuleValue)

    def testToXmlWithoutPayload(self):        
        an_activity = activity.Activity(action=dict(value=self.testActionValue), 
                                        rule=dict(type=self.testRuleType, value=self.testRuleValue))
        an_activity.set_at_from_string(self.testTimeStringValue)

        self.assertEqual(an_activity.to_xml(), self.xml_without_payload)

    def testFromXmlWithPayload(self):
        an_activity = activity.Activity()
        an_activity.from_xml(self.xml_with_payload)

        self.assertEqual(an_activity.get_at_as_string(), self.testTimeStringValue)
        self.assertEqual(an_activity.action["value"], self.testActionValue)
        self.assertEqual(an_activity.rule["type"], self.testRuleType)
        self.assertEqual(an_activity.rule["value"], self.testRuleValue)
        self.assertEqual(an_activity.actor["meta_url"], self.testActorMetaURL)
        self.assertEqual(an_activity.actor["value"], self.testActorValue)
        self.assertEqual(an_activity.title["value"], self.testTitleValue)
        self.assertEqual(an_activity.body["value"], self.testBodyValue)
        self.assertEqual(an_activity.dest_url["meta_url"], self.testDestURLMetaURL)
        self.assertEqual(an_activity.dest_url["value"], self.testDestURLValue)
        self.assertEqual(an_activity.source["value"], self.testSourceValue)
        self.assertEqual(an_activity.to["value"], self.testToValue)
        self.assertEqual(an_activity.to["meta_url"], self.testToMetaURL)
        self.assertEqual(an_activity.geo["value"], self.testGeoValue)
        self.assertEqual(an_activity.regarding_url["meta_url"], self.testRegardingURLMetaURL)
        self.assertEqual(an_activity.regarding_url["value"], self.testRegardingURLValue)
        self.assertEqual(an_activity.media_urls[0]["meta_url"], self.testMediaURLMetaURL1)
        self.assertEqual(an_activity.media_urls[0]["value"], self.testMediaUrlValue1)
        self.assertEqual(an_activity.media_urls[1]["meta_url"], self.testMediaURLMetaURL2)
        self.assertEqual(an_activity.media_urls[1]["value"], self.testMediaUrlValue2)
        self.assertEqual(an_activity.tags[0]["meta_url"], self.testTagMetaURL1)
        self.assertEqual(an_activity.tags[0]["value"], self.testTagValue1)
        self.assertEqual(an_activity.tags[1]["meta_url"], self.testTagMetaURL2)
        self.assertEqual(an_activity.tags[1]["value"], self.testTagValue2)  
        self.assertEqual(an_activity.raw["value"], self.testRaw)            

    def testToXmlWithPayload(self):
        an_activity = activity.Activity(action=dict(value=self.testActionValue), 
                                        rule=dict(type=self.testRuleType, value=self.testRuleValue),
                                        actor=dict(meta_url=self.testActorMetaURL, value=self.testActorValue),
                                        title=dict(value=self.testTitleValue),
                                        body=dict(value=self.testBodyValue),
                                        dest_url=dict(meta_url=self.testDestURLMetaURL, value=self.testDestURLValue),
                                        source=dict(value=self.testSourceValue),
                                        to=dict(meta_url=self.testToMetaURL, value=self.testToValue),
                                        geo=dict(value=self.testGeoValue),
                                        regarding_url=dict(meta_url=self.testRegardingURLMetaURL, value=self.testRegardingURLValue),
                                        media_urls=[dict(meta_url=self.testMediaURLMetaURL1, value=self.testMediaUrlValue1), dict(meta_url=self.testMediaURLMetaURL2, value=self.testMediaUrlValue2)],
                                        tags=[dict(meta_url=self.testTagMetaURL1, value=self.testTagValue1), dict(meta_url=self.testTagMetaURL2, value=self.testTagValue2)],
                                        raw=dict(value=self.testRaw))
        an_activity.set_at_from_string(self.testTimeStringValue)

        self.assertEqual(an_activity.to_xml(), self.xml_with_payload)

if __name__ == '__main__':
    unittest.main()        
