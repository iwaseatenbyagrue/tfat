# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='tfat',
    version='0.1',
    packages=find_packages(exclude='tests'),
    include_package_data=True,
    install_requires=[
       "Click",
        "click-plugins",
        "marshmallow",
        
    ],
    extras_require={u'dev': [u'pytest', u'pytest-pep8', u'pytest-cov']},
    entry_points='''
[console_scripts]
tfat=tfat.cli:base
    '''
)
