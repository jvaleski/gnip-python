from elementtree.ElementTree import *
import xml_objects

class Place(object):
    """Gnip Place container class.
    
    A Place represents the geo information in a Gnip Activity.
    """

    def __init__(self, point=None, elev=None, floor=None, feature_type_tag=None, feature_name=None, relationship_tag=None):
        """Initialize the class.

        @type point list of floats
        @param point Point property element containing a pair of coordinates representing latitude then longitude in the WGS84 coordinate reference system
        @type elev float
        @param elev Additional georss property indicating the elevation in meters such as obtained by GPS of the referenced geographic entity.
        @type floor int
        @param floor additional georss property indicating the elevation in building floors of the referenced geographic entity.
        @type feature_type_tag string
        @param feature_type_tag Additional georss property indicating the type of the referenced geographic entity.
        @type feature_name string
        @param feature_name Additional georss property indicating the name or identifier of the referenced geographic entity.
        @type relationship_tag string
        @param relationship_tag Additional georss property indicating the relationship of the accompanying geometric property to the referenced geographic entity.

        """

        self.point = point
        self.elev = elev
        self.floor = floor
        self.feature_type_tag = feature_type_tag
        self.feature_name = feature_name
        self.relationship_tag = relationship_tag

    def from_xml_node(self, place_xml_node):
        """ Populates place from a place xml node
        
        @type place_xml_node Element
        @param place_xml_node an Element representing the place
        """

        if place_xml_node is not None:

            point_node = place_xml_node.find("point")
            if point_node is not None:
                temp_points = point_node.text.split(" ")
                self.point = xml_objects.Point(float(temp_points[0]), float(temp_points[1]))   
            else:
                self.point = None

            elev_node = place_xml_node.find("elev")
            if elev_node is not None:
                self.elev = float(elev_node.text)
            else:
                self.elev = None

            floor_node = place_xml_node.find("floor")
            if floor_node is not None:
                self.floor = int(floor_node.text)
            else:
                self.floor = None

            feature_type_tag_node = place_xml_node.find("featuretypetag")
            if feature_type_tag_node is not None:
                self.feature_type_tag = feature_type_tag_node.text
            else:
                self.feature_type_tag = None

            feature_name_node = place_xml_node.find("featurename")
            if feature_name_node is not None:
                self.feature_name = feature_name_node.text
            else:
                self.feature_name = None

            relationship_tag_node = place_xml_node.find("relationshiptag")
            if relationship_tag_node is not None:
                self.relationship_tag = relationship_tag_node.text
            else:
                self.relationship_tag = None


    def to_xml_node(self):
        """ Return a XML representation of this object

        @return string containing XML representation of the object

        Returns a XML representation of this object.

        """

        place_node = Element("place")

        if self.point is not None:
            point_node = Element("point")
            point_node.text = " ".join([str(self.point.x), str(self.point.y)])
            place_node.append(point_node)

        if self.elev is not None:
            elev_node = Element("elev")
            elev_node.text = str(self.elev)
            place_node.append(elev_node)

        if self.floor is not None:
            floor_node = Element("floor")
            floor_node.text = str(self.floor)
            place_node.append(floor_node)

        if self.feature_type_tag is not None:
            feature_type_tag_node = Element("featuretypetag")
            feature_type_tag_node.text = str(self.feature_type_tag)
            place_node.append(feature_type_tag_node)

        if self.feature_name is not None:
            feature_name_node = Element("featurename")
            feature_name_node.text = str(self.feature_name)
            place_node.append(feature_name_node)

        if self.relationship_tag is not None:
            relationship_tag_node = Element("relationshiptag")
            relationship_tag_node.text = str(self.relationship_tag)
            place_node.append(relationship_tag_node)


        return place_node

    def __str__(self):
        return "[" + str(self.point) + \
            ", " + str(self.elev) + \
            ", " + str(self.floor) + \
            ", " + str(self.feature_type_tag) + \
            ", " + str(self.feature_name) + \
            ", " + str(self.relationship_tag) + \
            "]"
