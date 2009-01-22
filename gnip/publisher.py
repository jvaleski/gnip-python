from xml.dom.minidom import parseString

class Publisher(object):
    """Gnip Publisher container class

    This class provides an abstraction from the Gnip Publisher XML.

    """
    
    def __init__(self, name=None, rule_types=None):
        """Initialize the class.

        @type name string
        @param name the name of the publisher
        @type rule_types list of strings
        @param rule_types The rule types this publisher supports

        Initializes the class with the proper variables. 

        """
        
        self.name = name
        self.rule_types=rule_types
    
    def to_xml(self):
        """ Return a XML representation of the Publisher as a string. """
        xml = '<publisher name="' + self.name + '">'
        xml += '<supportedRuleTypes>'
        
        for rule_type in self.rule_types:
            xml += '<type>' + rule_type + '</type>'
        
        xml += '</supportedRuleTypes></publisher>'
        
        return xml
    
    def from_xml(self, xml):
        """ Populates the Publisher object based on Publsiher XML
        
        @type xml string
        @param xml the Publisher XML
        
        """
        root = parseString(xml).documentElement
        self.name = root.getAttribute("name")
        
        self.rule_types = []
        for node in root.childNodes:
            if node.tagName == 'supportedRuleTypes':
                for subnode in node.childNodes:
                    if subnode.tagName == 'type':
                        self.rule_types.append(subnode.childNodes[0].nodeValue)

    def __cmp__(self, other):
        if isinstance(other, Publisher):
            ret = cmp(self.name, other.name)
            if ret is 0:
                ret = cmp(sorted(self.rule_types), sorted(other.rule_types))                    
        else:
            ret = 1
        return ret