#!/usr/bin/env python

# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function
import time
import os
import string
import codecs

import six


_TEMPLATES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "templates")

_GITHUB_PAGES_BRANCHES = {
    'personal': 'master',
    'project': 'gh-pages'
}

CONF = {
    'pelican': 'pelican',
    'pelicanopts': '',
    'basedir': os.curdir,
    'ftp_host': 'localhost',
    'ftp_user': 'anonymous',
    'ftp_target_dir': '/',
    'ssh_host': 'localhost',
    'ssh_port': 22,
    'ssh_user': 'root',
    'ssh_target_dir': '/var/www',
    's3_bucket': 'my_s3_bucket',
    'cloudfiles_username': 'my_rackspace_username',
    'cloudfiles_api_key': 'my_rackspace_api_key',
    'cloudfiles_container': 'my_cloudfiles_container',
    'dropbox_dir': '~/Dropbox/Public/',
    'github_pages_branch': _GITHUB_PAGES_BRANCHES['project'],
    'default_pagination': 10,
    'siteurl': '',
    'lang': 'en',
    'timezone': 'Europe/Istanbul'
}


def get_template(name, as_encoding='utf-8'):
    template = os.path.join(_TEMPLATES_DIR, "{0}.in".format(name))

    if not os.path.isfile(template):
        raise RuntimeError("Cannot open {0}".format(template))

    with codecs.open(template, 'r', as_encoding) as fd:
        line = fd.readline()
        while line:
            yield line
            line = fd.readline()
        fd.close()


def sample():
    """
    Sample create method with demo data.
    :return:
    """
    params = {
        'basedir': '/tmp/myblog-%d' % int(time.time()),
        'sitename': 'My Super Blog',
        'author': 'John Doe',
        'lang': 'en',
        'siteurl': 'http://example.com',
        'with_pagination': True,
        'default_pagination': 5,
        'timezone': 'Europe/Paris',
        'ftp_host': 'ftp.example.com',
        'ftp_user': 'root',
        'ftp_target_dir': '/',
        'ssh_host': 'example.com',
        'ssh_port': 22,
        'ssh_user': 'root',
        'ssh_target_dir': '/var/www',
        's3_bucket': 'my_s3_bucket',
        'cloudfiles_username': 'my_rackspace_username',
        'cloudfiles_api_key': 'my_rackspace_api_key',
        'cloudfiles_container': 'my_cloudfiles_container',
        'dropbox_dir': '~/Dropbox/Public/',
        'github_pages_branch': 'personal',  # alternative is 'project'
    }

    create(params)


