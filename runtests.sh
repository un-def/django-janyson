#!/bin/sh
cd "$(dirname "$0")"
rm .coverage 2> /dev/null
tox $*
EXITCODE=$?
[ -f .coverage ] && coverage report -m
echo "\ntox exited with code: $EXITCODE\n"
exit $EXITCODE

