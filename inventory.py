#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Define your Ansible inventory in structured YAML. Ansible is basically YAML
# and python anyway. I never understood why they choose to introduce INI as
# an inventory format.
#
# This script was written by Stefan Berggren <nsg@nsg.cc> from inspiration
# from Anton Lindström and Tim Rice. This code is released under the MIT
# license.

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

        # Scan the host against matcher and assign it to groups.
        # This matcher works against the full hostname.
        # Example:
        # - regexp: 'myhost[0-9]'
        #   groups:
        #     - myhost
        for match in matcher:
            m = re.compile(match['regexp']).match(host)
            if m:
                if 'groups' in match:
                    for g in match['groups']:
                        auto_groups.append(g)

        # Split the hostname down to non-[a-z] groups and
        # append these groups to the host.
        for part in re.compile('[^a-z]').split(host):
            if part == "":
                continue
            auto_groups.append(part)

            # Scan the partial hostname against the matcher and
            # assign groups. This example will assign the group
            # nyc to sitenyc-myhost01, sto to sitesto-myhost01
            # and so on ...
            # Example:
            # - regexp: 'site(nyc|lon|sto)'
            #   part: true
            for match in matcher:
                m = re.compile(match['regexp']).match(part)
                if m:
                    if 'part' in match and match['part']:
                        for m2 in m.groups():
                            auto_groups.append(m2)

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
                    json_groups[d]['vars'] = v
    return json_groups

# main... duh
def main(argv):

    json_data = load_file(os.path.dirname(__file__) + "/inventory.yml")
    matcher = json_data['matcher'] or []

    if 'groups' in json_data:
        json_groups = walk_tree_groups(json_data['groups'], matcher=matcher)
    if 'vars' in json_data:
        json_vars = walk_tree_vars(json_groups, json_data['vars'])

    print_json(json_vars)

if __name__ == '__main__':
    sys.exit(main(sys.argv))
