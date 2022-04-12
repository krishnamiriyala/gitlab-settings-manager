import argparse
import os
import sys
import yaml

import gitlab


def parse_args():
    parser = argparse.ArgumentParser(
        description='Gitlab repo configuration',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-r', '--repo', default='https://gitlab.com', help='Gitlab Repo Url')
    parser.add_argument('-p', '--projects', action='extend',
                        nargs='+', default=[],
                        help='Gitlab Project Paths like krishna/allgorythms')
    parser.add_argument('--config-file', default='gitlab-project-cfg.yml',
                        help='Gitlab Project configuration for different settings')
    args = parser.parse_args()
    return args


def update_push_rules(project, pushrules):
    existing = project.pushrules.get()
    print(existing)
    for k, v in pushrules.items():
        old = getattr(existing, k)
        if old != v:
            print("Updating %s: %r --> %r" % (k, old, v))
            setattr(existing, k, v)
        else:
            print("NOT Updating %s: %r --> %r" % (k, old, v))
    existing.save()

def main():
    args = parse_args()
    print('Make sure ~/.python-gitlab.cfg or CI_GITLAB_TOKEN is configured '
          'to connect to gitlab')
    if os.environ.get('CI_GITLAB_TOKEN'):
        gl_client = gitlab.Gitlab(
            args.repo, private_token=os.environ['CI_GITLAB_TOKEN'])
    else:
        gl_client = gitlab.Gitlab.from_config(args.repo)
    cfgyml = yaml.load(open(args.config_file))

    for pname in set(args.projects):
        project = gl_client.projects.get(pname)
        update_push_rules(project, cfgyml['pushrules'])
