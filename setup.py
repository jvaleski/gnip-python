from setuptools import setup, find_packages

setup(
    name="gnip",
    version="2.1.0",

    packages=find_packages('gnip'),
    package_dir={'gnip':'.'},

    install_requires = [
            'iso8601 == 0.1.4',
            'pyjavaproperties == 0.3',
            'elementtree == 1.2.7_20070827_preview',
            'httplib2 == 0.4'
    ]
)