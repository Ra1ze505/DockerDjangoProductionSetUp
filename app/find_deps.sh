#!/bin/sh

set -e

DEPS=$(find $1 -type f -perm /a+x -o -name '*.so' \
        | xargs -n1 ldd 2>1 \
        | grep "=>" \
        | awk '{print $3;}' \
        | grep "/" \
        | sort -u)

echo "$DEPS" | xargs -n1 apk info --who-owns -q