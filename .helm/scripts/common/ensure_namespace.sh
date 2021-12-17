#!/bin/bash

set -e

function ensure_namespace() {

    echo ""
    echo "Making sure the namespace exists:"
    echo "$MATCHD_KUBE_NAMESPACE"
    echo ""

    kubectl describe namespace "$MATCHD_KUBE_NAMESPACE" || kubectl create namespace "$MATCHD_KUBE_NAMESPACE"

}
