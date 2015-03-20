#!/bin/bash

set -x
set -e
set -o pipefail

ansible-playbook -i inventory.ini -c local tests/site.yml | tee /tmp/out
grep -vq skipping /tmp/out
ansible-playbook -i inventory.py -c local tests/site.yml | tee /tmp/out
grep -vq skipping /tmp/out

set +x

echo "#"
echo "# TEST OK!"
echo "#"
