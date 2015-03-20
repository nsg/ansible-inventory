#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define your Ansible inventory in structured YAML. Ansible is basically YAML
# and python anyway. I never understood why they choose to introduce INI as
# an inventory format.
#
# This script was written by Stefan Berggren <nsg@nsg.cc> from inspiration
# from Anton Lindström and Tim Rice. This code is released under the MIT
# license.
#
# The MIT License (MIT)
# 
# Copyright (c) 2015 Stefan Berggren
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from __future__ import print_function
import yaml
import json
import sys
import re
import os

# Nice output
def print_json(data):
    print(json.dumps(data, indent=2))

# Load the YAML file
def load_file(file_name):
    with open(file_name, 'r') as fh:
        return yaml.load(fh)

def walk_subgroup(jsn, group, group_path, out, matcher):
    for key in jsn:
        for (k,v) in walk_tree_groups(jsn[key], key, group_path + [key], matcher=matcher).items():
            if k in out:
                out[k]['hosts'] = list(set(out[k]['hosts'] + v['hosts']))
            else:
                out[k] = v
        if group != "":
            if 'children' in out[group]:
                out[group]['children'] = out[group]['children'] + [key]
            else:
                out[group]['children'] = [key]
    return out

# Scan the host against matcher and assign it to groups.
def matcher_full(matcher, host, auto_groups):
    for match in matcher:
        m = re.compile(match['regexp']).match(host)
        if m:
            if 'groups' in match:
                for g in match['groups']:
                    auto_groups.append(g)
            if 'capture' in match and match['capture']:
                for m2 in m.groups():
                    auto_groups.append(m2)
    return auto_groups

def walk_hosts(jsn, group_path, matcher):
    ret = {}
    for host in jsn:
        auto_groups = []

        # Check for key value format
        # Example:
        # - name: myhost01
        if (type(host) == dict):
            if 'tags' in host:
                for tag in host['tags']:
                    auto_groups.append(tag)
            if 'vars' in host:
                for var in host['vars']:
                    auto_groups.append(var)

            host = host['name']

        auto_groups = matcher_full(matcher, host, auto_groups)

        # Split the hostname down to non-[a-z] groups and
        # append these groups to the host.
        for part in re.compile('[^a-z]').split(host):
            if part == "":
                continue
            auto_groups.append(part)
            auto_groups = matcher_full(matcher, host, auto_groups)

        # Assign the host to all groups generated above.
        for grp in group_path + auto_groups + ['-'.join(group_path[:i+1]) for i in range(1,len(group_path))]:
            if grp in ret:
                ret[grp]['hosts'] = list(set(ret[grp]['hosts'] + [host]))
            else:
                ret[grp] = { "hosts": [host] }

    return ret

# Parse 'inventory'
def walk_tree_groups(jsn, group="", group_path=[], out={}, matcher=[]):

    # This is a dict (=group), call my self down the tree
    if type(jsn) == dict:
        out = walk_subgroup(jsn, group, group_path, out, matcher)

    # This is a list (=host), parse the host and return the data
    elif type(jsn) == list:
        return walk_hosts(jsn, group_path, matcher)
    return out

# Scan inventory -> vars for variables and assign them.
# Example:
# vars:
#   - nyc
#     - dns_search: nyc.mycorp.ltd
#   - lon:
#     - dns_search: lon.mycorp.ltd
#     - dns_name: 8.8.8.8
def walk_tree_vars(json_groups, jsn):
    for d in json_groups:
        if type(jsn) == dict:
            if d in jsn:
                v = {}
                for jd in jsn[d]:
                    vp = jd.split("=")
                    v[vp[0]] = vp[1]
                    if 'vars' in json_groups[d]:
                        for v2 in json_groups[d]['vars']:
                            json_groups[d]['vars'][v2] = vp[1]
                    else:
                        json_groups[d]['vars'] = v
    return json_groups

# Parse a file
def parse(ifile, out={}):
    json_data = load_file(os.path.dirname(__file__) + "/" + ifile)

    if 'matcher' in json_data:
        matcher = json_data['matcher']
    else:
        matcher = []
    if 'groups' in json_data:
        json_groups = walk_tree_groups(json_data['groups'], out=out, matcher=matcher)
    if 'vars' in json_data:
        json_groups = walk_tree_vars(json_groups, json_data['vars'])
    if 'include' in json_data:
        for f in json_data['include']:
            parse(f, out)

    return json_groups

# main... duh
def main(argv):
    print_json(parse("inventory.yml"))

if __name__ == '__main__':
    sys.exit(main(sys.argv))
