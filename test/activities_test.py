import sys
import re
sys.path.append("../")
from gnip.activities import *
from gnip import *
from gnip.xml_objects import *
import unittest
import datetime
from xml.dom.minidom import parseString
import logging
import random

class ActivityTestCase(unittest.TestCase):
    def setUp(self):
        logging.getLogger('').setLevel(logging.INFO)
        
    def testActivitiesXmlParses(self):
        randVal1 = str(random.randint(1, 99999999))        
        randVal2 = str(random.randint(1, 99999999))
        xml = '<?xml version="1.0" encoding="utf-8"?><activities>' + \
              '<activity>' + \
              '<at>2008-07-02T11:16:16.000Z</at><action>update</action><activityID>' + randVal1 + '</activityID>' + \
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
              '<mediaURL>http://media2.com</mediaURL><raw>raw</raw></payload></activity>' + \
              '<activity>' + \
              '<at>2008-07-02T11:16:16.000Z</at><action>update</action><activityID>' + randVal2 + '</activityID>' + \
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
              '<mediaURL>http://media2.com</mediaURL><raw>raw</raw></payload></activity>' + \
              '</activities>'
        a = Activities()
        a.from_xml(xml)
        self.assertEquals(2, len(a.items))
        self.assertEquals("update", a.items[0].action)
        self.assertEquals(randVal1, a.items[0].activity_id)
        self.assertEquals("update", a.items[1].action)
        self.assertEquals(randVal2, a.items[1].activity_id)

        actual_xml = a.to_xml()
        self.assertEquals(self.drop_whitespace(xml), self.drop_whitespace(actual_xml))

    def drop_whitespace(self, xml):
        pattern = re.compile("\w")
        pattern.sub(xml,"")

if __name__ == '__main__':
    unittest.main()                          