#!/bin/bash

set -e

function delete() {

    echo "Deleting the following release:"
    echo $MATCHD_DEPLOYMENT_NAME
    echo ""

    helm delete "$MATCHD_DEPLOYMENT_NAME" || true

}
