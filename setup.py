#!/usr/bin/env python

from setuptools import setup

setup(name='tap-insided',
      version='0.0.1',
      description='Singer.io tap for extracting data from the inSided API',
      classifiers=['Programming Language :: Python :: 3 :: Only'],
      py_modules=['tap_insided'],
      install_requires=[
        'backoff==1.8.0',
        'ratelimit==2.2.1',
        'requests==2.24.0',
        'singer-python==5.9.0'
      ],
      entry_points='''
          [console_scripts]
          tap-insided=tap_insided:main
      ''',
      packages=['tap_insided'],
      package_data = {
          'tap_insided': ['schemas/*.json'],
      }
)
