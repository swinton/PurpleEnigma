#!/usr/bin/env python
from setuptools import find_packages, setup

setup(
    name='PurpleEnigma',
    version='0.0.1',
    description='Quick and dirty encryption and decryption using PyCrypto',
    author='Emma',
    author_email='builders@myemma.com',
    url='',
    packages=find_packages(),
    include_package_data=True,
    package_data={'': ['requirements.txt']},
    install_requires=[
        item for item in
        open("requirements.txt").read().split("\n")
        if item and not item.startswith("-i")])
