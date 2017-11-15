#!/bin/sh

PATH=/usr/local/bin:/usr/bin:/usr/local/sbin:/usr/sbin

if (("$#" != 1)); then
    echo "Usage: ./find_class.sh <class name>."
    exit 1
fi

for file in $(find . -type f -name *.jar)
do
    printf "File: '%s'\n" $file
    res=$(jar -tf $file | grep "$1")
   	if [[ $res ]]; then
       printf "File: '%s'\n" $file
    fi
done