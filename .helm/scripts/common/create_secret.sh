#!/bin/bash

set -e

function create_secret() {

  echo ""
  echo "Creating the docker pull secret:"
  echo "$MATCHD_IMAGE_PULL_SECRET_NAME"
  echo ""

  if [ -z "$MATCHD_IMAGE_PULL_USERNAME" ] || [ -z "$MATCHD_IMAGE_PULL_PASSWORD" ]; then
    echo "MATCHD_IMAGE_PULL_USERNAME or MATCHD_IMAGE_PULL_PASSWORD not present"
    exit 1
  fi

  kubectl create secret -n "$MATCHD_KUBE_NAMESPACE" \
    docker-registry $MATCHD_IMAGE_PULL_SECRET_NAME \
    --docker-server="$MATCHD_IMAGE_PULL_REGISTRY" \
    --docker-username="${MATCHD_IMAGE_PULL_USERNAME}" \
    --docker-password="${MATCHD_IMAGE_PULL_PASSWORD}" \
    -o yaml --dry-run | kubectl replace -n "$MATCHD_KUBE_NAMESPACE" --force -f -

}
