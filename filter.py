import iso8601
from ElementTree import *

class Filter:
    """Gnip filter container class

    This class provides an abstraction from the Gnip filter XML.

    """
    
    def __init__(self, name="", full_data="true", post_url=None, rules=[]):
        """Initialize the class.

        @type name string
        @param name The name of the filter
        @type post_url string
        @param post_url The URL to post filter activities to
        @type rules List of dict(type, value)
        @param rules The rules for the collection
        @type full_data string
        @type full_data Whether or not this filter is for full data

        Initializes the class with the proper variables. 

        """
        
        self.name = name
        self.rules = rules
        self.post_url = post_url
        self.full_data = full_data

    def to_xml(self):
        """ Return a XML representation of this object

        @return string containing XML representation of the object

        Returns a XML representation of this object.

        """

        filter_node = Element("filter")
        
        post_url_node = None
        if self.post_url is not None:
            post_url_node = Element("postURL")
            post_url_node.text = self.post_url

        rule_nodes = None
        if self.rules is not None and len(self.rules) > 0:
            rule_nodes = []
            for rule in self.rules:
                rule_node = Element("rule")
                rule_node.text = rule["value"]
                rule_node.set("type", rule["type"]) 
                rule_nodes.append(rule_node)
                
        filter_node.set("name", self.name)
        filter_node.set("fullData", self.full_data)
        if post_url_node is not None:
            filter_node.append(post_url_node)
        for rule_node in rule_nodes:
            filter_node.append(rule_node)

        return tostring(filter_node)
    
    def from_xml(self, xml):     
        """ Populate object from XML

        @type xml string
        @param xml The xml representation of a filter

        Sets all of the member variables to new values, based on the
        passed in XML.
        
        """   

        # Pull out all of the data from the xml
        filter_node = fromstring(xml)
        post_url_node = filter_node.find("postURL")
        rule_nodes = filter_node.findall("rule")
        
        # set local variables
        self.name = filter_node.get("name")
        self.full_data = filter_node.get("fullData")
        
        if post_url_node is not None:
            self.post_url = post_url_node.text
        else:
            self.post_url = None

        self.rules = []
        for rule_node in rule_nodes:
            rule = dict(type=rule_node.get("type"), value=rule_node.text)
            self.rules.append(rule)

    def __str__(self):
        return "[" + self.name + ", " + self.postURL + ", " + str(self.rules) + "]"