#!/usr/bin/env python3

"""
sbz poudriere runner
"""

import argparse
import configparser
import os
import shlex
import subprocess
import sys

import colored
from colored import stylize

LOCALBASE="/usr/local"
PORTSDIR="/usr/ports" or os.environ['PORTSDIR']

default_conf="""
[default]
debug=True
disk_path=%s/zfsfs
jails=12amd64,13amd64
jails_disabled=14amd64
mdconfig=False
mdconfig_cmd=mdconfig -f
cpuset=False
cpuset_cmd=cpuset -c -l 0-1

[12amd64]
name=12amd64
arch=amd64
version=12.2-RELEASE

[13amd64]
name=13amd64
arch=amd64
version=13.0-RC1

[14amd64]
name=14amd64
arch=amd64
version=14.0-CURRENT
""" % LOCALBASE

class Prunner(object):
    def __init__(self):
        loadDisk()
        self._jails = loadJails()
        self._port_trees = []
        self.is_setup = True
        if not self.is_setup:
            self.setUp()

    def setUp(self, **params):
        if debug:
            print("setup...")
        #TODO: test if exists to avoid recreating jails
        params['host'] = 'FREEBSD_HOST=ftp.fr.freebsd.org'
        for jail in self._jails:
            cmd = "poudriere jail -c -j {0} -a {1} -v {2} {3}".format(
                jail['name'],
                jail['arch'],
                jail['version'],
                params['host'])
            if debug:
                print("exec: {0}".format(cmd))
            sudo(cmd)

    def tearDown(self):
        #TODO: kill jail (stop them)
        for jail in self._jails:
            cmd = "poudriere jail -k -j {0}".format(jail['name'])
            if debug:
                print("exec: {0}".format(cmd))
            sudo(cmd)

    @property
    def jails(self):
       return self._jails

    @property
    def port_trees(self):
       return self._port_trees

    def testPort(self, origin, port_tree="portsdir"):
        for jail in self._jails:
            if debug:
                print(stylize("testport o: {0} j: {1}".format(origin, jail['name']), colored.fg("magenta")))
            cmd = "poudriere testport -o {0} -j {1} -p {2}".format(
                    origin,
                    jail['name'], port_tree)
            out, err = sudo(cmd)
            if debug:
                print("j: {0}\nout: {1}\nerr: {2}".format(jail['name'], out,
                    err))

    def testAll(self):
        for o in self.sbzports():
            self.test_port(o)

    def bulk(self, jail):
        raise NotImplemented("not available yet")

    def sbzPorts(self):
        #TODO: don't rely on sbzports file
        ports = open('{0}/sbzports'.format(os.path.expanduser('~%s' %
            os.environ['USER'])), 'r').read().strip().split('\n')
        return ports

    def __del__(self):
        if debug:
            print("teardown()...")
        if hasattr(self, 'is_setup') and self.is_setup:
            self.tearDown()

def run(command, use_sudo=False):
    cpuset_cmd = cfg.get('default', 'cpuset_cmd')
    use_cpuset = cfg.getboolean('default', 'cpuset')
    if use_cpuset:
        command = "%s %s" % (cpuset_cmd, command)

    command = "sudo %s" % command if use_sudo else command
    p = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, universal_newlines=True)
    stdout, stderr = p.communicate()
    p.wait()
    return stdout.strip(), stderr

def sudo(command):
    return run(command, use_sudo=True)

def loadDisk():
    if cfg.getboolean('default', 'mdconfig') is False:
        print("Skip mdconfig...\n")
        return

    mdconfig_cmd = cfg.get('default', 'mdconfig_cmd')
    disk_path = cfg.get('default', 'disk_path')
    if not os.path.exists('/dev/md0'):
        out, err = sudo("{0} {1}".format(mdconfig_cmd, disk_path))
        if err is not None:
            print("Error: {0}".format(out))
            sys.exit(1)

def loadJails():
    jails = []
    existing_jails = cfg.get('default', 'jails').split(',')
    try:
        existing_jails.remove(cfg.get('default', 'jails_disabled'))
    except:
        pass

    for jail in existing_jails:
        name = cfg.get(jail, 'name')
        arch = cfg.get(jail, 'arch')
        version = cfg.get(jail, 'version')
        jails.append({'name': name, 'arch': arch, 'version': version})

    return jails

def isValidOrigin(origin):
    abspath = "{0}/{1}".format(PORTSDIR, origin)
    return os.path.isdir(abspath)

def main():
    global cfg, debug
    cfg = configparser.ConfigParser()
    cfg.read_string(default_conf)
    debug = cfg.getboolean('default', 'debug')
    if debug:
        print(cfg.get('default', 'disk_path'))

    runner = Prunner()
    if len(sys.argv) == 1:
        cwd = os.getcwd()
        origin = "{0}/{1}".format(cwd.split('/')[-2], cwd.split('/')[-1])
    else:
        origin = sys.argv[1]

    if isValidOrigin(origin):
        runner.testPort(origin)
    runner.testPort("security/libssh2")

if __name__ == '__main__':
    main()
