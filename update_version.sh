#!/usr/bin/env bash

# Updates the SDK version in the right places.
if [ -z "$1" ]; then
    echo "Usage: $0 version" >&2
    exit 1
fi

VERSION="$1"

sed "s/version='[0-9.]*'/version='$VERSION'/" -i setup.py
sed "s/__version__ = .*/__version__ = '$VERSION'/" -i pillarsdk/config.py

git diff
echo
echo "================================================================"
echo "Version updated to $VERSION. Don't forget to commit!"
echo "================================================================"
