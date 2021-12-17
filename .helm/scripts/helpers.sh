#!/bin/bash

set -e

function check_variable() {
    NAME="$1"
    SECURE="$2"
    MESSAGE="$3"

    VALUE=$(eval echo "\$$NAME")

    if [ -z "$MESSAGE" ]; then
        MESSAGE="In order to deploy, the $1 variable must be set as a variable in the CI config."
    fi

    echo "Checking variable $NAME"

    if [ -z "$VALUE" ]; then
        echo $MESSAGE
        return 1
    fi

    dump_variable "$NAME" "$SECURE"
}

function variable_default() {
    NAME="$1"
    DEFAULT_VALUE="$2"
    SECURE="$3"

    VALUE=$(eval echo "\$$NAME")

    if [ -z "$VALUE" ]; then
        echo "$NAME is not explicitly set, providing default value"
        export "$NAME"="$DEFAULT_VALUE"
    fi

    dump_variable "$NAME" "$SECURE"
}

function dump_variable() {
    NAME="$1"
    VALUE=$(eval echo "\$$NAME")
    SECURE="$2"

    if [ -z "$SECURE" ]; then
        echo "$NAME is set to $VALUE"
    else
        echo "$NAME is set to ${VALUE:1:5}..."
    fi
}
