#!/usr/bin/env python

"""
Detects missing sysctl's description and report them

--
sbz@FreeBSD.org
"""

import platform
import subprocess
import shlex
import sys

from pprint import pprint as pp


SYSCTL_PREFIX = '/usr/sbin/' if platform.system() == 'Darwin' else '/sbin/'
SYSCTL_CMD = '{}sysctl'.format(SYSCTL_PREFIX)
SYSCTL_ARGS = '-d -a'


def sysctl_desc_empty(desc):
    return desc == ' '


def sysctl_summary(*sysctls):
    count = {}
    categories = ['compat', 'debug', 'dev', 'kern', 'user', 'net', 'hw',
                  'kstat', 'security', 'vfs', 'vm']
    for c in categories:
        count[c] = {}
        count[c]['count'] = 0
        count[c]['oids'] = []

    for s in sysctls:
        for c in categories:
            if s.startswith(c):
                count[c]['count'] += 1
                count[c]['oids'].append(s)
                count[c]['oids'] = sorted(count[c]['oids'])

    return count


def main():
    sysctl_to_fix = []

    p = subprocess.Popen(shlex.split("{} {}".format(SYSCTL_CMD, SYSCTL_ARGS)),
                         stdout=subprocess.PIPE)
    stdout, stderr = p.communicate()

    for sysctl_line in str(stdout).split('\n'):
        if ':' in sysctl_line:
            sysctl_oid, sysctl_desc = sysctl_line.split(':', 1)
            if sysctl_desc_empty(sysctl_desc):
                sysctl_to_fix.append(sysctl_oid)
                # print (sysctl_oid, sysctl_desc)

    print("Number of total sysctl description to fix: {}".format(
        len(sysctl_to_fix)))
    pp(sysctl_summary(*sysctl_to_fix))

    return 0

if __name__ == '__main__':
    sys.exit(main())
