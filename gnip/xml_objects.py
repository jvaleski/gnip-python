class URL(object):
    """Gnip URL container class"""

    def __init__(self, value=None, meta_url=None):

        self.value = value
        self.meta_url = meta_url
        
class Actor(object):
    """Gnip Actor container class"""

    def __init__(self, value=None, uid=None, meta_url=None):

        self.value = value
        self.uid = uid
        self.meta_url = meta_url

class Tag(object):
    """Gnip Tag container class"""

    def __init__(self, value=None, meta_url=None):

        self.value = value
        self.meta_url = meta_url

class To(object):
    """Gnip To container class"""

    def __init__(self, value=None, meta_url=None):

        self.value = value
        self.meta_url = meta_url

class Point(object):
    """Gnip Point container class"""

    def __init__(self, x=None, y=None):

        self.x = x
        self.y = y

    def __str__(self):
        return "[" + str(self.x) + \
            ", " + str(self.y) + \
            "]"

