import sys
sys.path.append("../")
from gnip import payload
import unittest
import logging

class PayloadTestCase(unittest.TestCase):

    def testSimpleEncodeAndDecode(self):
        p = payload.Payload()
        self.assertEquals(None, p.read_raw())
        
        raw = "this is raw payload data"
        p = payload.Payload(raw=raw)
        self.assertEqual(raw, p.read_raw())

        newraw = "this is another raw payload"
        p.write_raw(newraw)
        self.assertEqual(newraw, p.read_raw())

        p.write_raw(None)
        self.assertEqual(None, p.read_raw())
                
if __name__ == '__main__':
    unittest.main()
        