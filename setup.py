#!/usr/bin/env python
from setuptools import setup
import os

with open('requirements.txt') as f:
    required = f.read().splitlines()

setup(
    name = 'hawkeye',
    version = '0.1.0',
    description = 'AWS security policy compliance checking tool',
    install_requires = required,
    author='Michael Henry',
    author_email='mhenry@mozilla.com',
    url="https://github.com/neoCrimeLabs/hawkeye",
    packages = ['hawkeye', 'hawkeye.log', 'hawkeye.audit']

)
