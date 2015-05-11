#!/bin/bash

SCRIPTPATH=$( cd $(dirname $0) ; pwd -P )
./inventory.py --file $SCRIPTPATH/inventory.yml --list
