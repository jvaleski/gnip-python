import datetime
import iso8601
import time
from davclient import DAVClient
from string import count
from xml.dom.minidom import parseString

class Activity:
    """Gnip activity container class

    This class provides an abstraction from the Gnip activities XML.

    """

    def __init__(self, uid=None, at=None, type=None, guid=None):
        """Initialize the class.

        @type uid string
        @param uid The user ID related to the activity
        @type at datetime
        @param at The time of the activity
        @type type string
        @param type The type of activity
        @type guid string
        @param guid The GUID for the activity (optional)

        Initializes the class with the proper variables.

        """

        self.uid = uid
        self.at = at
        self.type = type
        self.guid = guid

    def get_at_as_string(self):
        """ Return 'at' member variable as a formatted string

        @return string representing 'at' in ISO8601 format

        Returns 'at' member variable as a formatted string of the form
        '2008-07-01T05:02:03+00:00'.

        """

        return self.at.strftime("%Y-%m-%dT%H:%M:%S+00:00")

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
        <activity type="added_friend" uid="sally" 
            at="2008-07-02T11:16:16-07:00" guid="123"/>

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

        self.uid = node.getAttribute("uid")
        self.set_at_from_string(node.getAttribute("at"))
        self.type = node.getAttribute("type")
        if True == node.hasAttribute("guid"):
            self.guid = node.getAttribute("guid")
        else:
            self.guid = None

    def to_xml(self):
        """ Return a XML representation of this object

        @return string containing XML representation of the object

        Returns a XML representation of this object.

        """

        xml = '<activity at="' + self.get_at_as_string() + '" '
        xml += 'type="' + self.type + '" '
        xml += 'uid="' + self.uid + '"'
        if None != self.guid:
            xml += ' guid="' + self.guid + '"'
        xml += '/>'
        return xml

    def __str__(self):
        return "[" + self.uid + ", " + self.get_at_as_string() + ", " + \
            self.type + ", " + str(self.guid) + "]"

class Collection:
    """Gnip collection container class.

    This class provides an abstraction from the Gnip collections XML.

    """

    def __init__(self, name=None, user_ids=None):
        """Initialize the class.
        
        @type name string
        @param name The name of the collection
        @type user_ids list of tuple of strings of form ("publisher", "uid")
        @param user_ids a list of all user ids associated with this collection
        
        Initializes the class with the proper variables.
        
        """

        self.name = name
        self.user_ids = user_ids

    def to_xml(self):
        """ Return a XML representation of this object

        @return string containing XML representation of the object

        Returns a XML representation of this object.

        """

        xml = '<collection name="' + self.name + '">'
        for uid in self.user_ids:
            xml += '<uid publisher.name="' + uid[0] + \
                '" name="' + uid[1] + '"/>'
        xml += '</collection>'

        return xml

    def from_xml(self, xml):        
        """ Populate object from XML

        @type xml string
        @param xml A complete collection in XML form

        Sets all of the member variables to new values, based on the
        passed in XML. XML should be of the form:
        <collection name="test">
            <uid publisher.name="mybloglog" name="me"/>
            <uid publisher.name="mybloglog" name="you"/>
            <uid publisher.name="mybloglog" name="bob"/>
        </collection>

        """

        root = parseString(xml).documentElement
        self.name = root.getAttribute("name")

        self.user_ids = []
        for node in root.childNodes:
            uid = [node.getAttribute("publisher.name"), 
                   node.getAttribute("name")]
            self.user_ids.append(uid)

    def __str__(self):
        return "[" + self.name + ", " + str(self.user_ids) + "]"

