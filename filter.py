import iso8601
from xml.dom.minidom import parseString

class Filter:
    """Gnip filter container class

    This class provides an abstraction from the Gnip filter XML.

    """
    
    def __init__(self, name=None, post_url=None, jid=None, rules=None, full_data=None):
        """Initialize the class.

        @type name string
        @param name The name of the filter
        @type post_url string
        @param post_url The URL to post filter activities to
        @type jid string
        @param jid The JabberID to post filter activities to
        @type rules list of strings of form (Type, Value)
        @param rules The rules for the collection
        @type full_data string
        @type full_data Whether or not this filter is for full data

        Initializes the class with the proper variables. Note that only
        one of post_url and jid will be used, with post_url taking
        priority.

        """
        
        self.name = name
        self.rules = rules
        self.post_url = post_url
        self.jid = jid
        self.full_data = full_data

    def to_xml(self):
        """ Return a XML representation of this object

        @return string containing XML representation of the object

        Returns a XML representation of this object.

        """

        xml = '<filter name="' + self.name + '" fullData="' + self.full_data + '">'
        if self.post_url is not None:
            xml += '<postUrl>' + self.post_url + '</postUrl>'
        elif self.jid is not None:
            xml += '<jid>' + self.jid + '</jid>'
            
        for rule in self.rules:
            xml += '<rule type="' + rule[0] + '" value="' + rule[1] + '"/>' 
        xml += '</filter>'

        return xml
    
    def from_xml(self, xml):     
        """ Populate object from XML

        @type xml string
        @param xml The xml representation of a filter

        Sets all of the member variables to new values, based on the
        passed in XML. XML should be of the form:
        <filter name="test">
            <rule type="actor" value="me"/>
            <rule type="actor" value="you"/>
            <rule type="actor" value="bob"/>
        </filter>

        """   

        root = parseString(xml).documentElement
        self.name = root.getAttribute("name")
        self.full_data = root.getAttribute("fullData")
        
        self.rules = []
        for node in root.childNodes:
            if node.tagName == 'postUrl':
                self.post_url = node.childNodes[0].nodeValue
            elif node.tagName == 'jid':
                self.jid = node.childNodes[0].nodeValue
            elif node.tagName == 'rule':
                self.rules.append([node.getAttribute('type'), node.getAttribute('value')])

    def __str__(self):
        return "[" + self.name + ", " + self.post_url + ", " + self.jid + ", " + str(self.rules) + "]"