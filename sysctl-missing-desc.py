#!/usr/bin/env python

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
Detects missing sysctl's description and report them

--
sbz
"""

import subprocess
import shlex
import sys

from pprint import pprint as pp


SYSCTL_PREFIX = '/sbin/'
SYSCTL_CMD = '{}sysctl'.format(SYSCTL_PREFIX)
SYSCTL_ARGS = '-a -d'


def sysctl_desc_empty(desc):
    return desc == ' '


def sysctl_summary(*sysctls):
    count = {}
    # sysctl -ad | grep ': $'|cut -d '.' -f1|sort -u | xargs echo
    # compat debug dev hw kern kstat net p1003_1b security user vfs vm
    categories = ['compat', 'debug', 'dev', 'hw', 'kern', 'kstat', 'net',
                  'machdep', 'p1003_1b', 'security', 'user', 'vfs', 'vm']
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
    total = 0
    sysctl_to_fix = []

    p = subprocess.Popen(shlex.split("{} {}".format(SYSCTL_CMD, SYSCTL_ARGS)),
                         stdout=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = p.communicate()

    for sysctl_line in str(stdout).splitlines():
        total += 1
        if ':' in sysctl_line:
            sysctl_oid, sysctl_desc = sysctl_line.split(':', 1)
            if sysctl_desc_empty(sysctl_desc):
                sysctl_to_fix.append(sysctl_oid)
                #print (sysctl_oid, sysctl_desc)

    pp(sysctl_summary(*sysctl_to_fix))
    print("Number of total sysctl description to fix: {}/{} ({}%)".format(
        len(sysctl_to_fix), total, len(sysctl_to_fix)/total*100))

    return 0

if __name__ == '__main__':
    sys.exit(main())
