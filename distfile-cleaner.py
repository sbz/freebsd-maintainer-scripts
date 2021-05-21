#!/usr/bin/env python3

"""
This simple script is an helper to purge old files left into
freefall:~/public_distfiles for ages to reclaim disk space. 

It uses paramiko, /bin/ls and /bin/rm to delete the obsolete files

--
sbz@FreeBSD.org
"""

import argparse
import datetime
import time
import sys

from dataclasses import dataclass

import paramiko

# by default keep file for at least 5 years
MAX_KEEP_YEAR = 5

__version__ = "1.0"

@dataclass
class FileEntry:
    name: str
    date: str

    def is_older(self) -> bool:

        current_year = datetime.datetime.fromtimestamp(time.time()).year
        year, month, day = self.date.split("-")
        if current_year - int(year) >= MAX_KEEP_YEAR:
            return True

        return False


class Checker(object):
    """Class to purge old FreeBSD distfiles"""

    def __init__(self, host: str="freefall.freebsd.org", user: str="sbz",
                 dryrun: bool=False):
        self.host = host
        self.user = user
        self.path = f"/home/{self.user}/public_distfiles/"
        self.list_cmd = f"ls -ltr -D%F {self.path}"
        self.dryrun = dryrun

    def remote_exec(self, cmd: str) -> str:
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.load_system_host_keys()
        client.connect(self.host)

        try:
            stdin, stdout, stderr = client.exec_command(cmd)
        except paramiko.SSHException as e:
            print(f"Failed to execute remote {cmd}: (stderr: {stderr.read()}")

        return stdout

    def clean_files(self) -> bool:
        stdout = self.remote_exec(self.list_cmd)
        files = self.read_stream(stdout)
        if len(files) == 0:
            return False

        for f in files:
            mode = "+" if not self.dryrun else "Dry run"
            print(f"[{mode}] Cleaning {f.name} dating from {f.date}", end=' ')
            self.clean_file(f.name)
            print(f"\N{check mark}" if not self.dryrun else f"\N{cross mark}")

        return True
        
    def read_stream(self, stream_input: paramiko.Channel) -> list:
        lines = []

        for line in stream_input.readlines()[1:]:
            if line == "":
                continue
            col = line.strip().split()
            f = FileEntry(col[-1], col[-2])
            if f.is_older():
                lines.append(f)

        return lines

    def clean_file(self, file_name: str):
        clean_cmd = f"rm -vf {self.path}{file_name}"
        if self.dryrun:
            clean_cmd = "echo " + clean_cmd
        stdout = self.remote_exec(clean_cmd)

def main() -> int:
    global MAX_KEEP_YEAR

    parser = argparse.ArgumentParser(
        description="Purge old FreeBSD files stored in ~/public_distfiles"
    )

    parser.add_argument(
        "-n", "--dryrun", action='store_true',
        help="Dry run mode. Do not execute remote command"
    )
    parser.add_argument(
        "-m", "--max-year", type=int,
        help="Maximum year to keep the files"
    )

    args = parser.parse_args()
    if args.max_year:
        MAX_KEEP_YEAR = args.max_year

    checker = Checker()
    if args.dryrun:
        checker = Checker(dryrun=True)

    print(f"[+] Only files older than {MAX_KEEP_YEAR}")
    if not checker.clean_files():
        print("Nothing to clean.")
        return 1

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt as e:
        sys.exit(0)
    except SystemExit as sysexit:
        if sysexit.code != 0:
            raise
        else:
            sys.exit(sysexit.code)
    except Exception:
        raise
