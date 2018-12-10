""" Simple Python Setuptools template.

This template is meant to leverage the setuptools
to facilitate requirements and project dependencies
management for multiple environments (prod, dev, ...)

The idea is to use this instead of doing pip freeze
after the completion of a project that usually resulting
extra packages that are not needed.
"""
from setuptools import setup


####################################################
# List of all required packages
####################################################
requires = [
    'django'
]

dev_requires = [
    'rope', 'flake8', 'black',
]

test_requires = [
    'coverage',
]

####################################################
# SETUP
####################################################
setup(
    name='django_tutorial',
    version='0.0.1',

    # Short one-liner
    description='Sample project',

    # Requires for production, always install these
    install_requires=requires,

    # Optional and not required for production.
    # These are usually for development, build, or testing, ...
    extras_require={
        'dev': dev_requires,
        'test': test_requires,
    },

    # Enable this block if this meant to be a PIP package
    # entry_points={
    #     'console_scripts': [
    #         'tutorial = tutorial:main'
    #     ],
    # },
)
