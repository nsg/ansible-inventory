#!/bin/bash

SCRIPTPATH=$(dirname $0)
./inventory.py --file $SCRIPTPATH/inventory.yml --list
