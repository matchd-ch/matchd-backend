#!/bin/bash

SCRIPT=$(readlink -f $0)
SCRIPTPATH=$(dirname $SCRIPT)

source $SCRIPTPATH/../helpers.sh
source $SCRIPTPATH/test_variables.sh
source $SCRIPTPATH/../variables.sh
source $SCRIPTPATH/../deploy.sh

deploy \
  --dry-run \
  --debug
