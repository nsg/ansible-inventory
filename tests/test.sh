#!/bin/bash

set -e

ansible --version

cd tests
for f in test-*/*.py; do
    (cd .. && ./tests/$f)
done