def create(params):
    """
    Creates a new blog according to given parameters.
    :param params: a dictionary containing parameters.
    :return:

    Deployment fields do not have to be provided.

    Sample parameter dictionary:

    params = {
        'basedir': '/tmp/myblog-%d' % int(time.time()),
        'sitename': 'My Super Blog',
        'author': 'John Doe',
        'lang': 'en',
        'siteurl': 'http://example.com',
        'with_pagination': True,
        'default_pagination': 5,
        'timezone': 'Europe/Paris',
        'ftp_host': 'ftp.example.com',
        'ftp_user': 'root',
        'ftp_target_dir': '/',
        'ssh_host': 'example.com',
        'ssh_port': 22,
        'ssh_user': 'root',
        'ssh_target_dir': '/var/www',
        's3_bucket': 'my_s3_bucket',
        'cloudfiles_username': 'my_rackspace_username',
        'cloudfiles_api_key': 'my_rackspace_api_key',
        'cloudfiles_container': 'my_cloudfiles_container',
        'dropbox_dir': '~/Dropbox/Public/',
        'github_pages_branch': 'personal',  # alternative is 'project'
    }

    """
    CONF['basedir'] = params.get('basedir', '.')
    CONF['sitename'] = params.get('sitename', 'My Blog')
    CONF['author'] = params.get('author', 'John Doe')
    CONF['lang'] = params.get('lang', 'en')

    if params.get('siteurl'):
        CONF['siteurl'] = params.get('siteurl')

    CONF['with_pagination'] = params.get('with_pagination', True)

    if CONF['with_pagination']:
        CONF['default_pagination'] = params.get('default_pagination', 5)
    else:
        CONF['default_pagination'] = False

    if params.get('timezone'):
        CONF['timezone'] = params.get('timezone')

    automation = True
    develop = True

    if automation:
        if params.get('ftp_host') and params.get('ftp_user'):
            CONF['ftp_host'] = params.get('ftp_host')
            CONF['ftp_user'] = params.get('ftp_user')
            CONF['ftp_target_dir'] = params.get('ftp_target_dir', '/')
        if params.get('ssh_host'):
            CONF['ssh_host'] = params.get('ssh_host')
            CONF['ssh_port'] = params.get('ssh_port', 22)
            CONF['ssh_user'] = params.get('ssh_user', 'root')
            CONF['ssh_target_dir'] = params.get('ssh_target_dir', '/var/www')

        if params.get('dropbox_dir'):
            CONF['dropbox_dir'] = params.get('dropbox_dir')

        if params.get('s3_bucket'):
            CONF['s3_bucket'] = params.get('s3_bucket')

        if params.get('cloud_files_username'):
            CONF['cloudfiles_username'] = params.get('cloudfiles_username')
            CONF['cloudfiles_api_key'] = params.get('cloudfiles_api_key')
            CONF['cloudfiles_container'] = params.get('cloudfiles_container')

        gpb = params.get('github_pages_branch')
        if gpb == "personal":
            CONF['github_pages_branch'] = _GITHUB_PAGES_BRANCHES['personal']
        elif gpb == "project":
            CONF['github_pages_branch'] = _GITHUB_PAGES_BRANCHES['project']

    try:
        os.makedirs(os.path.join(CONF['basedir'], 'content'))
    except OSError as e:
        print('Error: {0}'.format(e))

    try:
        os.makedirs(os.path.join(CONF['basedir'], 'output'))
    except OSError as e:
        print('Error: {0}'.format(e))

    try:
        with codecs.open(os.path.join(CONF['basedir'], 'pelicanconf.py'), 'w', 'utf-8') as fd:
            conf_python = dict()
            for key, value in CONF.items():
                conf_python[key] = repr(value)

            for line in get_template('pelicanconf.py'):
                template = string.Template(line)
                fd.write(template.safe_substitute(conf_python))
            fd.close()
    except OSError as e:
        print('Error: {0}'.format(e))

    try:
        with codecs.open(os.path.join(CONF['basedir'], 'publishconf.py'), 'w', 'utf-8') as fd:
            for line in get_template('publishconf.py'):
                template = string.Template(line)
                fd.write(template.safe_substitute(CONF))
            fd.close()
    except OSError as e:
        print('Error: {0}'.format(e))

    if automation:
        try:
            with codecs.open(os.path.join(CONF['basedir'], 'fabfile.py'), 'w', 'utf-8') as fd:
                for line in get_template('fabfile.py'):
                    template = string.Template(line)
                    fd.write(template.safe_substitute(CONF))
                fd.close()
        except OSError as e:
            print('Error: {0}'.format(e))
        try:
            with codecs.open(os.path.join(CONF['basedir'], 'Makefile'), 'w', 'utf-8') as fd:
                mkfile_template_name = 'Makefile'
                py_v = 'PY?=python'
                if six.PY3:
                    py_v = 'PY?=python3'
                template = string.Template(py_v)
                fd.write(template.safe_substitute(CONF))
                fd.write('\n')
                for line in get_template(mkfile_template_name):
                    template = string.Template(line)
                    fd.write(template.safe_substitute(CONF))
                fd.close()
        except OSError as e:
            print('Error: {0}'.format(e))

    if develop:
        conf_shell = dict()
        for key, value in CONF.items():
            if isinstance(value, six.string_types) and ' ' in value:
                value = '"' + value.replace('"', '\\"') + '"'
            conf_shell[key] = value
        try:
            with codecs.open(os.path.join(CONF['basedir'], 'develop_server.sh'), 'w', 'utf-8') as fd:
                lines = list(get_template('develop_server.sh'))
                py_v = 'PY=${PY:-python}\n'
                if six.PY3:
                    py_v = 'PY=${PY:-python3}\n'
                lines = lines[:4] + [py_v] + lines[4:]
                for line in lines:
                    template = string.Template(line)
                    fd.write(template.safe_substitute(conf_shell))
                fd.close()
                os.chmod((os.path.join(CONF['basedir'], 'develop_server.sh')), 493)  # mode 0o755
        except OSError as e:
            print('Error: {0}'.format(e))

    print('Done. Your new project is available at %s' % CONF['basedir'])


if __name__ == "__main__":
    sample()
