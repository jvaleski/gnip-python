import unittest
import datetime
import activity
from xml.dom.minidom import parseString

class ActivityTestCase(unittest.TestCase):
    def setUp(self):
        self.timeString = "2008-07-02T11:16:16.000Z"
        self.xml='<activity at="2008-07-02T11:16:16.000Z" action="upload" actor="sally" ' + \
             'regarding="blog_post" source="web" tags="trains,planes,automobiles" ' + \
             'to="bob" url="http://example.com"/>'
        self.testAction = "upload"
        self.testActor = "sally"
        self.testRegarding = "blog_post"
        self.testSource = "web"
        self.testTags = ["trains", "planes", "automobiles"]
        self.testTo = "bob"
        self.testUrl = "http://example.com"

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
        activity1.set_at_from_string(self.timeString)
        activity2 = activity.Activity(at=activity1.at)
        self.assertEqual(activity2.get_at_as_string(), self.timeString)

    def testFromXml(self):  
        an_activity = activity.Activity()
        an_activity.from_xml(self.xml)

        self.assertEqual(an_activity.get_at_as_string(), self.timeString)
        self.assertEqual(an_activity.action, self.testAction)
        self.assertEqual(an_activity.actor, self.testActor)
        self.assertEqual(an_activity.regarding, self.testRegarding)
        self.assertEqual(an_activity.source, self.testSource)
        self.assertEqual(an_activity.tags, self.testTags)
        self.assertEqual(an_activity.to, self.testTo)
        self.assertEqual(an_activity.url, self.testUrl)

    def testFromNode(self):
        node = parseString(self.xml).documentElement
        an_activity = activity.Activity()
        an_activity.from_node(node)

        self.assertEqual(an_activity.get_at_as_string(), self.timeString)
        self.assertEqual(an_activity.action, self.testAction)
        self.assertEqual(an_activity.actor, self.testActor)
        self.assertEqual(an_activity.regarding, self.testRegarding)
        self.assertEqual(an_activity.source, self.testSource)
        self.assertEqual(an_activity.tags, self.testTags)
        self.assertEqual(an_activity.to, self.testTo)
        self.assertEqual(an_activity.url, self.testUrl)

    def testToXml(self):
        an_activity = activity.Activity(action=self.testAction, actor=self.testActor,
                                        regarding=self.testRegarding,
                                        source=self.testSource, tags=self.testTags,
                                        to=self.testTo, url=self.testUrl)
        an_activity.set_at_from_string(self.timeString)

        self.assertEqual(an_activity.to_xml(), self.xml)