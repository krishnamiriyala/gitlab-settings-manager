#!/usr/bin/env python
# Copyright (c) 2022 Krishna Miriyala<krishnambm@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
# the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
# FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
# COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
# IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


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
            'gitlab-settings-manager=gitlab_settings_manager:gitlab_settings_manager.main',
            'gitlab-add-reviewers=gitlab_settings_manager:gitlab_add_reviewers.main',
        ],
    },
    install_requires=REQUIREMENTS,
)
