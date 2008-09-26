import unittest
import filter

class FilterTestCase(unittest.TestCase):
    def setUp(self):
        self.rules = [["actor", "me"], ["actor", "you"], ["actor", "bob"]]
        self.filterName = "test"
        self.filterFullData = "true"

    def tearDown(self):
        pass

    def testFromXmlWithoutPostUrlOrJid(self):
        xml = '<filter name="test" fullData="true">' + \
            '<rule type="actor" value="me"/>' + \
            '<rule type="actor" value="you"/>' + \
            '<rule type="actor" value="bob"/>' + \
            '</filter>'
        
        a_filter = filter.Filter()
        a_filter.from_xml(xml)

        self.assertEquals(a_filter.name, self.filterName)
        self.assertEquals(a_filter.rules, self.rules)
        self.assertEquals(a_filter.full_data, self.filterFullData)
        self.assertTrue(a_filter.post_url is None)
        self.assertTrue(a_filter.jid is None)
        
    def testFromXmlWithPostUrl(self):
        xml = '<filter name="test" fullData="true">' + \
            '<postUrl>http://example.com</postUrl>' + \
            '<rule type="actor" value="me"/>' + \
            '<rule type="actor" value="you"/>' + \
            '<rule type="actor" value="bob"/>' + \
            '</filter>'
        
        a_filter = filter.Filter()
        a_filter.from_xml(xml)

        self.assertEquals(a_filter.name, self.filterName)
        self.assertEquals(a_filter.rules, self.rules)
        self.assertEquals(a_filter.full_data, self.filterFullData)
        self.assertEquals(a_filter.post_url, "http://example.com")
        self.assertTrue(a_filter.jid is None)
            
    def testFromXmlWithJid(self):
        xml = '<filter name="test" fullData="true">' + \
            '<jid>joe@jabber.org</jid>' + \
            '<rule type="actor" value="me"/>' + \
            '<rule type="actor" value="you"/>' + \
            '<rule type="actor" value="bob"/>' + \
            '</filter>'
        
        a_filter = filter.Filter()
        a_filter.from_xml(xml)

        self.assertEquals(a_filter.name, self.filterName)
        self.assertEquals(a_filter.rules, self.rules)
        self.assertEquals(a_filter.full_data, self.filterFullData)
        self.assertTrue(a_filter.post_url is None)
        self.assertEquals(a_filter.jid, "joe@jabber.org")

    def testToXmlWithoutPostUrlOrJid(self):
        expected_xml = '<filter name="test" fullData="true">' + \
            '<rule type="actor" value="me"/>' + \
            '<rule type="actor" value="you"/>' + \
            '<rule type="actor" value="bob"/>' + \
            '</filter>'
            
        a_filter = filter.Filter(name=self.filterName, rules=self.rules, full_data=self.filterFullData)
        self.assertEqual(a_filter.to_xml(), expected_xml)
        
    def testToXmlWithPostUrl(self):
        expected_xml = '<filter name="test" fullData="true">' + \
            '<postUrl>http://example.com</postUrl>' + \
            '<rule type="actor" value="me"/>' + \
            '<rule type="actor" value="you"/>' + \
            '<rule type="actor" value="bob"/>' + \
            '</filter>'
            
        a_filter = filter.Filter(name=self.filterName, post_url="http://example.com", rules=self.rules, full_data=self.filterFullData)
        self.assertEqual(a_filter.to_xml(), expected_xml)
        
    def testToXmlWithJid(self):
        expected_xml = '<filter name="test" fullData="true">' + \
            '<jid>joe@jabber.org</jid>' + \
            '<rule type="actor" value="me"/>' + \
            '<rule type="actor" value="you"/>' + \
            '<rule type="actor" value="bob"/>' + \
            '</filter>'
            
        a_filter = filter.Filter(name=self.filterName, jid="joe@jabber.org", rules=self.rules, full_data=self.filterFullData)
        self.assertEqual(a_filter.to_xml(), expected_xml)