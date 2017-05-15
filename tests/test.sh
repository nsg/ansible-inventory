#!/bin/bash

set -e
trap "kill 0" SIGINT

ansible --version

# Setup a little HTTP server to test the url include
(
  cd tests/test-include/
  python -m SimpleHTTPServer 8080
) &

cd tests
for f in test-*/*.py; do
    (cd .. && ./tests/$f)
done
