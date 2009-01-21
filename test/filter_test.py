import sys
sys.path.append("../")
from gnip import filter
from gnip.xml_objects import *
import unittest

class FilterTestCase(unittest.TestCase):

    def setUp(self):
        self.rules = [Rule(type="actor", value="me"), Rule(type="actor", value="you"), Rule(type="actor", value="bob")]
        self.filterName = "test"
        self.filterFullData = True

    def tearDown(self):
        pass

    def testFromXmlWithoutPostUrl(self):
        xml = '<filter fullData="true" name="test">' + \
            '<rule type="actor">me</rule>' + \
            '<rule type="actor">you</rule>' + \
            '<rule type="actor">bob</rule>' + \
            '</filter>'
        
        a_filter = filter.Filter()
        a_filter.from_xml(xml)

        self.assertEqual(a_filter.name, self.filterName)
        self.assertEqual(a_filter.rules, self.rules)
        self.assertEqual(a_filter.full_data, self.filterFullData)
        self.assertTrue(a_filter.post_url is None)
        
    def testFromXmlWithPostUrl(self):
        xml = '<filter fullData="true" name="test">' + \
            '<postURL>http://example.com</postURL>' + \
            '<rule type="actor">me</rule>' + \
            '<rule type="actor">you</rule>' + \
            '<rule type="actor">bob</rule>' + \
            '</filter>'
        
        a_filter = filter.Filter()
        a_filter.from_xml(xml)

        self.assertEquals(a_filter.name, self.filterName)
        self.assertEquals(a_filter.rules, self.rules)
        self.assertEquals(a_filter.full_data, self.filterFullData)
        self.assertEquals(a_filter.post_url, "http://example.com")

    def testFilterWithFullDataSetToFalse(self):
        xml = '<filter fullData="false" name="test">' + \
            '<postURL>http://example.com</postURL>' + \
            '<rule type="actor">me</rule>' + \
            '<rule type="actor">you</rule>' + \
            '<rule type="actor">bob</rule>' + \
            '</filter>'

        a_filter = filter.Filter()
        a_filter.from_xml(xml)

        self.assertEquals(a_filter.name, self.filterName)
        self.assertEquals(a_filter.rules, self.rules)
        self.assertEquals(a_filter.post_url, "http://example.com")
        self.assertFalse(a_filter.full_data)

    def testToXmlWithoutPostUrl(self):
        expected_xml = '<filter fullData="true" name="test">' + \
            '<rule type="actor">me</rule>' + \
            '<rule type="actor">you</rule>' + \
            '<rule type="actor">bob</rule>' + \
            '</filter>'
            
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.assertEqual(a_filter.to_xml(), expected_xml)
        
    def testToXmlWithPostUrl(self):
        expected_xml = '<filter fullData="true" name="test">' + \
            '<postURL>http://example.com</postURL>' + \
            '<rule type="actor">me</rule>' + \
            '<rule type="actor">you</rule>' + \
            '<rule type="actor">bob</rule>' + \
            '</filter>'
            
        a_filter = filter.Filter(name=self.filterName, post_url="http://example.com", rules=self.rules, full_data=self.filterFullData)
        self.assertEqual(a_filter.to_xml(), expected_xml)

    def testFilterEquals(self):
        filter1 = filter.Filter("jojo-filter", True, "http://www.example.com/posttome", [Rule("actor", "jojo")])
        filter2 = filter.Filter("jojo-filter", True, "http://www.example.com/posttome", [Rule("actor", "jojo")])
        self.assertEquals(filter1, filter2)

        filter2 = filter.Filter(name="jojo-filter", post_url="http://www.example.com/posttome", rules=[Rule("actor", "jojo")])
        self.assertEquals(filter1, filter2)

        filter1 = filter.Filter(name="jojo-filter", rules=[Rule("actor", "jojo")])
        filter2 = filter.Filter(name="jojo-filter", rules=[Rule("actor", "jojo")])
        self.assertEquals(filter1, filter2)

        filter1 = filter.Filter(name="jojo-filter", rules=[Rule("actor", "jojo"), Rule("actor", "bob")])
        filter2 = filter.Filter(name="jojo-filter", rules=[Rule("actor", "bob"), Rule("actor", "jojo")])
        self.assertEquals(filter1, filter2)

        filter1 = filter.Filter(name="jojo-filter")
        filter2 = filter.Filter(name="jojo-filter")
        self.assertEquals(filter1, filter2)

        filter1 = filter.Filter(name="jojo-filter", rules=[Rule("actor", "me"), Rule("actor", "you"), Rule("actor", "bob")])
        filter2 = filter.Filter(name="jojo-filter", rules=[Rule("actor", "bob"), Rule("actor", "you"), Rule("actor", "me")])
        self.assertEquals(filter1, filter2)
        
    def testFilterNotEquals(self):
        filter1 = filter.Filter("jojo-filter", True, "http://www.example.com/posttome", [Rule("actor", "jojo")])
        filter2 = filter.Filter("jojo-other-filter", True, "http://www.example.com/posttome", [Rule("actor", "jojo")])
        self.assertNotEquals(filter1, filter2)

        filter1 = filter.Filter("jojo-filter", True, "http://www.example.com/posttome", [Rule("actor", "jojo")])
        filter2 = filter.Filter("jojo-filter", False, "http://www.example.com/posttome", [Rule("actor", "jojo")])
        self.assertNotEquals(filter1, filter2)

        filter1 = filter.Filter("jojo-filter", True, "http://www.example.com/posttome", [Rule("actor", "jojo")])
        filter2 = filter.Filter("jojo-filter", True, "http://www.example.com/posttomehere", [Rule("actor", "jojo")])
        self.assertNotEquals(filter1, filter2)

        filter1 = filter.Filter("jojo-filter", True, "http://www.example.com/posttome", [Rule("actor", "jojo")])
        filter2 = filter.Filter("jojo-filter", True, "http://www.example.com/posttome", [Rule("actor", "bob")])
        self.assertNotEquals(filter1, filter2)

        filter1 = filter.Filter("jojo-filter", True, "http://www.example.com/posttome", [Rule("actor", "jojo")])
        filter2 = filter.Filter("jojo-filter", True, "http://www.example.com/posttome", [Rule("actor", "jojo"), Rule("to", "frank")])
        self.assertNotEquals(filter1, filter2)
        
if __name__ == '__main__':
    unittest.main()
