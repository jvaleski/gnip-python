from elementtree.ElementTree import *
import xml_objects

class Payload(object):
    """Gnip Payload container class"""

    def __init__(self, title=None, body=None, media_urls=None, raw=None):
        """Initialize the class.

        @type title string
        @param title Activity title
        @type body string
        @param body Activity body
        @type media_urls List of URLs
        @param media_urls MediaURLs associated with the activity
        @type raw base64 & gzipped string
        @param raw Raw text of activity

        Initializes the class with the proper variables.

        """

        self.title = title
        self.body = body
        self.media_urls = media_urls
        self.raw = raw

    def from_xml_node(self, payload_xml_node):
        """ Populates payload from a payload xml node """

        if payload_xml_node is not None:

            title_node = payload_xml_node.find("title")

            if title_node is not None:
                self.title = title_node.text
            else:
                self.title = None

            body_node = payload_xml_node.find("body")

            if body_node is not None:
                self.body = body_node.text
            else:
                self.body = None

            media_url_nodes = payload_xml_node.findall("mediaURL")

            if media_url_nodes is not None:
                self.media_urls = []
                for media_url_node in media_url_nodes:
                    media_url = xml_objects.URL(value=media_url_node.text, meta_url=media_url_node.get("metaURL"))
                    self.media_urls.append(media_url)
            else:
                self.media_urls = None

            raw_node = payload_xml_node.find("raw")

            self.raw = raw_node.text

    def to_xml_node(self):
        """ Return a XML representation of this object

        @return string containing XML representation of the object

        Returns a XML representation of this object.

        """

        payload_node = Element("payload")

        if self.title is not None:
            title_node = Element("title")
            title_node.text = self.title
            payload_node.append(title_node)

        if self.body is not None:
            body_node = Element("body")
            body_node.text = self.body
            payload_node.append(body_node)

        if self.media_urls is not None and len(self.media_urls) > 0:
            for media_url in self.media_urls:
                media_url_node = Element("mediaURL")
                media_url_node.text = media_url.value
                if media_url.meta_url is not None:
                    media_url_node.set("metaURL", media_url.meta_url)
                payload_node.append(media_url_node)

        if self.raw is not None:
            raw_node = Element("raw")
            raw_node.text = self.raw
            payload_node.append(raw_node)

        return payload_node

    def __str__(self):
        return "[" + str(self.title) + \
            ", " + str(self.body) + \
            ", " + str(self.media_urls) + \
            ", " + str(self.raw) + \
            "]"
