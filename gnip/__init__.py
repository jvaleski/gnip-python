import activities
import activity
import filter
import publisher
import datetime
import iso8601
import time
import gzip
import StringIO
import logging
import httplib2
from elementtree.ElementTree import *
from pyjavaproperties import Properties
from xml_objects import *
from response import *

class Gnip:
    """Provides the primary interface to the Gnip service.
    
    Provides an authenticated connection between your code, and the Gnip servers.
    Gnip's primary functionality is provided through this class.

    """

    def __init__(self, username, password, gnip_server=None):
        """Initialize the class.

        @type username string
        @param username Your Gnip account username
        @type password string
        @param password Your Gnip account password
        @type gnip_server string
        @param gnip_server The Gnip server to connect to

        Initializes a Gnip class by setting up authentication
        information, used to log into the Gnip service.

        """

        index = int(__file__.rfind("/"))
        basedir = __file__[0:index]
        p = Properties()
        p.load(open(basedir + '/gnip.properties'))
        
        # Determine base Gnip URL
        if (gnip_server is None):
            self.base_url = p['gnip.server']
        else:
            self.base_url = gnip_server
        
        self.tunnel_over_post = bool(p['gnip.tunnel.over.post=false'])

        # Configure authentication
        self.client = httplib2.Http(timeout = int(p['gnip.http.timeout']))
        self.client.add_credentials(username, password)

        self.headers = {}
        self.headers['Accept'] = 'gzip, application/xml'
        self.headers['User-Agent'] = 'Gnip-Client-Python/2.1.0'
        self.headers['Content-Encoding'] = 'gzip'
        self.headers['Content-Type'] = 'application/xml'

    def sync_clock(self, theTime):
        """Adjust a time so that it corresponds with Gnip time

        @type datetime datetime
        @param datetime The datetime object to adjust
        @return datetime object representing the corrected time

        This method gets the current time from the Gnip server,
        gets the current local time and determines the difference 
        between the two. It then adjusts the passed in time to 
        account for the difference. This method can be used to ensure
        your application's time is in sync with Gnip server time in
        order to prevent clock drift between the two.

        """

        # Do HTTP HEAD request
        resp, content = self.__do_http_head()

        # Get local time, before we do any other processing
        # so that we can get the two times as close as possible
        local_time = datetime.datetime.utcnow()

        # Get time from headers and parse into python format
        gnip_time = datetime.datetime.strptime(resp["date"], "%a, %d %b %Y %H:%M:%S %Z")

        # Determine the time difference
        time_delta = gnip_time - local_time

        # Return the corrected time
        return theTime + time_delta

    def time_to_string(self, time):
        """Convert the time to a Gnip bucket formatted string.

        @type time time
        @param time The time object to convert to a string
        @return string representing time

        Converts the time passed in to a string of the
        form YYYYMMDDHHMM. Gnip uses this string format for
        notification/activity bucket specification.

        """

        return str(time.strftime("%Y%m%d%H%M"))

    def publish_activities(self, publisher_name, activities):
        """Publish the provided activities to Gnip.

        @type publisher_name string
        @param publisher_name string The name of the publisher to
            receive the activities. You must be the owner of the publisher.
        @type activities list of Activity objects
        @param activities The activities to be published
        @return string containing response from the server

        This method allows a publisher to publish activities to the Gnip
        service. You can only publish activities to a publisher that you own.

        """

        url_path = "/my/publishers/" + publisher_name + "/activity.xml"
        return self.__parse_response(self.__do_http_post(url_path, activities.to_xml()))

    def create_filter(self, publisher_scope, publisher_name, filter):
        """Create a Filter on the Gnip service.

        @type publisher_scope string
        @param publisher_scope The scope of the publisher ("my," "public" or "gnip")  
        @type publisher_name string
        @param publisher_name The publisher that the Filter will be applied to.
        @type filter Filter
        @param filter A populated Filter object
        @return string containing response from the server

        Creates a new filter, specific to your account, on the Gnip service.
        """
        url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/filters.xml"
        return self.__parse_response(self.__do_http_post(url_path, filter.to_xml()))

    def add_rule_to_filter(self, publisher_scope, publisher_name, filter_name, rule):
        """Add a rule to a pre-existing Gnip filter.

        @type publisher_scope string
        @param publisher_scope The scope of the publisher ("my," "public" or "gnip")  
        @type publisher_name string
        @param publisher_name The publisher of the filter to update
        @type filter_name string
        @param filter_name The filter to update
        @type rule string
        @param rule a Rule object to add
        @return string containing response from the server
        """

        url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/filters/" + filter_name + "/rules.xml"
        return self.__parse_response(self.__do_http_post(url_path, rule.to_xml()))

    def add_rules_to_filter(self, publisher_scope, publisher_name, filter_name, rules):
        """Add rules to a Gnip filter.

        @type publisher_scope string
        @param publisher_scope The scope of the publisher ("my," "public" or "gnip")  
        @type publisher_name string
        @param publisher_name The publisher of the filter to update
        @type filter_name string
        @param filter_name The filter to update
        @type rules List of Rule objects
        @param rules List of Rule objects
        @return string containing response from the server
        """

        url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/filters/" + filter_name + "/rules.xml"
        rules_xml = "<rules>"
        for rule in rules:
            rules_xml+=rule.to_xml()
        rules_xml+="</rules>"
        return self.__parse_response(self.__do_http_post(url_path, rules_xml))

    def remove_rule_from_filter(self, publisher_scope, publisher_name, filter_name, rule):
        """Remove a rule from a Gnip filter.

        @type publisher_scope string
        @param publisher_scope The scope of the publisher ("my," "public" or "gnip")  
        @type publisher_name string
        @param publisher_name The publisher of the filter to update
        @type filter_name string
        @param filter_name The filter to update
        @type rule string
        @param rule a Rule to remove
        @return string containing response from the server
        """

        url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/filters/" + filter_name + "/rules"

        return self.__parse_response(self.__do_http_delete(url_path, rule.to_delete_query_string()))

    def rule_exists_in_filter(self, publisher_scope, publisher_name, filter_name, rule):
        """Determine whether or not a given rule exists in an existing Filter.

        @type publisher_scope string
        @param publisher_scope The scope of the publisher ("my," "public" or "gnip") 
        @type publisher_name string
        @param publisher_name The publisher of the filter to update
        @type filter_name string
        @param filter_name The filter to check
        @type rule string
        @param rule a Rule to check
        @return boolean as to the existance of the rule, None if existance of the rule can't be determined
        """

        url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/filters/" + filter_name + "/rules?" + rule.to_delete_query_string()

        response, body = self.__do_http_get(url_path)
        if (response.status == 200):
            return True
        elif (response.status == 404):
            return False
        else:
            return None

    def delete_filter(self, publisher_scope, publisher_name, name):
        """Delete a Gnip filter.

        @type publisher_scope string
        @param publisher_scope The scope of the publisher ("my," "public" or "gnip") 
        @type publisher_name string
        @param publisher_name The publisher to create filter for
        @type name string
        @param name The name of the filter to delete
        @return string containing response from the server
        """

        url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/filters/" + name + ".xml"
        return self.__parse_response(self.__do_http_delete(url_path))

    def find_filter(self, publisher_scope, publisher_name, name):
        """Find an account specific Filter in Gnip.

        @type publisher_scope string
        @param publisher_scope The scope of the publisher ("my," "public" or "gnip") 
        @type publisher_name string
        @param publisher_name The publisher to create filter for
        @type name string
        @param name The name of the filter to find
        @return Response which contains the Filter object
        """

        url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/filters/" + name + ".xml"
        return self.__parse_response(self.__do_http_get(url_path), filter.Filter())

    def get_publisher_activities(self, publisher_scope, publisher_name, date_time=None):
        """Get a Publisher's Activities (as opposed to Notifications).

        @type publisher_scope string
        @param publisher_scope The scope of the publisher ("my," "public" or "gnip") 
        @type publisher_name string
        @param publisher_name The publisher you want Activities for.
        @type date_time datetime
        @param date_time The datetime for which data should be retrieved
        @return List of Activity objects, one for each activity retrieved

        Gets all of the Activities for a specific publisher. You can specify a time
        (in UTC) from which you would like specific Activities, otherwise the current
        time will be used.
        
        See Also: get_publisher_notifications()
        """
        if None == date_time:
            url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/activity/current.xml"
        else:
            corrected_time = self.sync_clock(date_time)
            time_string = self.time_to_string(corrected_time)

            url_path = "/" + publisher_scope + "/publishers/" + publisher_name + \
                "/activity/" + time_string + ".xml"

        return self.__parse_response(self.__do_http_get(url_path), activities.Activities())

    def get_filter_activities(self, publisher_scope, publisher_name, name, date_time=None):
        """Get Activites (as opposed to Notifications) from a Filter.

        @type publisher_scope string
        @param publisher_scope The scope of the publisher (my, public or gnip)  
        @type name string
        @param name The name of the filter you want activities for
        @type publisher_name string
        @param publisher_name The publisher associated with the filter.
        @type date_time datetime
        @param date_time The time for which data should be retrieved
        @return string containing response from the server

        Gets all of the Activities for a specific Filter. You can specify a time
        (in UTC) from which you would like specific Activities, otherwise the current
        time will be used.

        See Also: get_filter_notifications()
        """
        if None == date_time:
            url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/filters/" + name + "/activity/current.xml"
        else:
            corrected_time = self.sync_clock(date_time)
            time_string = self.time_to_string(corrected_time)

            url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/filters/" + name + "/activity/" + \
                time_string + ".xml"

        return self.__parse_response(self.__do_http_get(url_path), activities.Activities())

    def get_publisher_notifications(self, publisher_scope, publisher_name, date_time=None):
        """Get a Publisher's Notifications (as opposed to Activities).

        @type publisher_scope string
        @param publisher_scope The scope of the publisher ("my," "public" or "gnip") 
        @type publisher_name string
        @param publisher_name The publisher you want Notifications for.
        @type date_time datetime
        @param date_time The datetime for which data should be retrieved
        @return List of Activity objects, one for each activity retrieved

        Gets all of the Notifications for a specific publisher. You can specify a time
        (in UTC) from which you would like specific Notifications, otherwise the current
        time will be used.
        
        Gnip currently represents both "Activities" and "Notifications" in the same
        object: Activity. "Notification" and "Activity" Activity objects are identical, with the
        exception of the "Activity" Activity object containing a payload.
        
        See Also: get_publisher_activities()
        """
        if None == date_time:
            url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/notification/current.xml"
        else:
            corrected_time = self.sync_clock(date_time)
            time_string = self.time_to_string(corrected_time)

            url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/notification/" + time_string + ".xml"

        return self.__parse_response(self.__do_http_get(url_path), activities.Activities())

    def get_filter_notifications(self, publisher_scope, publisher_name, name, date_time=None):
        """Get Notifications (as opposed to Activities) from a Filter.

        @type publisher_scope string
        @param publisher_scope The scope of the publisher (my, public or gnip)  
        @type name string
        @param name The name of the filter you want Notifications for
        @type publisher_name string
        @param publisher_name The publisher associated with the filter.
        @type date_time datetime
        @param date_time The time for which data should be retrieved
        @return string containing response from the server

        Gets all of the Notifications for a specific Filter. You can specify a time
        (in UTC) from which you would like specific Notifications, otherwise the current
        time will be used.
        
        Gnip currently represents both "Activities" and "Notifications" in the same
        object: Activity. "Notification" and "Activity" Activity objects are identical, with the
        exception of the "Activity" Activity object containing a payload.

        See Also: get_filter_activities()
        """
        if None == date_time:
            url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/filters/" + name + "/notification/current.xml"
        else:
            corrected_time = self.sync_clock(date_time)
            time_string = self.time_to_string(corrected_time)

            url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/filters/" + name + "/notification/" + time_string + ".xml"

        return self.__parse_response(self.__do_http_get(url_path), activities.Activities())

    def update_filter(self, publisher_scope, publisher_name, filter):
        """Update a Gnip filter.

        @type publisher_scope string
        @param publisher_scope The scope of the publisher (my, public or gnip)  
        @type publisher_name string
        @param publisher_name The publisher of the filter
        @type filter Filter
        @param filte A populated Filter object
        @return string containing response from the server

        Updates the Filter on the Gnip service with the Filter provided.
        The Filter must already exist on the service.

        """
        url_path = "/" + publisher_scope + "/publishers/" + publisher_name + "/filters/" + filter.name + ".xml"
        return self.__parse_response(self.__do_http_put(url_path, filter.to_xml()))

    def create_publisher(self, publisher):
        """Create a Gnip publisher in the "my" scope.

        @type publisher Publisher
        @param publisher A populated Publisher object
        @return string containing response from the server

        Creates a new publisher on the Gnip server within the "my" publisher scope.
        The publisher will be visible only to your account, and only you, can
        publish to it.
        """

        url_path = "/my/publishers"
        return self.__parse_response(self.__do_http_post(url_path, publisher.to_xml()))
    
    def get_publisher(self, scope, name):
        """Get a Gnip publisher.

        @type scope string
        @param scope The scope of the publisher ("my," "public" or "gnip")
        @type name string
        @param name The name of the publisher to get
        @return Publisher object based on response from the server

        Gets a Publisher from the Gnip server. The Publisher object allows
        you to determine what capabilities a Publisher supports. These
        capabilities determine what kind of rules you can use when creating
        a Filter.
        """

        url_path = "/" + scope + "/publishers/" + name + ".xml"
        return self.__parse_response(self.__do_http_get(url_path),publisher.Publisher())

    def update_publisher(self, publisher):
        """Update a Gnip filter.

        @type publisher Publisher
        @param publisher The publisher object to update
        @return string containing response from the server

        Updates a pre-existing Publisher with the Publisher provided.
        """

        url_path = "/my/publishers/" + publisher.name + ".xml"
        return self.__parse_response(self.__do_http_put(url_path, publisher.to_xml()))

    def __compress_with_gzip(self, string):
        if (string is None or len(string) is 0):
            return ""
        zbuf = StringIO.StringIO()
        zfile = gzip.GzipFile(mode='wb', fileobj=zbuf, compresslevel=9)
        zfile.write(string)
        zfile.close()
        return zbuf.getvalue()

    def __do_http_head(self):
        return self.client.request(self.base_url, "HEAD", headers=self.headers)

    def __do_http_get(self, url_path, query_string = None):
        url = self.base_url + url_path
        if query_string is not None:
            url+="?" + query_string
        return self.client.request(url, "GET", headers=self.headers)

    def __do_http_post(self, url_path, data, query_string = None):
        url = self.base_url + url_path
        if query_string is not None:
            url+="?" + query_string
        return self.client.request(url, "POST", headers=self.headers, body=self.__compress_with_gzip(data))

    def __do_http_put(self, url_path, data, query_string = None):
        url = self.base_url + url_path
        if (self.tunnel_over_post):
            url += ';edit'
            verb = "POST"
        else:
            verb = "PUT"

        if query_string is not None:
            url+="?" + query_string

        return self.client.request(url, verb, headers=self.headers, body=self.__compress_with_gzip(data))

    def __do_http_delete(self, url_path, query_string = None):
        url = self.base_url + url_path
        if (self.tunnel_over_post):
            url += ';delete'
            verb = "POST"
        else:
            verb = "DELETE"

        if query_string is not None:
            url+="?" + query_string

        return self.client.request(url, verb, headers=self.headers, body=self.__compress_with_gzip(" "))

    def __parse_response(self, response, data_object=None):
        if (response[0].status == 200):
            if data_object is None:
                return Response(response[0].status, self.__parse_result(response[1]))
            else:
                data_object.from_xml(response[1])
                return Response(response[0].status, data_object)
        else:
            return Response(response[0].status, self.__parse_error(response[1]))

    def __parse_error(self, error_xml):
        logging.info("Parsing error from XML: " + error_xml)
        error = Error()
        error.from_xml(error_xml)
        return error

    def __parse_result(self, result_xml):
        result = Result()
        result.from_xml(result_xml)
        return result
                
if __name__=="__main__":

    print "This module was not designed to be called directly."
    print
    print "Try 'from gnip import Gnip'"
    print "or 'from gnip import *'"