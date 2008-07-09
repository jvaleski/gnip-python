import unittest
from gnip import *
from xml.dom.minidom import parseString

# Be sure to fill these in if you want to run the test cases
TEST_USERNAME = ""
TEST_PASSWORD = ""
TEST_PUBLISHER = ""

class ActivityTestCase(unittest.TestCase):
    def setUp(self):
        self.timeString = "2008-01-01T12:00:00+00:00"
        self.xml = '<activity at="' + self.timeString + '" type="test" ' + \
            'uid="me" guid="1234"/>'
        self.testUid = "me"
        self.testType = "test"
        self.testGuid = "1234"

    def tearDown(self):
        pass

    def testTimeStringConversion(self):
        currentTime = datetime.datetime.now()
        activity1 = Activity(self.testUid, currentTime, 
                                 self.testType, self.testGuid)
        self.assertEqual(activity1.at, currentTime)

        timeString1 = activity1.get_at_as_string()
        activity2 = Activity()
        activity2.set_at_from_string(timeString1)
        timeString2 = activity2.get_at_as_string()
        self.assertEqual(timeString1, timeString2)

    def testFromXml(self):  
        activity = Activity()
        activity.from_xml(self.xml)

        self.assertEqual(activity.uid, self.testUid)
        self.assertEqual(activity.get_at_as_string(), self.timeString)
        self.assertEqual(activity.type, self.testType)
        self.assertEqual(activity.guid, self.testGuid)

    def testFromNode(self):
        node = parseString(self.xml).documentElement
        activity = Activity()
        activity.from_node(node)

        self.assertEqual(activity.uid, self.testUid)
        self.assertEqual(activity.get_at_as_string(), self.timeString)
        self.assertEqual(activity.type, self.testType)
        self.assertEqual(activity.guid, self.testGuid)

    def testToXml(self):
        activity = Activity(self.testUid, None, self.testType, 
                                self.testGuid)
        activity.set_at_from_string(self.timeString)

        self.assertEqual(activity.to_xml(), self.xml)

class CollectionTestCase(unittest.TestCase):
    def setUp(self):
        self.xml = '<collection name="test">' + \
            '<uid publisher.name="' + TEST_PUBLISHER + '" name="me"/>' + \
            '<uid publisher.name="' + TEST_PUBLISHER + '" name="you"/>' + \
            '<uid publisher.name="' + TEST_PUBLISHER + '" name="bob"/>' + \
            '</collection>'
        self.user_ids = [[TEST_PUBLISHER, "me"], 
                         [TEST_PUBLISHER, "you"], 
                         [TEST_PUBLISHER, "bob"]]
        self.collectionName = "test"

    def tearDown(self):
        pass

    def testFromXml(self):
        collection = Collection()
        collection.from_xml(self.xml)

        self.assertEquals(collection.name, self.collectionName)
        self.assertEquals(collection.user_ids, self.user_ids)

    def testToXml(self):
        collection = Collection(self.collectionName, self.user_ids)
        self.assertEqual(collection.to_xml(), self.xml)


