import sys
import urllib
sys.path.append("../")
from gnip.xml_objects import *
import unittest

class XmlObjectsTest(unittest.TestCase):

    def testPointsAreEqual(self):
        point1 = Point(12.1243,-13.432)
        point2 = Point(12.1243,-13.432)
        
        self.assertEqual(0, cmp(point1, point2))
        self.assertEquals(point1,point2)

    def testPointsAreNotEqual(self):
        point1 = Point(-12.34212, 13.324)
        point2 = Point(13.324, -12.34212)
        point3 = Point(-12.34212, 12.324)

        self.assertEqual(-1, cmp(point1, point2))
        self.assertEqual(1, cmp(point1, point3))
        self.assertEqual(1, cmp(point2, point1))
        self.assertEqual(-1, cmp(point3, point1))

        self.assertNotEquals(point1,point2)
        self.assertNotEquals(point2,point3)
        self.assertNotEquals(point3,point1)

    def testRulesAreEqual(self):
        rule1 = Rule(type='actor',value='joe')
        rule2 = Rule(type='actor',value='joe')
        self.assertEquals(rule1,rule2)

    def testRulesArentEqual(self):
        rule1 = Rule(type='actor',value='joe')
        rule2 = Rule(type='actor',value='bob')
        rule3 = Rule(type='to',value='joe')
        self.assertNotEquals(rule1,rule2)
        self.assertNotEquals(rule1,rule3)
        self.assertNotEquals(rule2,rule3)

    def testRuleToDeleteQueryString(self):
        rule = Rule('actor','joe@example.com')
        self.assertEquals(urllib.urlencode([("type",rule.type),("value",rule.value)]),rule.to_delete_query_string())

    def testTagsAreEqual(self):
        tag1 = Tag(value='nyc', meta_url='http://www.example.com/api/tags/nyc')
        tag2 = Tag(value='nyc', meta_url='http://www.example.com/api/tags/nyc')
        self.assertEquals(tag1, tag2)

        tag1 = Tag(value='red')
        tag2 = Tag(value='red')

        self.assertEquals(tag1,tag2)

    def testTagsArentEqual(self):
        tag1 = Tag(value='nyc', meta_url='http://www.example.com/api/tags/nyc')
        tag2 = Tag(value='seattle', meta_url='http://www.example.com/api/tags/seattle')
        tag3 = Tag(value='sf', meta_url='http://www.example.com/api/tags/sf')
        self.assertNotEquals(tag1, tag2)
        self.assertNotEquals(tag1, tag3)
        self.assertNotEquals(tag2, tag3)

        tag1 = Tag(value='red')
        tag2 = Tag(value='blue')

        self.assertNotEquals(tag1,tag2)

    def testResultObjectParses(self):
        result1 = Result()
        result1.from_xml("<result>Hello World!</result>")
        self.assertEquals("Hello World!", result1.message)

        result2 = Result("Hello World!")
        self.assertEquals("Hello World!", result2.message)                

    def testErrorObjectParses(self):
        error1 = Error()
        error1.from_xml("<error>Hello Cruel World!</error>")
        self.assertEquals("Hello Cruel World!", error1.message)

        error2 = Error("Hello Cruel World!")
        self.assertEquals("Hello Cruel World!", error2.message)

if __name__ == '__main__':
    unittest.main()
