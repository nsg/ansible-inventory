#!/bin/bash

set -e

ansible --version

cd tests
for f in */*.py; do
    (cd .. && ./tests/$f)
done
