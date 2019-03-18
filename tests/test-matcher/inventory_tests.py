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
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager

class AnsibleInventoryTests(unittest.TestCase):
    dataloader = DataLoader()
    yml_inv = InventoryManager(
        sources="{}/inv.sh".format(os.path.dirname(__file__)),
        loader=dataloader
    )
    var_manager = VariableManager(loader=dataloader, inventory=yml_inv)

    def test_check_matcher_capture_on_stowww1(self):
        yml = self.yml_inv.get_host("stowww1.example.com").get_vars()
        result = [
            u'com',
            u'example',
            u'root',
            u'root-com',
            u'root-example',
            u'root-site', # from matcher group
            u'root-sto',
            u'root-stowww',
            u'root-test', # from matcher group
            u'root-www',
            u'site',
            u'sto',
            u'stowww',
            u'test',
            u'www'
        ]
        self.assertListEqual(yml['group_names'], result, msg="\nGot:    {}\nExpect: {}".format(yml['group_names'], result))

    def test_check_matcher_capture_on_lonwww2(self):
        yml = self.yml_inv.get_host("lonwww2.example.com").get_vars()
        result = [
            u'com',
            u'example',
            u'lon',
            u'lonwww',
            u'root',
            u'root-com',
            u'root-example',
            u'root-lon',
            u'root-lonwww',
            u'root-site', # from matcher groups
            u'root-www',
            u'site',
            u'www'
        ]
        self.assertListEqual(yml['group_names'], result, msg="\nGot:    {}\nExpect: {}".format(yml['group_names'], result))

    def test_check_matcher_capture_on_londb3(self):
        yml = self.yml_inv.get_host("londb3.example.com").get_vars()
        result = [
            u'com',
            u'db',
            u'example',
            u'lon',
            u'londb',
            u'root',
            u'root-com',
            u'root-db',
            u'root-example',
            u'root-lon',
            u'root-londb'
        ]
        self.assertListEqual(yml['group_names'], result, msg="\nGot:    {}\nExpect: {}".format(yml['group_names'], result))

if __name__ == '__main__':
    print("\n### Execute test {}\n".format( __file__))
    unittest.main(verbosity=2)
