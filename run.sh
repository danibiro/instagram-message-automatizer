#!/bin/bash

if [ ! $# -eq 1 ]; then
    echo Usage: "$0" path_to_py_file
    exit 1
fi

if [ ! -d "$1" ]; then
    echo "$1" is not a valid directory
    exit 1
fi

if [ ! -e "$1/main.py" ]; then
    echo There is no file named main.py in the directory "$1"
    exit 1
fi

if [ ! -r "$1/user_config.yaml" ] || [ ! -f "$1/user_config.yaml" ]; then
    echo There is no file named user_config.yaml in the directory "$1" or it is not readable.
fi
if [ ! -r "$1/message_config.yaml" ] || [ ! -f "$1/message_config.yaml" ]; then
    echo There is no file named message_config.yaml in the directory "$1" or it is not readable.
fi
cd "$1" || exit
python_loc=$(whereis python3.10 | cut -d" " -f2)
$python_loc main.py
