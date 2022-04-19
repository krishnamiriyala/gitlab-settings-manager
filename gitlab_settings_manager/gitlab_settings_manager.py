#!/usr/bin/env python

import argparse
import os
import functools
import yaml

import gitlab


def parse_args():
    parser = argparse.ArgumentParser(
        description='Gitlab repo configuration',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-r', '--repo', default='https://gitlab.com',
        help='Gitlab Repo Url')
    parser.add_argument(
        '-p', '--projects', action='extend', nargs='+', default=[],
        help='Gitlab Project Paths like krishna/allgorythms')
    parser.add_argument(
        '--config-file', default='gitlab-project-cfg.yml',
        help='Gitlab Project configuration for different settings')
    args = parser.parse_args()
    return args


def get_groups(gitlab_client, groups):
    return [get_group(gitlab_client, x) for x in groups]


@functools.lru_cache
def get_group(gitlab_client, groupid):
    print('Extracting group id for %s' % groupid)
    return gitlab_client.groups.list(search=groupid)[0].id


def get_users(gitlab_client, users):
    return [get_user(gitlab_client, x) for x in users]


@functools.lru_cache
def get_user(gitlab_client, userid):
    print('Extracting user id for %s' % userid)
    return gitlab_client.users.list(search=userid)[0].id


def update_approvalrules(gitlab_client, project, approvalrules):
    for name, cfg in approvalrules.items():
        print('Checking merge approval rule', name)
        existing = project.approvalrules.list()
        approvals_required = cfg.get('approvals_required', 1)
        rule_type = cfg.get('rule_type', 'regular')
        users = get_users(gitlab_client, cfg.get('users', []))
        groups = get_groups(gitlab_client, cfg.get('groups', []))
        for rule in existing:
            if rule.name == name:
                print('Updating existing merge approval rule', rule.name)
                rule.approvals_required = approvals_required
                rule.rule_type = rule_type
                if users:
                    rule.users = users
                if groups:
                    rule.groups = groups
                rule.save()
                break
            if rule.name.lower() == name.lower():
                print('Deleting conflicting merge approval rule', rule.name)
                rule.delete()
        else:
            print('Creating new merge approval rule', name)
            project.approvalrules.create(dict(
                name=name, approvals_required=approvals_required,
                groups=groups, users=users, rule_type=rule_type))


def update_variables(project, variables):
    variables = {}
    for key, value in variables.items():
        try:
            try:
                variable = project.variables.get(key)
                variable.value = value
                variable.masked = True
                variable.save()
            except gitlab.exceptions.GitlabGetError:
                project.variables.create(
                    {'key': key, 'value': value, 'masked': True})
        except Exception as err:
            print("ERROR: Updating", key, value, err)
    print(variables)


def update_pushrules(project, pushrules):
    existing = project.pushrules.get()
    print(existing)
    for k, val in pushrules.items():
        old = getattr(existing, k)
        if old != val:
            print("Updating %s: %r --> %r" % (k, old, val))
            setattr(existing, k, val)
        else:
            print("NOT Updating %s: %r --> %r" % (k, old, val))
    existing.save()


def main():
    args = parse_args()
    print('Make sure ~/.python-gitlab.cfg or CI_GITLAB_TOKEN is configured '
          'to connect to gitlab')
    if os.environ.get('CI_GITLAB_TOKEN'):
        gitlab_client = gitlab.Gitlab(
            args.repo, private_token=os.environ['CI_GITLAB_TOKEN'])
    else:
        gitlab_client = gitlab.Gitlab.from_config(args.repo)
    cfgyml = yaml.load(open(args.config_file))

    for pname in set(args.projects):
        project = gitlab_client.projects.get(pname)
        print("Updating settings for project", project)
        update_pushrules(project, cfgyml.get('pushrules', {}))
        update_variables(project, cfgyml.get('variables', {}))
        update_approvalrules(
                gitlab_client, project, cfgyml.get('approvalrules', {}))