class Gnip:
    """Common functionality between all Gnip classes

    This class provides basic functionality help for all Gnip classes.

    """

    def __init__(self, username, password, gnip_server="s.gnipcentral.com"):
        """Initialize the class.

        @type username string
        @param username The Gnip account username
        @type password string
        @param password The Gnip account password
        @type gnip_server string
        @param gnip_server The Gnip server to connect to

        Initializes a Gnip class by setting up authorization
        information, used to log into the Gnip website.

        """

        # Determine base Gnip URL
        self.base_url = "https://" + gnip_server

        # Configure authentication
        self.client = DAVClient(self.base_url)
        self.client.set_basic_auth(username,password)
        self.client.headers['Accept'] = 'application/xml'

    def do_http_delete(self, url_path):
        """Do a HTTP DELETE.

        @type url_path string
        @param url_path The URL to DELETE
        @return string representing page retrieved

        Does a HTTP DELETE request of the passed in url, and returns 
        the result from the server.

        """

        self.client.delete(self.base_url + url_path)
        return self.client.response.body

    def do_http_get(self, url_path):
        """Do a HTTP GET.

        @type url_path string
        @param url_path The URL to GET
        @return string representing page retrieved

        Does a HTTP GET request of the passed in url, and returns 
        the result from the server.

        """

        self.client.get(self.base_url + url_path)
        return self.client.response.body

    def do_http_post(self, url_path, data):
        """Do a HTTP POST.

        @type url_path string
        @param url_path The URL to POST to
        @type data string in XML format
        @param data Formatted POST data
        @return string representing page retrieved

        Does a HTTP POST request of the passed in url and data, and returns 
        the result from the server.

        """

        self.client.post(self.base_url + url_path, data, 
                         {"Content-Type" : "application/xml"})
        return self.client.response.body

    def do_http_put(self, url_path, data):
        """Do a HTTP PUT.

        @type url_path string
        @param url_path The URL to PUT to
        @type data string in XML format
        @param data Formatted PUT data
        @return string representing page retrieved

        Does a HTTP PUT request of the passed in url and data, and returns 
        the result from the server.

        """

        self.client.put(self.base_url + url_path, data, None,
                        {"Content-Type" : "application/xml"})
        return self.client.response.body

    def round_time(self, time):
        """Round time to nearest five minutes.

        @type time datetime
        @param time The time to round
        @return datetime object containing the time at the 
                previous 5 minute mark

        Rounds the time passed in down to the previous 5 minute mark.

        """

        new_min = time.minute - (time.minute % 5)
        return time.replace(minute = new_min, second = 0)

    def sync_clock(self, time):
        """Adjust a time so that it corresponds with Gnip time

        @type time datetime
        @param time The time to adjust
        @return datetime object containing the corrected time

        This method gets the current time from the Gnip server,
        gets the current local time and determines the difference 
        between the two. It then adjusts the passed in time to 
        account for the difference.

        """

        # Do HTTP HEAD request
        self.client.head(self.base_url)

        # Get local time, before we do any other processing
        # so that we can get the two times as close as possible
        local_time = datetime.datetime.utcnow()

        # Get time from headers and parse into python format
        gnip_time = datetime.datetime.strptime(
            self.client.response.getheader("Date"), "%a, %d %b %Y %H:%M:%S %Z")

        # Determine the time difference
        time_delta = gnip_time - local_time

        # Return the corrected time
        return time + time_delta

    def time_to_string(self, time):
        """Convert the time to a formatted string.

        @type theTime datetime
        @param theTime The time to convert to a string
        @return string representing time

        Converts the time passed in to a string of the
        form YYYYMMDDHHMM.

        """

        return str(time.strftime("%Y%m%d%H%M"))

    def publish_activities(self, publisher, activities):
        """Publish activities.

        @type publisher string
        @param publisher string The name of the publisher
        @type activities list of Activity objects
        @param activities The activities to publish
        @return string containing response from the server

        This method takes in a XML document with a list of activities and 
        sends it to the Gnip server.

        """

        activity_xml = '<?xml version="1.0" encoding="UTF-8"?><activities>'
        for activity in activities:
            activity_xml += activity.to_xml()
        activity_xml += '</activities>'

        return self.publish_xml(publisher, activity_xml)

    def publish_xml(self, publisher, activity_xml):
        """Publish activities.

        @type publisher string
        @param publisher string The name of the publisher
        @type activity_xml string
        @param activity_xml XML document formatted to Gnip schema
        @return string containing response from the server

        This method takes in a XML document with a list of activities and 
        sends it to the Gnip server.

        """

        url_path = "/publishers/" + publisher + "/activity.xml"
        return self.do_http_post(url_path, activity_xml)

    def create_collection(self, collection):
        """Create a Gnip collection.

        @type collection Collection
        @param collection A populated Collection object
        @return string containing response from the server

        Creates a new collection on the Gnip server, based on the
        passed in collection.

        """
        return self.create_collection_from_xml(collection.name, collection.to_xml())

    def create_collection_from_xml(self, name, data):
        """Create a Gnip collection.

        @type name string
        @param name The name of the collection to create
        @type data string
        @param XML data formatted to Gnip collection schema
        @return string containing response from the server

        Creates a new collection on the Gnip server, based on the
        passed in parameters.

        """

        url_path = "/collections.xml"
        return self.do_http_post(url_path, data)

    def delete_collection(self, name):
        """Delete a Gnip collection.

        @type name string
        @param name The name of the collection to delete
        @return string containing response from the server

        Deletes an existing collection on the Gnip server, based on the
        name of the collection.

        """

        url_path = "/collections/" + name + ".xml"
        return self.do_http_delete(url_path)

    def find_collection(self, name):
        """Find a Gnip collection.

        @type name string
        @param name The name of the collection to find
        @return string containing response from the server

        Finds an existing collection and returns a Collection representing
        that collection.

        """

        xml = self.find_collection_xml(name)
        collection = Collection()
        collection.from_xml(xml)
        return collection

    def find_collection_xml(self, name):
        """Find a Gnip collection.

        @type name string
        @param name The name of the collection to find
        @return string containing response from the server

        Finds an existing collection and returns the XML representation
        of that collection.

        """

        url_path = "/collections/" + name + ".xml"
        return self.do_http_get(url_path)

    def get_publisher_activities(self, publisher, date_and_time=None):
        """Get the data for a publisher.

        @type publisher string
        @param publisher The publisher of the data
        @type date_and_time datetime
        @param date_and_time The time for which data should be retrieved
        @return list of Activity objects, one for each activity retrieved

        Gets all of the data for a specific publisher, based on the
        date_and_time parameter, which should be a datetime object. If
        date_and_time is not passed in, the current time will be used. 
        Note that all times need to be in UTC.

        """

        xml = self.get_publisher_xml(publisher, date_and_time)
        root = parseString(xml).documentElement
        activities = []
        for node in root.childNodes:
            activity = Activity()
            activity.from_node(node)
            activities.append(activity)
        return activities

    def get_publisher_xml(self, publisher, date_and_time=None):
        """Get the data for a publisher.

        @type publisher string
        @param publisher The publisher of the data
        @type date_and_time datetime
        @param date_and_time The time for which data should be retrieved
        @return string containing response from the server

        Gets all of the data for a specific publisher, based on the
        date_and_time parameter, which should be a datetime object. If
        date_and_time is not passed in, the current time will be used. 
        Note that all times need to be in UTC.

        """

        if None == date_and_time:
            url_path = "/publishers/" + publisher + "/activity/current.xml"
        else:
            corrected_time = self.sync_clock(date_and_time)
            rounded_time = self.round_time(corrected_time)
            time_string = self.time_to_string(rounded_time)
    
            url_path = "/publishers/" + publisher + \
                "/activity/" + time_string + ".xml"

        return self.do_http_get(url_path)

    def get_collection_activities(self, name, date_and_time=None):
        """Get a Gnip collection.

        @type name string
        @param name The name of the collection to get
        @type publisher string
        @param publisher The publisher of the collection
        @type date_and_time datetime
        @param date_and_time The time for which data should be retrieved
        @return string containing response from the server

        Gets all of the data for a specific collection, based on the
        date_and_time parameter, which should be a datetime object. If
        date_and_time is not passed in, the current time will be used.
        Note that all times need to be in UTC.

        """

        xml = self.get_collection_xml(name, date_and_time)
        root = parseString(xml).documentElement
        activities = []
        for node in root.childNodes:
            activity = Activity()
            activity.from_node(node)
            activities.append(activity)
        return activities

    def get_collection_xml(self, name, date_and_time=None):
        """Get a Gnip collection.

        @type name string
        @param name The name of the collection to get
        @type publisher string
        @param publisher The publisher of the collection
        @type date_and_time datetime
        @param date_and_time The time for which data should be retrieved
        @return string containing response from the server

        Gets all of the data for a specific collection, based on the
        date_and_time parameter, which should be a datetime object. If
        date_and_time is not passed in, the current time will be used.
        Note that all times need to be in UTC.

        """

        if None == date_and_time:
            url_path = "/collections/" + name + "/activity/current.xml"
        else:
            corrected_time = self.sync_clock(date_and_time)
            rounded_time = self.round_time(corrected_time)
            time_string = self.time_to_string(rounded_time)
    
            url_path = "/collections/" + name + "/activity/" + \
                time_string + ".xml"

        return self.do_http_get(url_path)


    def update_collection(self, collection):
        """Update a Gnip collection.

        @type collection Collection
        @param collection A populated Collection object
        @return string containing response from the server

        Creates a new collection on the Gnip server, based on the
        passed in parameters.

        """

        return self.update_collection_from_xml(collection.name, collection.to_xml())

    def update_collection_from_xml(self, name, data):
        """Update a Gnip collection.

        @type name string
        @param name The name of the collection to update
        @type data string
        @param XML data formatted to Gnip collection schema
        @return string containing response from the server

        Updates a collection on the Gnip server, based on the
        passed in parameters.

        """

        url_path = "/collections/" + name + ".xml"

        return self.do_http_put(url_path, data)

if __name__=="__main__":

    print "This module was not designed to be called directly."
    print
    print "Try 'from gnip import Gnip'"
    print "or 'from gnip import *'"
