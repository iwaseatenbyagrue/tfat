# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='tfat',
    version='0.1',
    packages=find_packages(exclude='tests'),
    include_package_data=True,
    test_runner="test",
    install_requires=[
       "Click",
        "click-plugins",
        "marshmallow",
        "pyYAML",
        "feedparser",
        "paho-mqtt"
    ],
    extras_require={u'tests': [u'pytest', u'pytest-runner', u'pytest-pep8', u'pytest-cov']},
    entry_points='''
[console_scripts]
tfat=tfat.cli:base
[tfat.plugins]
password=plugins.password:cli
download=plugins.download:cli
    '''
)
