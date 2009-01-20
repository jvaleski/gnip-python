from elementtree.ElementTree import *
import urllib

class URL(object):
    """Gnip URL container class"""

    def __init__(self, value=None, meta_url=None):
        self.value = value
        self.meta_url = meta_url

    def __str__(self):
        return "[" + str(self.value) + ", " + str(self.meta_url) + "]"

    def __cmp__(self, other):
        if isinstance(other, URL):
            ret = cmp(self.value, other.value)
            if ret == 0:
                ret = cmp(self.meta_url, other.meta_url)
        else:
            ret = 1
        return ret

class Actor(object):
    """Gnip Actor container class"""

    def __init__(self, value=None, uid=None, meta_url=None):
        self.value = value
        self.uid = uid
        self.meta_url = meta_url

    def __str__(self):
        return "[" + str(self.value) + ", " + str(self.uid) + ", " + str(self.meta_url) + "]"

class Tag(object):
    """Gnip Tag container class"""

    def __init__(self, value=None, meta_url=None):
        self.value = value
        self.meta_url = meta_url

    def __str__(self):
        return "[" + str(self.value) + ", " + str(self.meta_url) + "]"

    def __cmp__(self, other):
        if isinstance(other, Tag):
            ret = cmp(self.value, other.value)
            if ret == 0:
                ret = cmp(self.meta_url, other.meta_url)
        else:
            ret = 1
        return ret

class To(object):
    """Gnip To container class"""

    def __init__(self, value=None, meta_url=None):
        self.value = value
        self.meta_url = meta_url

    def __str__(self):
        return "[" + str(self.value) + ", " + str(self.meta_url) + "]"

    def __cmp__(self, other):
        if isinstance(other, To):
            ret = cmp(self.value, other.value)
            if ret == 0:
                ret = cmp(self.meta_url, other.meta_url)
        else:
            ret = 1
        return ret

class Point(object):
    """Gnip Point container class"""

    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

    def __str__(self):
        return "[" + str(self.x) + ", " + str(self.y) + "]"

    def __cmp__(self, other):
        if isinstance(other, Point):
            if self.x < other.x:
                ret = -1
            elif self.x > other.x:
                ret = 1
            elif self.y < other.y:
                ret = -1
            elif self.y > other.y:
                ret = 1
            else:
                ret = 0
        else:
            ret = 1
        return ret

class Rule(object):
    """Gnip Rule container class"""

    def __init__(self, type=None, value=None):
        self.type = type
        self.value = value

    def to_delete_query_string(self):
        return urllib.urlencode([("type",self.type),("value",self.value)])

    def to_xml(self):
        rule_node = Element("rule")
        rule_node.text = self.value
        rule_node.set("type", self.type)
        return tostring(rule_node)

    def __str__(self):
        return "[" + str(self.type) + ", " + str(self.value) + "]"

    def __cmp__(self, other):
        if isinstance(other, Rule):
            ret = cmp(self.type, other.type)
            if(ret == 0):
                ret = cmp(self.value, other.value)
        else:
            ret = 1
        return ret

class Result(object):
    """Gnip result container class"""

    def __init__(self, message=None):
        self.message = message

    def from_xml(self, xml):
        node = fromstring(xml)

        if node is not None:
            self.message = node.text
        else:
            self.message = ""

class Error(object):
    """Gnip error container class"""

    def __init__(self, message=None):
        self.message = message

    def from_xml(self, xml):
        node = fromstring(xml)

        if node is not None:
            self.message = node.text
        else:
            self.message = ""