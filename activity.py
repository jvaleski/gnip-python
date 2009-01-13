import iso8601
from ElementTree import *

class Activity:
    """Gnip activity container class

    This class provides an abstraction from the Gnip activities XML.

    """

    def __init__(self, at=None, action=None, rule=None, actor=None,
                 title=None, body=None, dest_url=None, source=None, 
                 to=None, geo=None, regarding_url=None, media_urls=None,
                 tags=None, raw=None):
        """Initialize the class.

        @type at datetime
        @param at The time of the activity
        @type action dict(value)
        @param action The type of activity
        @type rule dict(type, value)
        @param rule The primary key
        @type actor dict(value, meta_url)
        @param actor Who performed the action
        @type title dict(value)
        @param title The source of the activity
        @type body dict(value)
        @param body Activity body
        @type dest_url dict(value, meta_url)
        @param dest_url Destination _url
        @type source dict(value)
        @param souce Source of the activity
        @type to dict(value)
        @param to Who activity is directed towards
        @type geo dict(value)
        @param geo Geography info
        @type regarding_url dict(value, meta_url)
        @param regarding_url Regarding _url
        @type media_urls list(dict(value, meta_url))
        @param media_urls List of media _urls
        @type tags list(dict(value, meta_url))
        @param tags List of tags
        @type raw dict(value)
        @param raw Raw text of activity
        
        Initializes the class with the proper variables.

        """

        self.at = at
        self.action = action
        self.rule = rule
        self.actor = actor
        self.title = title
        self.body = body
        self.dest_url = dest_url
        self.source = source
        self.to = to
        self.geo = geo
        self.regarding_url = regarding_url
        self.media_urls = media_urls
        self.tags = tags
        self.raw = raw

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
        passed in XML. 
        """

        # Pull out all of the data from the xml
        root_node = fromstring(xml)
        at_node = root_node.find("at")
        action_node = root_node.find("action")
        rule_node = root_node.find("rule")
        payload_node = root_node.find("payload")
        if payload_node is not None:
            actor_node = payload_node.find("actor")
            title_node = payload_node.find("title")
            body_node = payload_node.find("body")
            dest_url_node = payload_node.find("destURL")
            source_node = payload_node.find("source")
            to_node = payload_node.find("to")
            geo_node = payload_node.find("geo")
            regarding_url_node = payload_node.find("regardingURL")
            media_url_nodes = payload_node.findall("mediaURL")
            tag_nodes = payload_node.findall("tag")
            raw_node = payload_node.find("raw")

        # Set local variables from xml data
        self.set_at_from_string(at_node.text)
        self.action = dict(value=action_node.text)
        self.rule = dict(value=rule_node.text, type=rule_node.get("type"))
        if payload_node is not None:
            if actor_node is not None:
                self.actor = dict(value=actor_node.text, meta_url=actor_node.get("metaURL"))
            else:
                self.actor = dict()
                
            if title_node is not None:
                self.title = dict(value=title_node.text)
            else:
                self.title = dict() 
                
            if body_node is not None:
                self.body = dict(value=body_node.text)
            else:
                self.body = dict() 
                        
            if dest_url_node is not None:
                self.dest_url = dict(value=dest_url_node.text, meta_url=dest_url_node.get("metaURL"))
            else:
                self.dest_url = dict() 
                        
            if source_node is not None:
                self.source = dict(value=source_node.text)
            else:
                self.source = dict() 
                        
            if to_node is not None:
                self.to = dict(value=to_node.text, meta_url=to_node.get("metaURL"))
            else:
                self.to = dict() 
                        
            if geo_node is not None:
                self.geo = dict(value=geo_node.text)
            else:
                self.geo = dict() 
                        
            if regarding_url_node is not None:
                self.regarding_url = dict(value=regarding_url_node.text, meta_url=regarding_url_node.get("metaURL"))
            else:
                self.regarding_url = dict()     
            
            self.media_urls = []
            for media_url_node in media_url_nodes:
                media_url = dict(value=media_url_node.text, meta_url=media_url_node.get("metaURL"))
                self.media_urls.append(media_url)
            
            self.tags = []
            for tag_node in tag_nodes:
                tag = dict(value=tag_node.text, meta_url=tag_node.get("metaURL"))
                self.tags.append(tag)
                
            self.raw = dict(value=raw_node.text)    

    def to_xml(self):
        """ Return a XML representation of this object

        @return string containing XML representation of the object

        Returns a XML representation of this object.

        """
        
        # Create all the nodes
        at_node = Element("at")
        at_node.text = self.get_at_as_string()
        
        action_node = Element("action")
        action_node.text = self.action["value"]
        
        rule_node = Element("rule")
        rule_node.set("type", self.rule["type"])
        rule_node.text = self.rule["value"]

        actor_node = None
        if self.actor is not None and len(self.actor) > 0:
            actor_node = Element("actor")
            actor_node.text = self.actor["value"]
            actor_node.set("metaURL", self.actor["meta_url"])
            
        title_node = None
        if self.title is not None and len(self.title) > 0:
            title_node = Element("title")
            title_node.text = self.title["value"]
        
        body_node = None
        if self.body is not None and len(self.body) > 0:
            body_node = Element("body")
            body_node.text = self.body["value"]
            
        dest_url_node = None
        if self.dest_url is not None and len(self.dest_url) > 0:
            dest_url_node = Element("destURL")
            dest_url_node.text = self.dest_url["value"]
            dest_url_node.set("metaURL", self.dest_url["meta_url"])    
            
        source_node = None
        if self.source is not None and len(self.source) > 0:
            source_node = Element("source")
            source_node.text = self.source["value"] 
            
        to_node = None
        if self.to is not None and len(self.to) > 0:
            to_node = Element("to")
            to_node.text = self.to["value"]
            to_node.set("metaURL", self.to["meta_url"])     
            
        geo_node = None
        if self.geo is not None and len(self.geo) > 0:
            geo_node = Element("geo")
            geo_node.text = self.geo["value"]        
        
        regarding_url_node = None
        if self.regarding_url is not None and len(self.regarding_url) > 0:
            regarding_url_node = Element("regardingURL")
            regarding_url_node.text = self.regarding_url["value"]
            regarding_url_node.set("metaURL", self.regarding_url["meta_url"])      
                
        media_url_nodes = None
        if self.media_urls is not None and len(self.media_urls) > 0:
            media_url_nodes = []
            for media_url in self.media_urls:
                media_url_node = Element("mediaURL")
                media_url_node.text = media_url["value"]
                media_url_node.set("metaURL", media_url["meta_url"]) 
                media_url_nodes.append(media_url_node)
                
        tag_nodes = None
        if self.tags is not None and len(self.tags) > 0:
            tag_nodes = []
            for tag in self.tags:
                tag_node = Element("tag")
                tag_node.text = tag["value"]
                tag_node.set("metaURL", tag["meta_url"]) 
                tag_nodes.append(tag_node)
            
        raw_node = None
        if self.raw is not None and len(self.raw) > 0:
            raw_node = Element("raw")
            raw_node.text = self.raw["value"]
        
        # Build element tree
        activity_node = Element("activity")
        
        activity_node.append(at_node)
        activity_node.append(action_node)
        activity_node.append(rule_node)
        if raw_node is not None:
            payload_node = Element("payload") 
            activity_node.append(payload_node)
            payload_node.append(actor_node)
            payload_node.append(title_node)
            payload_node.append(body_node)
            payload_node.append(dest_url_node)
            payload_node.append(source_node)
            payload_node.append(to_node)
            payload_node.append(geo_node)
            payload_node.append(regarding_url_node)
            for media_url_node in media_url_nodes:
                payload_node.append(media_url_node)
            for tag_node in tag_nodes:
                payload_node.append(tag_node)
            payload_node.append(raw_node)
            
        return tostring(activity_node)                                                          

    def __str__(self):
        return "[" + self.get_at_as_string() + \
            ", " + str(self.action) + \
            ", " + str(self.rule) + \
            ", " + str(self.actor) + \
            ", " + str(self.title) + \
            ", " + str(self.body) + \
            ", " + str(self.dest_url) + \
            ", " + str(self.source) + \
            ", " + str(self.geo) + \
            ", " + str(self.regarding_url) + \
            ", " + str(self.media_urls) + \
            ", " + str(self.tags) + \
            ", " + str(self.raw) + \
            "]"
