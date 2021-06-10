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
            raise e

        return stdout

    def clean_files(self) -> bool:
        stdout = self.remote_exec(self.list_cmd)
        files = self.read_stream(stdout)
        if len(files) == 0:
            return False

        if self.dryrun:
            mode = "Dry run"
        else:
            mode = "+"

        for f in files:
            print(f"[{mode}] Cleaning {f.name} from {f.date}", end=' ')
            try:
                self.clean_file(f.name)
            except Exception as e:
                mark = "\u2757"
            else:
                mark = "\N{cross mark}" if self.dryrun else "\u2705"
            print(f"{mark}")

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
        try:
            stdout = self.remote_exec(clean_cmd)
        except Exception as e:
            raise Exception(f"Cleaning error for file {file_name}")

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

    parser.add_argument(
        "-u", "--user", type=str,
        help="Run as user"
    )

    args = parser.parse_args()
    if args.max_year:
        MAX_KEEP_YEAR = args.max_year

    kwargs = {}

    if args.user:
        kwargs.update(user=args.user)

    if args.dryrun:
        kwargs.update(user=args.user)
        kwargs.update(dryrun=True)

    checker = Checker(**kwargs)

    print(f"[+] Process files older than {MAX_KEEP_YEAR} year old")
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
