from elementtree.ElementTree import *
import xml_objects
import payload
import place
import iso8601

class Activity(object):
    """Gnip activity container class

    This class provides an abstraction from the Gnip activities XML.

    """

    def __init__(self, at=None, action=None, activity_id=None, url=None, sources=None, places=None, actors=None,
                 destination_urls=None, tags=None, tos=None, regarding_urls=None, payload=None):
        """Initialize the class.

        @type at datetime
        @param at The time of the activity
        @type action string
        @param action The type of activity
        @type activity_id string
        @param activity_id The activity ID
        @type url string
        @param url URL of activity
        @type sources List of strings
        @param sources Sources of the activity
        @type places List of Places
        @param places Place of the activity
        @type actors List of Actors
        @param actors The actors of the activity
        @type destination_urls List of URLs
        @param The destination URLs
        @type tags List of Tags
        @param tags The activity tags
        @type tos List of Tos
        @param tos List of actors this activity is directed to
        @type regarding_urls List of URLS
        @param regarding_urls URLs that this activity is regarding
        @type payload Payload
        @param payload The payload and raw data for the activity
        
        Initializes the class with the proper variables.

        """

        self.at = at
        self.action = action
        self.activity_id = activity_id
        self.url = url
        self.sources = sources
        self.places = places
        self.actors = actors
        self.destination_urls = destination_urls
        self.tags = tags
        self.tos = tos
        self.regarding_urls = regarding_urls
        self.payload = payload

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

        root_node = fromstring(xml)
        self.from_xml_node(root_node)


    def to_xml(self):
        """ Return a XML representation of this object

        @return string containing XML representation of the object

        Returns a XML representation of this object.

        """

        activity_node = Element("activity")

        if self.at is not None:
            at_node = Element("at")
            at_node.text = self.get_at_as_string()
            activity_node.append(at_node)

        if self.action is not None:
            action_node = Element("action")
            action_node.text = self.action
            activity_node.append(action_node)

        if self.activity_id is not None:
            activity_id_node = Element("activityID")
            activity_id_node.text = self.activity_id
            activity_node.append(activity_id_node)

        if self.url is not None:
            url_node = Element("URL")
            url_node.text = self.url
            activity_node.append(url_node)

        if self.sources is not None and len(self.sources) > 0:
            for source in self.sources:
                source_node = Element("source")
                source_node.text = source
                activity_node.append(source_node)
            
        if self.places is not None and len(self.places) > 0:
            for a_place in self.places:
                place_node = a_place.to_xml_node()
                activity_node.append(place_node)

        if self.actors is not None and len(self.actors) > 0:
            for actor in self.actors:
                actor_node = Element("actor")
                actor_node.text = actor.value
                if actor.meta_url is not None:
                    actor_node.set("metaURL", actor.meta_url)
                if actor.uid is not None:
                    actor_node.set("uid", actor.uid)
                activity_node.append(actor_node)

        if self.destination_urls is not None and len(self.destination_urls) > 0:
            for destination_url in self.destination_urls:
                destination_url_node = Element("destinationURL")
                destination_url_node.text = destination_url.value
                if destination_url.meta_url is not None:
                    destination_url_node.set("metaURL", destination_url.meta_url)
                activity_node.append(destination_url_node)

        if self.tags is not None and len(self.tags) > 0:
            for tag in self.tags:
                tag_node = Element("tag")
                tag_node.text = tag.value
                if tag.meta_url is not None:
                    tag_node.set("metaURL", tag.meta_url)
                activity_node.append(tag_node)

        if self.tos is not None and len(self.tos) > 0:
            for to in self.tos:
                to_node = Element("to")
                to_node.text = to.value
                if to.meta_url is not None:
                    to_node.set("metaURL", to.meta_url)
                activity_node.append(to_node)

        if self.regarding_urls is not None and len(self.regarding_urls) > 0:
            for regarding_url in self.regarding_urls:
                regarding_url_node = Element("regardingURL")
                regarding_url_node.text = regarding_url.value
                if regarding_url.meta_url is not None:
                    regarding_url_node.set("metaURL", regarding_url.meta_url)
                activity_node.append(regarding_url_node)

        if self.payload is not None:
            payload_node = self.payload.to_xml_node()
            activity_node.append(payload_node)

        return tostring(activity_node)                                                          


    def from_xml_node(self, xml_node):
        at_node = xml_node.find("at")
        self.set_at_from_string(at_node.text)

        action_node = xml_node.find("action")
        self.action = action_node.text

        activity_id_node = xml_node.find("activityID")
        if activity_id_node is not None:
            self.activity_id = activity_id_node.text
        else:
            self.activity_id = None

        url_node = xml_node.find("URL")
        if url_node is not None:
            self.url = url_node.text
        else:
            self.url = None

        source_nodes = xml_node.findall("source")
        if source_nodes is not None:
            self.sources = []
            for source_node in source_nodes:
                source = source_node.text
                self.sources.append(source)
        else:
            self.sources = None

        place_nodes = xml_node.findall("place")
        if place_nodes is not None:
            self.places = []
            for place_node in place_nodes:
                a_place = place.Place()
                a_place.from_xml_node(place_node)
                self.places.append(a_place)
        else:
            self.places = None

        actor_nodes = xml_node.findall("actor")
        if actor_nodes is not None:
            self.actors = []
            for actor_node in actor_nodes:
                actor = xml_objects.Actor(value=actor_node.text, meta_url=actor_node.get("metaURL"), uid=actor_node.get("uid"))
                self.actors.append(actor)
        else:
            self.actors = None

        destination_url_nodes = xml_node.findall("destinationURL")
        if destination_url_nodes is not None:
            self.destination_urls = []
            for destination_url_node in destination_url_nodes:
                destination_url = xml_objects.URL(value=destination_url_node.text, meta_url=destination_url_node.get("metaURL"))
                self.destination_urls.append(destination_url)
        else:
            self.destination_urls = None

        tag_nodes = xml_node.findall("tag")
        if tag_nodes is not None:
            self.tags = []
            for tag_node in tag_nodes:
                tag = xml_objects.Tag(value=tag_node.text, meta_url=tag_node.get("metaURL"))
                self.tags.append(tag)
        else:
            self.tags = None

        to_nodes = xml_node.findall("to")
        if to_nodes is not None:
            self.tos = []
            for to_node in to_nodes:
                to = xml_objects.To(value=to_node.text, meta_url=to_node.get("metaURL"))
                self.tos.append(to)
        else:
            self.tos = None

        regarding_url_nodes = xml_node.findall("regardingURL")
        if regarding_url_nodes is not None:
            self.regarding_urls = []
            for regarding_url_node in regarding_url_nodes:
                regarding_url = xml_objects.URL(value=regarding_url_node.text, meta_url=regarding_url_node.get("metaURL"))
                self.regarding_urls.append(regarding_url)
        else:
            self.regarding_urls = None

        payload_node = xml_node.find("payload")
        if payload_node is not None:
            self.payload = payload.Payload()
            self.payload.from_xml_node(payload_node)

    def __str__(self):
        return "[" + self.get_at_as_string() + \
            ", " + str(self.action) + \
            ", " + str(self.activity_id) + \
            ", " + str(self.url) + \
            ", " + str(self.sources) + \
            ", " + str(self.places) + \
            ", " + str(self.actors) + \
            ", " + str(self.destination_urls) + \
            ", " + str(self.tags) + \
            ", " + str(self.tos) + \
            ", " + str(self.regarding_urls) + \
            ", " + str(self.payload) + \
            "]"
