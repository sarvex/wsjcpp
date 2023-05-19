#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import os
import sys
import shutil
import datetime

print ("Welcome to preapre ppa package...")

dists = [
    {
        "name": "Ubuntu 16.04.7 LTS (xenial)",
        "dist_name": "xenial",
        "ppa_name_suffix": "ppa-ubuntu-16-04-xenial-1",
        "end": "April 2021",
        "version": "16.04.7 LTS",
    },
    {
        "name": "Ubuntu 18.04.5 LTS (bionic)",
        "dist_name": "bionic",
        "ppa_name_suffix": "ppa-ubuntu-18-04-bionic-2",
        "end": "April 2023",
        "version": "18.04.5 LTS",
    },
    {
        "name": "Ubuntu 20.04.2 LTS (focal)",
        "dist_name": "focal",
        "ppa_name_suffix": "ppa-ubuntu-20-04-focal-2",
        "end": "April 2025",
        "version": "20.04.2 LTS",
    },
    {
        "name": "Ubuntu 21.04 (Hirsute Hippo)",
        "dist_name": "hirsute",
        "ppa_name_suffix": "ppa-ubuntu-21-04-hirsute-1",
        "end": "January 2022",
        "version": "20.10",
    },
]

print("Please choose dist name:")

i = 0
for d in dists:
    print(
        f'    {str(i)}. '
        + d['dist_name']
        + ' ('
        + d['version']
        + '), date end: '
        + d['end']
    )
    i = i + 1

dist_num_ = input("Enter number of dist: ")
dist_num_ = int(dist_num_)
if dist_num_ >= len(dists):
    sys.exit("Wrong dist number")

dist_name_ = dists[dist_num_]['dist_name']
ppa_name_ = dists[dist_num_]['ppa_name_suffix']

print(f"Dist Name: {dist_name_}")

#############################################

def clear_all():
    print( " -> Clear all")
    if os.path.exists('./wsjcpp'):
        shutil.rmtree('./wsjcpp')
    print( " -> DONE")
    print( " -> Cleanup previous ppa packages")
    onlyfiles = [f for f in os.listdir('./') if os.path.isfile(os.path.join('./', f))]
    for f in onlyfiles:
        if m := re.search(
            r'^wsjcpp_(\d+\.\d+\.\d+)-ppa-.*(\.orig\.tar\.gz|source\.changes|_source\.build|_source.ppa.upload|\.tar\.gz|_source\.buildinfo|\.dsc)$',
            f,
        ):
            print(f'Remove file {f}')
            os.remove(f)

clear_all()

print( " -> Prepare sources directory ")
os.mkdir('./wsjcpp')


def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)

shutil.copytree('../../src', './wsjcpp/src', symlinks=False, ignore=None)
shutil.copytree('../../src.wsjcpp', './wsjcpp/src.wsjcpp', symlinks=False, ignore=None)
shutil.copytree('../../src-resources.wsjcpp', './wsjcpp/src-resources.wsjcpp', symlinks=False, ignore=None)
shutil.copy2('../../CMakeLists.txt', './wsjcpp/CMakeLists.txt')
shutil.copy2('../../VERSION', './wsjcpp/VERSION')
shutil.copy2('../../LICENSE', './wsjcpp/LICENSE')
shutil.copytree('./debian', './wsjcpp/debian', symlinks=False, ignore=None)

print( " -> DONE ")

#############################################

print( " -> Read version of package ")

with open("../../VERSION",'r') as f:
    filedata = f.read()
print(filedata)

if m := re.search('(\\d+\\.\\d+\\.\\d+)', filedata):
    current_version = m[1]

print ("\n *** Current version: " + current_version + "\n")

# parse CHANGELOG.md
changelog_list = []
version_logs = {'version': '', 'dt': '', 'logs': []}
lines = [line.rstrip('\n') for line in open('../../CHANGELOG.md')]
for li in lines:
    if m := re.search(
        r'[ ]*##[ ]+\[v(\d+\.\d+\.\d+)\][ ]*-[ ]*(\d+)-(\d+)-(\d+)[ ]*\((.*)\).*',
        li,
    ):
        if version_logs['version'] != '':
            changelog_list.append(version_logs)
            version_logs = {'version': '', 'dt': '', 'logs': []}
        ver = m[1]
        year = int(m[2])
        month = int(m[3])
        day = int(m[4])
        _dt = datetime.date(year, month, day)

        # must be format Mon, 22 Mar 2010 00:37:31 +0100
        dt = _dt.strftime("%a, %d %b %Y %H:%M:%S +0700")
        version_logs['version'] = ver
        version_logs['dt'] = dt

    if version_logs['version'] == '':
        continue

    if m := re.search('[ ]*-[ ]*(.*)', li):
        line_log = m[1]
        version_logs['logs'].append(line_log)

if version_logs['version'] != '':
    changelog_list.append(version_logs)
    version_logs = {'version': '', 'dt': '', 'logs': []}

print(version_logs)

#############################################

print( " -> Prepare changelog ")

changelog="./wsjcpp/debian/changelog"
with open(changelog,'w') as f:
    li_count = 0
    for li in changelog_list:
        if li_count != 0:
            f.write("\n")
            f.write("\n")
        li_count = li_count + 1
        f.write("wsjcpp (" + li['version'] + "-" + ppa_name_ + ") " + dist_name_ + "; urgency=low\n\n")
        for li_log in li['logs']:
            li_log = li_log.strip()
            if li_log != '':
                f.write(f"  * {li_log}" + "\n")
        f.write("\n")
        #if li['dt'] == '?':
        #    li['dt'] = subprocess.Popen(['date', '-R'], stdout=subprocess.PIPE).communicate()[0]
        f.write(" -- Evgenii Sopov <mrseakg@gmail.com>  " + li['dt']) # 2 space!!!
    f.write("\n")
print( " -> DONE ")

# TODO 
# subprocess.call("./clean_sources_ppa.sh")

#############################################

print( " -> Prepare tar.gz source package ")

os.system(
    f"cd ./ && tar -acf wsjcpp_{current_version}-{ppa_name_}.orig.tar.gz wsjcpp"
)
os.system("cd ./wsjcpp && debuild -S -sa")

print( " -> DONE ")

dput_filename = f"wsjcpp_{current_version}-{ppa_name_}_source.changes"

if (
    os.system(
        f"debsign -k 3AA3105C5766233DD2F243A3A742BE2E628592AC {dput_filename}"
    )
    != 0
):
    print( " -> FAILED ")
    sys.exit(-1)

sys.stdout.write("Are you want try upload source package to ppa.launchpad? [y/n]: ")
ask_upload_ = input().lower()

if ask_upload_ == "y":
    os.system(f"dput ppa:sea5kg/wsjcpp {dput_filename}")