class GnipTestCase(unittest.TestCase):
    def setUp(self):
        self.gnip = Gnip(TEST_USERNAME, TEST_PASSWORD)
        self.collectionXml = '<?xml version="1.0" encoding="UTF-8"' +\
            ' standalone="yes"?>' +\
            '<collection name="test">' + \
            '<uid publisher.name="' + TEST_PUBLISHER + '" name="me"/>' + \
            '<uid publisher.name="' + TEST_PUBLISHER + '" name="you"/>' + \
            '<uid publisher.name="' + TEST_PUBLISHER + '" name="bob"/>' + \
            '</collection>'
        self.user_ids = [[TEST_PUBLISHER, "me"], 
                         [TEST_PUBLISHER, "you"], 
                         [TEST_PUBLISHER, "bob"]]
        self.collectionName = "test"
        self.success = '<result>Success</result>'

    def tearDown(self):
        self.gnip.delete_collection(self.collectionName)

    def testPublishXml(self):
        xml = '<activities><activity at="2008-01-01T12:00:00+00:00"' + \
            ' type="test" uid="me" guid="1234"/></activities>'
        result = self.gnip.publish_xml(TEST_PUBLISHER, xml)
        self.assertEqual(result, self.success)       

    def testPublishActivities(self):
        activity = Activity("me", None, "test", "1234")
        activity.set_at_from_string("2008-01-01T12:00:00+00:00")
        result = self.gnip.publish_activities(TEST_PUBLISHER, [activity])
        self.assertEqual(result, self.success)

    def testCreateCollection(self):
        collection = Collection(self.collectionName, self.user_ids)
        result = self.gnip.create_collection(collection)
        self.assertEqual(result, self.success)

    def testCreateCollectionFromXml(self):
        result = self.gnip.create_collection_from_xml(
            self.collectionName, self.collectionXml)
        self.assertEqual(result, self.success)

    def testDeleteCollection(self):
        collection = Collection(self.collectionName, self.user_ids)
        self.gnip.create_collection(collection)
        result = self.gnip.delete_collection(self.collectionName)
        self.assertEqual(result, self.success)

    def testFindCollection(self):
        collection = Collection(self.collectionName, self.user_ids)
        self.gnip.create_collection(collection)
        resultCollection = self.gnip.find_collection(self.collectionName)
        self.assertEqual(resultCollection.name, collection.name)
        self.assertEqual(resultCollection.user_ids, collection.user_ids)

    def testFindCollectionXml(self):
        collection = Collection(self.collectionName, self.user_ids)
        self.gnip.create_collection(collection)
        resultXml = self.gnip.find_collection_xml(self.collectionName)
        self.assertEqual(resultXml, self.collectionXml)

    def testGetPublisherActivities(self):
        xml = '<activities><activity at="2008-01-01T12:00:00+00:00"' +\
            ' type="test" uid="me" guid="1234"/></activities>'
        self.gnip.publish_xml(TEST_PUBLISHER, xml)

        resultActivities = self.gnip.get_publisher_activities(
            TEST_PUBLISHER)
        numMatches = 0
        for activity in resultActivities:
            timeString = activity.get_at_as_string()
            numMatches += count(timeString, "2008-01-01T12:00:00")
        self.assert_(0 != numMatches)

    def testGetPublisherXml(self):
        publishXml = '<activities><activity at="2008-01-01T12:00:00+00:00"' +\
            ' type="test" uid="me" guid="1234"/></activities>'
        self.gnip.publish_xml(TEST_PUBLISHER, publishXml)

        resultXml = self.gnip.get_publisher_xml(TEST_PUBLISHER)
        self.assert_(0 != count(resultXml, "2008-01-01T12:00:00"))

    def testGetCollectionActivities(self):
        collection = Collection(self.collectionName, self.user_ids)
        self.gnip.create_collection(collection)
        publishXml = '<activities><activity at="2008-01-01T12:00:00+00:00"' +\
            ' type="test" uid="me" guid="1234"/></activities>'
        self.gnip.publish_xml(TEST_PUBLISHER, publishXml)

        resultActivities = self.gnip.get_collection_activities(
            self.collectionName)
        numMatches = 0
        for activity in resultActivities:
            timeString = activity.get_at_as_string()
            numMatches += count(timeString, "2008-01-01T12:00:00")
        self.assert_(0 != numMatches)

    def testGetCollectionXml(self):
        collection = Collection(self.collectionName, self.user_ids)
        self.gnip.create_collection(collection)
        publishXml = '<activities><activity at="2008-01-01T12:00:00+00:00"' +\
            ' type="test" uid="me" guid="1234"/></activities>'
        self.gnip.publish_xml(TEST_PUBLISHER, publishXml)

        resultXml = self.gnip.get_collection_xml(self.collectionName)
        self.assert_(0 != count(resultXml, "2008-01-01T12:00:00"))

    def testUpdateCollection(self):
        collection = Collection(self.collectionName, self.user_ids)
        self.gnip.create_collection(collection)
        collection.user_ids.append([TEST_PUBLISHER, "joe"])
        result = self.gnip.update_collection(collection)
        self.assertEqual(result, self.success)

    def testUpdateCollectionFromXml(self):
        collection = Collection(self.collectionName, self.user_ids)
        self.gnip.create_collection(collection)
        updatedXml = '<?xml version="1.0" encoding="UTF-8"' +\
            ' standalone="yes"?>' +\
            '<collection name="test">' + \
            '<uid publisher.name="' + TEST_PUBLISHER + '" name="joe"/>' + \
            '<uid publisher.name="' + TEST_PUBLISHER + '" name="me"/>' + \
            '<uid publisher.name="' + TEST_PUBLISHER + '" name="you"/>' + \
            '<uid publisher.name="' + TEST_PUBLISHER + '" name="bob"/>' +\
            '</collection>'
        result = self.gnip.update_collection_from_xml(
            collection.name, updatedXml)
        self.assertEqual(result, self.success)

if __name__ == '__main__':
    unittest.main()

