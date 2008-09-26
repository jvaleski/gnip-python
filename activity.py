import iso8601
from xml.dom.minidom import parseString

class Activity:
    """Gnip activity container class

    This class provides an abstraction from the Gnip activities XML.

    """

    def __init__(self, at=None, action=None, actor=None, regarding=None,
                 source=None, tags=None, to=None, url=None):
        """Initialize the class.

        @type at datetime
        @param at The time of the activity
        @type action string
        @param action The type of activity
        @type actor string
        @param actor The user ID related to the activity
        @type regarding string
        @param regarding what this activitiy is regarding
        @type source string
        @param source The source of the activity
        @type tags string
        @param tags Tags associated with the activity
        @type to string
        @param to Who the activity is directed toward
        @type url string
        @param url Reference to the original activity
        
        Initializes the class with the proper variables.

        """

        self.at = at
        self.action = action
        self.actor = actor
        self.regarding = regarding
        self.source = source
        self.tags = tags
        self.to = to
        self.url = url

    def get_at_as_string(self):
        """ Return 'at' member variable as a formatted string

        @return string representing 'at' in ISO8601 format

        Returns 'at' member variable as a formatted string of the form
        '2008-07-01T05:02:03+00:00'.

        """

        return self.at.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    def set_at_from_string(self, string):
        """ Set 'at' attribute from a formatted string

        @type string string
        @param string ISO8601 formatted string

        Sets 'at' attribute from an ISO8601 formatted string.

        """

        self.at = iso8601.parse_date(string)

    def from_xml(self, xml):
        """ Populate object from XML

        @type xml string
        @param xml A single XML activity fragment

        Sets all of the member variables to new values, based on the
        passed in XML. XML should be of the form:
        <activity at="2008-07-02T11:16:16-07:00" action="upload" actor="sally"
             regarding="blog_post" source="web" tags="trains, planes, automobiles"
             to="bob" url="http://example.com"/>

        """

        node = parseString(xml).documentElement
        self.from_node(node)

    def from_node(self, node):
        """ Populate object from DOM node

        @type node DOM node
        @param node A pre-parsed DOM node

        Sets all of the member variables to new values, based on the
        passed in DOM node.

        """
                   
        self.set_at_from_string(node.getAttribute("at"))
        self.action = node.getAttribute("action")
        self.actor = node.getAttribute("actor")
        self.regarding = node.getAttribute("regarding")
        self.source = node.getAttribute("source")
        self.tags = node.getAttribute("tags").split(",")
        self.to = node.getAttribute("to")
        self.url = node.getAttribute("url")
        

    def to_xml(self):
        """ Return a XML representation of this object

        @return string containing XML representation of the object

        Returns a XML representation of this object.

        """

        xml = '<activity at="' + self.get_at_as_string() + '" '
        xml += 'action="' + self.action + '" '
        xml += 'actor="' + self.actor + '" '
        xml += 'regarding="' + self.regarding + '" '
        xml += 'source="' + self.source + '" '            
        xml += 'tags="' + ",".join(self.tags) + '" '
        xml += 'to="' + self.to + '" '
        xml += 'url="' + self.url + '"'
        xml += '/>'
        return xml

    def __str__(self):
        return "[" + self.get_at_as_string() + \
            ", " + str(self.action) + \
            ", " + str(self.actor) + \
            ", " + str(self.regarding) + \
            ", " + str(self.source) + \
            ", " + str(self.tags) + \
            ", " + str(self.to) + \
            ", " + str(self.url) + \
            "]"
