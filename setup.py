#!/usr/bin/env python
import sys
from distutils.core import setup
 
version = '0.1'
 
kwargs = {
    'name' : 'gnip-python',
    'version' : version,
    'description' : 'Gnip Convenience Class',
    'long_description' : \
    """gnip-python is a convenience class for Gnip API""",
    'author' : 'Gnip',
    'author_email' : 'gnip-community@googlegroups.com',
    'url' : 'http://groups.google.com/group/gnip-community',
    'packages' : ['gnip'],
    }
 
#if sys.hexversion >= 0x02050000:

kwargs['requires'] = ['DAVClient', 'iso8601', 'pyjavaproperties']
kwargs['provides'] = ['gnip']
 
setup(**kwargs)