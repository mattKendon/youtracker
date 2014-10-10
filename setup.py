__author__ = 'Matthew'

from setuptools import setup, find_packages

setup(
    name='youtracker',
    version='5.0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'requests',
    ]
)