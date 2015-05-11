#!/bin/bash

set -e

cd tests
for f in */*.py; do
    (cd .. && ./tests/$f)
done
