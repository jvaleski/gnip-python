import sys
sys.path.append("../")
from gnip import filter
import unittest

class FilterTestCase(unittest.TestCase):
    def setUp(self):
        self.rules = [dict(type="actor", value="me"), dict(type="actor", value="you"), dict(type="actor", value="bob")]
        self.filterName = "test"
        self.filterFullData = "true"

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

        self.assertEquals(a_filter.name, self.filterName)
        self.assertEquals(a_filter.rules, self.rules)
        self.assertEquals(a_filter.full_data, self.filterFullData)
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

if __name__ == '__main__':
    unittest.main()
