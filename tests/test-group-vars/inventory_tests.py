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
        loader=dataloader)
    var_manager = VariableManager(loader=dataloader, inventory=yml_inv)

    def test_check_group_var(self):
        host = self.yml_inv.list_hosts("myhost1.example.com")[0]
        yml = self.var_manager.get_vars(host=host)
        self.assertEqual(yml['version'], 1.6, msg="Failed to get group variable")

    def test_that_host_vars_supersedes_group_vars(self):
        host = self.yml_inv.list_hosts("myhost2.example.com")[0]
        yml = self.var_manager.get_vars(host=host)
        self.assertEqual(yml['version'], 2.0, msg="Failed to get group variable")

    def test_that_we_can_set_vars_to_root(self):
        host = self.yml_inv.list_hosts("myhost3.example.com")[0]
        yml = self.var_manager.get_vars(host=host)
        self.assertEqual(yml['version'], 1.0, msg="Failed to get group variable")

if __name__ == '__main__':
    print("\n### Execute test {}\n".format( __file__))
    unittest.main(verbosity=2)
