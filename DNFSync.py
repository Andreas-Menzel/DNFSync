#!/usr/bin/env python3

#-------------------------------------------------------------------------------
# DNFSync
#
# Easily save and restore all installed DNF packages.
#
# https://github.com/Andreas-Menzel/DNFSync
#-------------------------------------------------------------------------------
# @author: Andreas Menzel
# @license: MIT License
# @copyright: Copyright (c) 2021 Andreas Menzel
#-------------------------------------------------------------------------------

import argparse
import os.path
from signal import signal, SIGINT
import subprocess

### ARGPARSE ###################################################################
parser = argparse.ArgumentParser(description='Save and restore your DNF apps!', prog='DNFSync')

parser.add_argument('--version', action='version', version='%(prog)s v1.1')
parser.add_argument('-b', '--backup',
    action='store_true',
    help='Create a list of all installed DNF apps.')
parser.add_argument('-i', '--install',
    action='store_true',
    help='Install all DNF apps listed in a file.')
parser.add_argument('-f', '--file',
    default="DNFSync__installed_apps.txt",
    help='Specify the filename where the DNF apps list is stored.')

args = parser.parse_args()
# end - argparse


# get_installed_apps
#
# Reads the list of installed packages from a file and returns it.
#
# @return   [string]    The list of installed packages listed in the file.
def get_installed_apps():
    if not os.path.isfile(args.file):
        print('File', '"' + args.file + '"', 'does not exist.')
        return []

    return_string = ""
    with open(args.file, 'r') as reader:
        return_string = reader.read()

    return return_string.split('\n')[1:-1]


# create_backup
#
# Get the userinstalled packages and save them in a file.
#
# @return   None
def create_backup():
    with open(args.file, 'w') as file:
        subprocess.run(["dnf", "history", "userinstalled"], stdout=file, text=True).stdout


# install
#
# Install a given list of packages.
#
# @param    [string]    apps    List of apps to install.
#
# @return   None
def install(apps):
    args = ["dnf", "install", "-y"]
    args.extend(apps)
    subprocess.run(args)


# end
#
# Ends the script.
#
# @param    int         sig     Signal.
# @param    FrameType   frame   Frame.
#
# @return   None
def end(sig, frame):
    print("Goodbye!")
    exit(0)


if __name__ == '__main__':
    signal(SIGINT, end)

    if args.install:
        install(get_installed_apps())

    if args.backup:
        create_backup()
