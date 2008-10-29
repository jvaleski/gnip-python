import activity
import filter
import datetime
import davclient
import iso8601
import time
import httplib2
import gzip
import StringIO
from xml.dom.minidom import parseString

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
        self.client = davclient.DAVClient(self.base_url)
        self.client.set_basic_auth(username,password)
        self.client.headers['Accept'] = 'application/xml'
        self.client.headers['User-Agent'] = 'Gnip-Client-Python/2.0.1'
        self.client.headers['Content-Encoding'] = 'gzip'
        self.client.headers['Content-Type'] = 'application/xml'


    def compress_with_gzip(self, string):
        """Compress a string with GZIP

        @type string string
        @param string The data to compress
        @return string gzipped data

        Does a proper gzip of the incoming string and returns it as a string

        """
        zbuf = StringIO.StringIO()
        zfile = gzip.GzipFile(mode='wb', fileobj=zbuf, compresslevel=9)
        zfile.write(string)
        zfile.close()
        return zbuf.getvalue()

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
    
    def do_http_head(self):
        """Do a HTTP HEAD.

        @return response object

        Does a HTTP HEAD request of the Gnip Server

        """

        self.client.head(self.base_url)
        return self.client.response

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

        self.client.post(self.base_url + url_path, self.compress_with_gzip(data))
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
        
        self.client.put(self.base_url + url_path, self.compress_with_gzip(data))
        return self.client.response.body

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
        resp = self.do_http_head()

        # Get local time, before we do any other processing
        # so that we can get the two times as close as possible
        local_time = datetime.datetime.utcnow()

        # Get time from headers and parse into python format
        gnip_time = datetime.datetime.strptime(
            resp.getheader("Date"), "%a, %d %b %Y %H:%M:%S %Z")

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

    def create_filter(self, publisher, filter):
        """Create a Gnip filter.

        @type publisher string
        @param publisher The publisher to create filter for
        @type filter Filter
        @param filter A populated Filter object
        @return string containing response from the server

        Creates a new filter on the Gnip server, based on the
        passed in filter.

        """
        return self.create_filter_from_xml(publisher, filter.to_xml())

    def create_filter_from_xml(self, publisher, data):
        """Create a Gnip filter.

        @type publisher string
        @param publisher The publisher to create filter for
        @type data string
        @param data XML formatted to Gnip filter schema
        @return string containing response from the server

        Creates a new filter on the Gnip server, based on the
        passed in parameters.

        """

        url_path = "/publishers/" + publisher + "/filters.xml"
        return self.do_http_post(url_path, data)

    def delete_filter(self, publisher, name):
        """Delete a Gnip filter.

        @type name string
        @param name The name of the filter to delete
        @return string containing response from the server

        Deletes an existing filter on the Gnip server, based on the
        name of the filter.

        """

        url_path = "/publishers/" + publisher + "/filters/" + name + ".xml"
        return self.do_http_delete(url_path)

    def find_filter(self, publisher, name):
        """Find a Gnip filter.

        @type publisher string
        @param publisher The publisher to create filter for
        @type name string
        @param name The name of the filter to find
        @return string containing response from the server

        Finds an existing filter and returns a Filter representing
        that filter.

        """

        xml = self.find_filter_xml(publisher, name)
        if "<error>" in xml:
            return None
        the_filter = filter.Filter()
        the_filter.from_xml( xml)
        return the_filter

    def find_filter_xml(self, publisher, name):
        """Find a Gnip filter.

        @type publisher string
        @param publisher The publisher to create filter for
        @type name string
        @param name The name of the filter to find
        @return string containing response from the server

        Finds an existing filter and returns the XML representation
        of that filter.

        """

        url_path = "/publishers/" + publisher + "/filters/" + name + ".xml"
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

        xml = self.get_publisher_activities_xml(publisher, date_and_time)
        root = parseString(xml).documentElement
        activities = []
        for node in root.childNodes:
            if node.tagName == 'activity':
                an_activity = activity.Activity()
                an_activity.from_node(node)
                activities.append(an_activity)
        return activities

    def get_publisher_activities_xml(self, publisher, date_and_time=None):
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
            time_string = self.time_to_string(corrected_time)
    
            url_path = "/publishers/" + publisher + \
                "/activity/" + time_string + ".xml"

        xml = self.do_http_get(url_path)
        print xml

        return xml 

    def get_filter_activities(self, publisher, name, date_and_time=None):
        """Get a Gnip filter.

        @type name string
        @param name The name of the filter to get
        @type publisher string
        @param publisher The publisher of the filter
        @type date_and_time datetime
        @param date_and_time The time for which data should be retrieved
        @return string containing response from the server

        Gets all of the data for a specific filter, based on the
        date_and_time parameter, which should be a datetime object. If
        date_and_time is not passed in, the current time will be used.
        Note that all times need to be in UTC.

        """

        xml = self.get_filter_activities_xml(publisher, name, date_and_time)
        root = parseString(xml).documentElement
        activities = []
        for node in root.childNodes:
            if node.tagName == 'activity':
                an_activity = activity.Activity()
                an_activity.from_node(node)
                activities.append(an_activity)
        return activities

    def get_filter_activities_xml(self, publisher, name, date_and_time=None):
        """Get a Gnip filter.

        @type name string
        @param name The name of the filter to get
        @type publisher string
        @param publisher The publisher of the filter
        @type date_and_time datetime
        @param date_and_time The time for which data should be retrieved
        @return string containing response from the server

        Gets all of the data for a specific filter, based on the
        date_and_time parameter, which should be a datetime object. If
        date_and_time is not passed in, the current time will be used.
        Note that all times need to be in UTC.

        """

        if None == date_and_time:
            url_path = "/publishers/" + publisher + "/filters/" + name + "/activity/current.xml"
        else:
            corrected_time = self.sync_clock(date_and_time)
            time_string = self.time_to_string(corrected_time)
    
            url_path = "/publishers/" + publisher + "/filters/" + name + "/activity/" + \
                time_string + ".xml"

        return self.do_http_get(url_path)
    
    def get_publisher_notifications(self, publisher, date_and_time=None):
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

        xml = self.get_publisher_notifications_xml(publisher, date_and_time)
        root = parseString(xml).documentElement
        activities = []
        for node in root.childNodes:
            if node.tagName == 'activity':
                an_activity = activity.Activity()
                an_activity.from_node(node)
                activities.append(an_activity)
        return activities

    def get_publisher_notifications_xml(self, publisher, date_and_time=None):
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
            url_path = "/publishers/" + publisher + "/notification/current.xml"
        else:
            corrected_time = self.sync_clock(date_and_time)
            time_string = self.time_to_string(corrected_time)
    
            url_path = "/publishers/" + publisher + \
                "/notification/" + time_string + ".xml"

        return self.do_http_get(url_path)

    def get_filter_notifications(self, publisher, name, date_and_time=None):
        """Get a Gnip filter.

        @type name string
        @param name The name of the filter to get
        @type publisher string
        @param publisher The publisher of the filter
        @type date_and_time datetime
        @param date_and_time The time for which data should be retrieved
        @return string containing response from the server

        Gets all of the data for a specific filter, based on the
        date_and_time parameter, which should be a datetime object. If
        date_and_time is not passed in, the current time will be used.
        Note that all times need to be in UTC.

        """

        xml = self.get_filter_notifications_xml(publisher, name, date_and_time)
        root = parseString(xml).documentElement
        activities = []
        for node in root.childNodes:
            if node.tagName == 'activity':
                an_activity = activity.Activity()
                an_activity.from_node(node)
                activities.append(an_activity)
        return activities

    def get_filter_notifications_xml(self, publisher, name, date_and_time=None):
        """Get a Gnip filter.

        @type name string
        @param name The name of the filter to get
        @type publisher string
        @param publisher The publisher of the filter
        @type date_and_time datetime
        @param date_and_time The time for which data should be retrieved
        @return string containing response from the server

        Gets all of the data for a specific filter, based on the
        date_and_time parameter, which should be a datetime object. If
        date_and_time is not passed in, the current time will be used.
        Note that all times need to be in UTC.

        """

        if None == date_and_time:
            url_path = "/publishers/" + publisher + "/filters/" + name + "/notification/current.xml"
        else:
            corrected_time = self.sync_clock(date_and_time)
            rounded_time = self.round_time(corrected_time)
            time_string = self.time_to_string(rounded_time)
    
            url_path = "/publishers/" + publisher + "/filters/" + name + "/notification/" + \
                time_string + ".xml"

        return self.do_http_get(url_path)

    def update_filter(self, publisher, filter_to_update):
        """Update a Gnip filter.

        @type filter_to_update Filter
        @param filter_to_update A populated Filter object
        @return string containing response from the server

        Creates a new filter on the Gnip server, based on the
        passed in parameters.

        """

        return self.update_filter_from_xml(publisher, filter_to_update.name, filter_to_update.to_xml())

    def update_filter_from_xml(self, publisher, name, data):
        """Update a Gnip filter.

        @type name string
        @param name The name of the filter to update
        @type data string
        @param XML data formatted to Gnip filter schema
        @return string containing response from the server

        Updates a filter on the Gnip server, based on the
        passed in parameters.

        """

        url_path = "/publishers/" + publisher + "/filters/" + name + ".xml"
        return self.do_http_put(url_path, data)

if __name__=="__main__":

    print "This module was not designed to be called directly."
    print
    print "Try 'from gnip import Gnip'"
    print "or 'from gnip import *'"
