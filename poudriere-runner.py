#!/usr/bin/env python3

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

"""
sbz poudriere runner
"""

import argparse
import configparser
import os
import shlex
import subprocess
import sys

from typing import Dict

import colored
from colored import stylize

LOCALBASE = "/usr/local"
PORTSDIR = "/usr/ports" or os.environ["PORTSDIR"]

default_conf = (
    """
[default]
debug=False
setup=False
disk_path=%s/zfsfs
jails=12amd64
jails_disabled=11amd64,13amd64,14amd64
mdconfig=False
mdconfig_cmd=mdconfig -f
cpuset=False
cpuset_cmd=cpuset -c -l 0-1
sets_host=FREEBSD_HOST=https://download.FreeBSD.org
port_tree=portsdir

[11amd64]
name=11amd64
arch=amd64
version=11.4-RELEASE

[12amd64]
name=12amd64
arch=amd64
version=12.2-RELEASE

[13amd64]
name=13amd64
arch=amd64
version=13.0-RELEASE

[14amd64]
name=14amd64
arch=amd64
version=14.0-CURRENT
"""
    % LOCALBASE
)


class Prunner(object):
    def __init__(self):
        loadDisk()
        self._jails = loadJails()
        self._port_tree = cfg.get("default", "port_tree")
        self.is_setup = cfg.getboolean("default", "setup")
        if self.is_setup:
            self.setUp()

    def setUp(self, **params: Dict):
        if debug:
            print("Creating jail setup...")
        params["host"] = cfg.get("default", "sets_host")
        for jail in self._jails:
            cmd = "poudriere jail -c -j {0} -a {1} -v {2} {3}".format(
                jail["name"], jail["arch"], jail["version"], params["host"]
            )
            if debug:
                print("exec: {0}".format(cmd))
            sudo(cmd)

    def tearDown(self):
        if debug:
            print("Stoping jails teardown()...")
        for jail in self._jails:
            cmd = "poudriere jail -k -j {0}".format(jail["name"])
            if debug:
                print("exec: {0}".format(cmd))
            sudo(cmd)

    @property
    def jails(self):
        return self._jails

    @property
    def port_tree(self):
        return self._port_tree

    def testPort(self, origin: str, port_tree: str):
        for jail in self._jails:
            if debug:
                print(
                    stylize(
                        "testport o: {0} j: {1}".format(origin, jail["name"]),
                        colored.fg("magenta"),
                    )
                )
            cmd = "poudriere testport -o {0} -j {1} -p {2}".format(
                origin, jail["name"], port_tree
            )
            out, err = sudo(cmd)
            if debug:
                print("j: {0}\nout: {1}\nerr: {2}".format(jail["name"], out, err))

    def testAll(self):
        for o in self.sbzports():
            self.test_port(o)

    def bulk(self, jail):
        raise NotImplemented("not available yet")

    def __del__(self):
        if hasattr(self, "is_setup") and self.is_setup:
            self.tearDown()


def run(command: str, use_sudo=False) -> str:
    cpuset_cmd = cfg.get("default", "cpuset_cmd")
    use_cpuset = cfg.getboolean("default", "cpuset")
    if use_cpuset:
        command = "%s %s" % (cpuset_cmd, command)

    command = "sudo %s" % command if use_sudo else command
    p = subprocess.Popen(
        shlex.split(command), stdout=subprocess.PIPE, universal_newlines=True
    )
    stdout, stderr = p.communicate()
    p.wait()

    return stdout.strip(), stderr


def sudo(command: str):
    return run(command, use_sudo=True)


def loadDisk():
    if cfg.getboolean("default", "mdconfig") is False:
        if debug:
            print("Skip mdconfig...\n")
        return

    mdconfig_cmd = cfg.get("default", "mdconfig_cmd")
    disk_path = cfg.get("default", "disk_path")
    if not os.path.exists("/dev/md0"):
        out, err = sudo("{0} {1}".format(mdconfig_cmd, disk_path))
        if err is not None:
            print("Error: {0}".format(out))
            sys.exit(1)


def loadJails():
    jails = []
    existing_jails = cfg.get("default", "jails").split(",")
    try:
        existing_jails.remove(cfg.get("default", "jails_disabled"))
    except Exception:
        pass

    for jail in existing_jails:
        name = cfg.get(jail, "name")
        arch = cfg.get(jail, "arch")
        version = cfg.get(jail, "version")
        jails.append({"name": name, "arch": arch, "version": version})

    return jails


def isValidOrigin(origin: str):
    abspath = "{0}/{1}".format(PORTSDIR, origin)

    return os.path.isdir(abspath)


def main():
    global cfg, debug
    cfg = configparser.ConfigParser()
    cfg.read_string(default_conf)
    debug = cfg.getboolean("default", "debug")
    if debug:
        print(cfg.get("default", "disk_path"))

    runner = Prunner()
    if len(sys.argv) == 1:
        cwd = os.getcwd()
        origin = "{0}/{1}".format(cwd.split("/")[-2], cwd.split("/")[-1])
    else:
        origin = sys.argv[1]

    if isValidOrigin(origin):
        runner.testPort(origin, runner.port_tree)

    return 0


if __name__ == "__main__":
    sys.exit(main())
