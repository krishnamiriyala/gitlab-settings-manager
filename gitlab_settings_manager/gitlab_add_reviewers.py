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


from .gitlab_settings_manager import (
    get_default_parser, get_gitlab_client, get_users, update_reviewers)


def parse_args():
    parser = get_default_parser()
    parser.add_argument(
        '-m', '--mr-ids', action='extend', nargs='+', default=[],
        help='Merge request ids to add reviewers to')
    parser.add_argument(
        '--reviewers', action='extend', nargs='+', default=[],
        help='Merge request ids to add reviewers to')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    gitlab_client = get_gitlab_client(args)

    reviewer_ids = get_users(gitlab_client, args.reviewers)
    for pname in set(args.projects):
        project = gitlab_client.projects.get(pname)
        print("Checking settings for project", project)
        for mr_id in set(args.mr_ids):
            update_reviewers(project, mr_id, reviewer_ids)
