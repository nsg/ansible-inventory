#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Tests to compare the ini and yaml based inventorys.
#
# This script was written by Stefan Berggren <nsg@nsg.cc>
# This code is released under the MIT license.
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
import os
import unittest
import operator

from ansible import errors
from ansible.inventory import Inventory

class AnsibleInventoryTests(unittest.TestCase):

    yml_inv = Inventory("inventory.py")
    ini_inv = Inventory("inventory.ini")

    ##
    # Compare the INI and YAML inventory.
    ##

    def check_var(self, host):
        yml = self.yml_inv.get_variables(host)
        ini = self.ini_inv.get_variables(host)
        self.assertDictEqual(yml, ini, 
                msg="Failed on {}\nYML: {}\nINI: {}".format(host, yml, ini))

    def test_list_hosts(self):
        yml = sorted(self.yml_inv.list_hosts())
        ini = sorted(self.ini_inv.list_hosts())
        self.assertListEqual(yml, ini, msg="\nYML: {}\nINI: {}".format(yml, ini))

    def test_check_vars_and_groups(self):
        for host in self.yml_inv.list_hosts():
            self.check_var(host)

    ##
    # Make specific tests on the YAML inventory
    ##

    def test_var_on_matcher_groups(self):
        yml = self.yml_inv.get_variables("lonprod-pres02")
        self.assertEqual(yml['search'], 'lon.mysite.ltd',
                msg="search was not 'lon.mysite.ltd'")

    def test_var_on_host(self):
        yml = self.yml_inv.get_variables("stoint-docker02")
        self.assertEqual(yml['baz'], 3,
                msg="baz was not 3")

    def test_hash_merge(self):
        yml = self.yml_inv.get_variables("stoint-docker02")
        self.assertEqual(yml['bar'], 1,
                msg="bar was not 1")

    def test_hash_merge_and_overwrite(self):
        yml = self.yml_inv.get_variables("nyctest-docker01")
        self.assertEqual(yml['foo'], 2,
                msg="foo was not 2")

if __name__ == '__main__':
        unittest.main(verbosity=2)
