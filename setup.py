#!/usr/bin/env python

from setuptools import setup

setup(name='planner',
      packages=['planner', 'planner.maps', 'planner.utils'],
      version='0.1.0',
      install_requires=[
            'networkx',
            'pyYAML',
            'numpy',
            'matplotlib',
            'importlib_resources'
      ],
      description='Planner for experiments with MRTA',
      author='Angela Enriquez Gomez',
      author_email='angela.enriquez@smail.inf.h-brs.de',
      package_dir={'': '.'}
      )
