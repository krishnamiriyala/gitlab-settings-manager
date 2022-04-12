#!/usr/bin/env python

import argparse
import os
import sys

import setuptools

TOP_DIR = os.path.dirname(__file__)
README = os.path.join(TOP_DIR, "README.md")
REQUIREMENTS = [
    "gitlab",
    "pyyaml",
]


def get_current_date():
    import datetime
    now = datetime.datetime.utcnow()
    return ('%04d%02d%02d' %
            (now.year, now.month, now.day))


parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    '--build-number', default=get_current_date(),
    help='Build Number to be used for packaging [defauts to date]')
args, sys.argv = parser.parse_known_args(sys.argv)
BUILD_NUMBER = args.build_number


setuptools.setup(
    name="gitlab-settings-manager",
    version="0.1.%s" % BUILD_NUMBER,
    author="Krishna Miriyala",
    author_email="krishnambm@gmail.com",
    url="https://github.com/krishnamiriyala/gitlab-settings-manager",
    description="Manage gitlab project settings",
    long_description=open(README, "r").read(),
    packages=setuptools.find_packages(),
    license="AS IS",
    entry_points={
        'console_scripts': [
            'gitlab-settings-manager=gitlab_settings_manager:main',
        ],
    },
    install_requires=REQUIREMENTS,
)
