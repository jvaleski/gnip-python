import sys
import unittest
import datetime
import logging
import re
import StringIO
import gzip
import base64
from xml.dom.minidom import parseString
sys.path.append("../")
from gnip import activity
from gnip import payload
from gnip import place
from gnip.xml_objects import *

class ActivityTestCase(unittest.TestCase):
    
    def setUp(self):
        logging.getLogger('').setLevel(logging.WARN)
        index = int(__file__.rfind("/"))
        if index >= 0:
            basedir = __file__[0:index]
        else:
            basedir = "./"
        logging.info("Loading XML files from " + basedir)

        self.xml_without_payload = open(basedir + "/activity_without_payload.xml").read()
        self.xml_with_payload = open(basedir + "/activity_with_payload.xml").read()
        
        self.testTimeStringValue = "2001-01-01T01:01:00.000Z"
        self.testActionValue = "the_action"
        self.testActivityIdValue = "the_activityID"
        self.testURLValue = "the_URL"
        self.testSource1Value = "the_source_1"
        self.testSource2Value = "the_source_2"

        self.testPlacePointX1 = 1.0
        self.testPlacePointY1 = -2.0
        self.testPlaceElev1 = 3.0
        self.testPlaceFloor1 = 4
        self.testPlaceFeatureTypeTag1 = "the_featuretypetag_1"
        self.testPlaceFeatureName1 = "the_featurename_1"
        self.testPlaceRelationshipTag1 = "the_relationshiptag_1"

        self.testPlacePointX2 = 11.0
        self.testPlacePointY2 = -12.0
        self.testPlaceElev2 = 13.0
        self.testPlaceFloor2 = 14
        self.testPlaceFeatureTypeTag2 = "the_featuretypetag_2"
        self.testPlaceFeatureName2 = "the_featurename_2"
        self.testPlaceRelationshipTag2 = "the_relationshiptag_2"

        self.testActorMetaURL1 = "actor_metaURL_1"
        self.testActorUid1 = "actor_uid_1"
        self.testActorValue1 = "the_actor_1"        
        self.testActorMetaURL2 = "actor_metaURL_2"
        self.testActorUid2 = "actor_uid_2"
        self.testActorValue2 = "the_actor_2"
        self.testDestinationURLMetaURL1 = "destinationURL_metaURL_1"
        self.testDestinationURLValue1 = "the_destinationURL_1"
        self.testDestinationURLMetaURL2 = "destinationURL_metaURL_2"
        self.testDestinationURLValue2 = "the_destinationURL_2"
        self.testTagMetaURL1 = "tag_metaURL_1"
        self.testTagValue1 = "tag_metaURL_1"
        self.testTagMetaURL2 = "tag_metaURL_2"
        self.testTagValue2 = "tag_metaURL_2"          
        self.testToValue1 = "the_to_1"
        self.testToMetaURL1 = "to_metaURL_1"
        self.testToValue2 = "the_to_2"
        self.testToMetaURL2 = "to_metaURL_2" 
        self.testRegardingURLMetaURL1 = "regardingURL_metaURL_1"
        self.testRegardingURLValue1 = "the_regardingURL_1" 
        self.testRegardingURLMetaURL2 = "regardingURL_metaURL_2"
        self.testRegardingURLValue2 = "the_regardingURL_2"

        self.testTitleValue = "the_title"            
        self.testBodyValue = "the_body"
        self.testMediaURLMetaURL1 = "mediaURL_metaURL_1"
        self.testMediaUrlValue1 = "the_mediaURL_1"
        self.testMediaURLMetaURL2 = "mediaURL_metaURL_2"
        self.testMediaUrlValue2 = "the_mediaURL_2" 
        self.testRaw = "the_raw"   
        
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
        self.assertEqual(an_activity.action, self.testActionValue)
        self.assertEqual(an_activity.activity_id, self.testActivityIdValue)
        self.assertEqual(an_activity.url, self.testURLValue)
        self.assertEqual(an_activity.sources[0], self.testSource1Value)
        self.assertEqual(an_activity.sources[1], self.testSource2Value)

        self.assertEqual(an_activity.places[0].point.x, self.testPlacePointX1)
        self.assertEqual(an_activity.places[0].point.y, self.testPlacePointY1)
        self.assertEqual(an_activity.places[0].elev, self.testPlaceElev1)
        self.assertEqual(an_activity.places[0].floor, self.testPlaceFloor1)
        self.assertEqual(an_activity.places[0].feature_type_tag, self.testPlaceFeatureTypeTag1)
        self.assertEqual(an_activity.places[0].feature_name, self.testPlaceFeatureName1)
        self.assertEqual(an_activity.places[0].relationship_tag, self.testPlaceRelationshipTag1)

        self.assertEqual(an_activity.places[1].point.x, self.testPlacePointX2)
        self.assertEqual(an_activity.places[1].point.y, self.testPlacePointY2)
        self.assertEqual(an_activity.places[1].elev, self.testPlaceElev2)
        self.assertEqual(an_activity.places[1].floor, self.testPlaceFloor2)
        self.assertEqual(an_activity.places[1].feature_type_tag, self.testPlaceFeatureTypeTag2)
        self.assertEqual(an_activity.places[1].feature_name, self.testPlaceFeatureName2)
        self.assertEqual(an_activity.places[1].relationship_tag, self.testPlaceRelationshipTag2)

        self.assertEqual(an_activity.actors[0].meta_url, self.testActorMetaURL1)
        self.assertEqual(an_activity.actors[0].uid, self.testActorUid1)
        self.assertEqual(an_activity.actors[0].value, self.testActorValue1)        
        self.assertEqual(an_activity.actors[1].meta_url, self.testActorMetaURL2)
        self.assertEqual(an_activity.actors[1].uid, self.testActorUid2)
        self.assertEqual(an_activity.actors[1].value, self.testActorValue2)            
        self.assertEqual(an_activity.destination_urls[0].meta_url, self.testDestinationURLMetaURL1)
        self.assertEqual(an_activity.destination_urls[0].value, self.testDestinationURLValue1)        
        self.assertEqual(an_activity.destination_urls[1].meta_url, self.testDestinationURLMetaURL2)
        self.assertEqual(an_activity.destination_urls[1].value, self.testDestinationURLValue2)  
        self.assertEqual(an_activity.tags[0].meta_url, self.testTagMetaURL1)
        self.assertEqual(an_activity.tags[0].value, self.testTagValue1)
        self.assertEqual(an_activity.tags[1].meta_url, self.testTagMetaURL2)
        self.assertEqual(an_activity.tags[1].value, self.testTagValue2)  
        self.assertEqual(an_activity.tos[0].meta_url, self.testToMetaURL1)
        self.assertEqual(an_activity.tos[0].value, self.testToValue1)
        self.assertEqual(an_activity.tos[1].meta_url, self.testToMetaURL2)
        self.assertEqual(an_activity.tos[1].value, self.testToValue2)     
        self.assertEqual(an_activity.regarding_urls[0].meta_url, self.testRegardingURLMetaURL1)
        self.assertEqual(an_activity.regarding_urls[0].value, self.testRegardingURLValue1)
        self.assertEqual(an_activity.regarding_urls[1].meta_url, self.testRegardingURLMetaURL2)
        self.assertEqual(an_activity.regarding_urls[1].value, self.testRegardingURLValue2)     

    def testToXmlWithoutPayload(self):

        a_place1 = place.Place(Point(self.testPlacePointX1, self.testPlacePointY1), self.testPlaceElev1, self.testPlaceFloor1,
                               self.testPlaceFeatureTypeTag1, self.testPlaceFeatureName1, self.testPlaceRelationshipTag1)

        a_place2 = place.Place(Point(self.testPlacePointX2, self.testPlacePointY2), self.testPlaceElev2, self.testPlaceFloor2,
                               self.testPlaceFeatureTypeTag2, self.testPlaceFeatureName2, self.testPlaceRelationshipTag2)

        an_activity = activity.Activity(action=self.testActionValue,
                                        activity_id=self.testActivityIdValue,
                                        url=self.testURLValue,
                                        sources=[self.testSource1Value, self.testSource2Value],
                                        places=[a_place1, a_place2],
                                        actors=[Actor(value=self.testActorValue1, meta_url=self.testActorMetaURL1, uid=self.testActorUid1),
                                                Actor(value=self.testActorValue2, meta_url=self.testActorMetaURL2, uid=self.testActorUid2)],
                                        destination_urls=[URL(value=self.testDestinationURLValue1, meta_url=self.testDestinationURLMetaURL1),
                                                          URL(value=self.testDestinationURLValue2, meta_url=self.testDestinationURLMetaURL2)],
                                        tags=[Tag(meta_url=self.testTagMetaURL1, value=self.testTagValue1),
                                              Tag(meta_url=self.testTagMetaURL2, value=self.testTagValue2)],
                                        tos=[To(value=self.testToValue1, meta_url=self.testToMetaURL1),
                                             To(value=self.testToValue2, meta_url=self.testToMetaURL2)],
                                        regarding_urls=[URL(value=self.testRegardingURLValue1, meta_url=self.testRegardingURLMetaURL1),
                                                        URL(value=self.testRegardingURLValue2, meta_url=self.testRegardingURLMetaURL2)])
        
        an_activity.set_at_from_string(self.testTimeStringValue)

        self.assertEqual(an_activity.to_xml(), self.xml_without_payload)

    def testFromXmlWithPayload(self):
        an_activity = activity.Activity()
        an_activity.from_xml(self.xml_with_payload)
                      
        self.assertEqual(an_activity.get_at_as_string(), self.testTimeStringValue)
        self.assertEqual(an_activity.action, self.testActionValue)
        self.assertEqual(an_activity.activity_id, self.testActivityIdValue)
        self.assertEqual(an_activity.url, self.testURLValue)
        self.assertEqual(an_activity.sources[0], self.testSource1Value)
        self.assertEqual(an_activity.sources[1], self.testSource2Value)

        self.assertEqual(an_activity.places[0].point.x, self.testPlacePointX1)
        self.assertEqual(an_activity.places[0].point.y, self.testPlacePointY1)
        self.assertEqual(an_activity.places[0].elev, self.testPlaceElev1)
        self.assertEqual(an_activity.places[0].floor, self.testPlaceFloor1)
        self.assertEqual(an_activity.places[0].feature_type_tag, self.testPlaceFeatureTypeTag1)
        self.assertEqual(an_activity.places[0].feature_name, self.testPlaceFeatureName1)
        self.assertEqual(an_activity.places[0].relationship_tag, self.testPlaceRelationshipTag1)

        self.assertEqual(an_activity.places[1].point.x, self.testPlacePointX2)
        self.assertEqual(an_activity.places[1].point.y, self.testPlacePointY2)
        self.assertEqual(an_activity.places[1].elev, self.testPlaceElev2)
        self.assertEqual(an_activity.places[1].floor, self.testPlaceFloor2)
        self.assertEqual(an_activity.places[1].feature_type_tag, self.testPlaceFeatureTypeTag2)
        self.assertEqual(an_activity.places[1].feature_name, self.testPlaceFeatureName2)
        self.assertEqual(an_activity.places[1].relationship_tag, self.testPlaceRelationshipTag2)

        self.assertEqual(an_activity.actors[0].meta_url, self.testActorMetaURL1)
        self.assertEqual(an_activity.actors[0].uid, self.testActorUid1)
        self.assertEqual(an_activity.actors[0].value, self.testActorValue1)
        self.assertEqual(an_activity.actors[1].meta_url, self.testActorMetaURL2)
        self.assertEqual(an_activity.actors[1].uid, self.testActorUid2)
        self.assertEqual(an_activity.actors[1].value, self.testActorValue2)               
        self.assertEqual(an_activity.destination_urls[0].meta_url, self.testDestinationURLMetaURL1)
        self.assertEqual(an_activity.destination_urls[0].value, self.testDestinationURLValue1)        
        self.assertEqual(an_activity.destination_urls[1].meta_url, self.testDestinationURLMetaURL2)
        self.assertEqual(an_activity.destination_urls[1].value, self.testDestinationURLValue2)  
        self.assertEqual(an_activity.tags[0].meta_url, self.testTagMetaURL1)
        self.assertEqual(an_activity.tags[0].value, self.testTagValue1)
        self.assertEqual(an_activity.tags[1].meta_url, self.testTagMetaURL2)
        self.assertEqual(an_activity.tags[1].value, self.testTagValue2)  
        self.assertEqual(an_activity.tos[0].meta_url, self.testToMetaURL1)
        self.assertEqual(an_activity.tos[0].value, self.testToValue1)
        self.assertEqual(an_activity.tos[1].meta_url, self.testToMetaURL2)
        self.assertEqual(an_activity.tos[1].value, self.testToValue2)     
        self.assertEqual(an_activity.regarding_urls[0].meta_url, self.testRegardingURLMetaURL1)
        self.assertEqual(an_activity.regarding_urls[0].value, self.testRegardingURLValue1)
        self.assertEqual(an_activity.regarding_urls[1].meta_url, self.testRegardingURLMetaURL2)
        self.assertEqual(an_activity.regarding_urls[1].value, self.testRegardingURLValue2)
        
        self.assertEqual(an_activity.payload.title, self.testTitleValue)
        self.assertEqual(an_activity.payload.body, self.testBodyValue)
        self.assertEqual(an_activity.payload.media_urls[0].value, self.testMediaUrlValue1)
        self.assertEqual(an_activity.payload.media_urls[0].meta_url, self.testMediaURLMetaURL1)
        self.assertEqual(an_activity.payload.media_urls[1].meta_url, self.testMediaURLMetaURL2)
        self.assertEqual(an_activity.payload.media_urls[1].value, self.testMediaUrlValue2)

        self.assertEqual(an_activity.payload.read_raw(), self.testRaw)            

    def testToXmlWithPayload(self):
        a_place1 = place.Place(Point(self.testPlacePointX1, self.testPlacePointY1), self.testPlaceElev1, self.testPlaceFloor1,
                               self.testPlaceFeatureTypeTag1, self.testPlaceFeatureName1, self.testPlaceRelationshipTag1)

        a_place2 = place.Place(Point(self.testPlacePointX2, self.testPlacePointY2), self.testPlaceElev2, self.testPlaceFloor2,
                               self.testPlaceFeatureTypeTag2, self.testPlaceFeatureName2, self.testPlaceRelationshipTag2)

        a_payload = payload.Payload(title=self.testTitleValue,
                                        body=self.testBodyValue,
                                        media_urls=[URL(value=self.testMediaUrlValue1, meta_url=self.testMediaURLMetaURL1),
                                                    URL(value=self.testMediaUrlValue2, meta_url=self.testMediaURLMetaURL2)],
                                        raw=self.testRaw)

        an_activity = activity.Activity(action=self.testActionValue, 
                                        activity_id=self.testActivityIdValue,
                                        url=self.testURLValue,
                                        sources=[self.testSource1Value, self.testSource2Value],
                                        places=[a_place1, a_place2],
                                        actors=[Actor(value=self.testActorValue1, meta_url=self.testActorMetaURL1, uid=self.testActorUid1),
                                                Actor(value=self.testActorValue2, meta_url=self.testActorMetaURL2, uid=self.testActorUid2)],
                                        destination_urls=[URL(value=self.testDestinationURLValue1, meta_url=self.testDestinationURLMetaURL1),
                                                          URL(value=self.testDestinationURLValue2, meta_url=self.testDestinationURLMetaURL2)],
                                        tags=[Tag(meta_url=self.testTagMetaURL1, value=self.testTagValue1),
                                              Tag(meta_url=self.testTagMetaURL2, value=self.testTagValue2)],
                                        tos=[To(value=self.testToValue1, meta_url=self.testToMetaURL1),
                                             To(value=self.testToValue2, meta_url=self.testToMetaURL2)],
                                        regarding_urls=[URL(value=self.testRegardingURLValue1, meta_url=self.testRegardingURLMetaURL1),
                                                        URL(value=self.testRegardingURLValue2, meta_url=self.testRegardingURLMetaURL2)],
                                        payload=a_payload)
        an_activity.set_at_from_string(self.testTimeStringValue)

        extract_raw = "(.*<raw>)(.*)(</raw>.*)" 
        actual = re.match(extract_raw, an_activity.to_xml())
        expected = re.match(extract_raw, self.xml_with_payload)
        
        self.assertEqual(actual.group(1) + actual.group(3), expected.group(1) + expected.group(3))
        self.assertEqual(self.__decode_and_ungzip(actual.group(2)), self.__decode_and_ungzip(expected.group(2)))

    def __decode_and_ungzip(self, data):
        decoded = base64.b64decode(data)
        zbuf = StringIO.StringIO(decoded)
        zfile = gzip.GzipFile(fileobj=zbuf)
        return zfile.read()        

if __name__ == '__main__':
    unittest.main()