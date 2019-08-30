#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Set up the dpipe package.
"""

from setuptools import setup


setup(
    name='dpipe',
    version='0.0.1',
    packages=['dpipe'],
    install_requires=['pandas >= 0.24.0', 'pytest'],
    url='https://github.com/xh2/data-pipeline',
    license='MIT',
    author='sm-art',
    author_email='mail@s-m.dev',
    description='Minimum viable DataFrame pipeline.'
)
