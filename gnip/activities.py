from elementtree.ElementTree import *
import activity

class Activities(object):
    """A list of Gnip Activities."""

    def __init__(self, activitiyList=[]):
        self.items = activitiyList

    def to_xml(self):
        activity_xml = '<?xml version="1.0" encoding="UTF-8"?><activities>'
        for activity in self.items:
            xml = activity.to_xml()
            activity_xml += xml
        activity_xml += '</activities>'
        return activity_xml

    def from_xml(self, activities_xml):
        root = fromstring(activities_xml)
        activity_nodes = root.findall("activity")
        self.activities = []
        for node in activity_nodes:
            an_activity = activity.Activity()
            an_activity.from_xml_node(node)
            self.items.append(an_activity)
