#!/bin/bash

set -e

export MATCHD_KUBE_NAMESPACE="matchd-frontend-production"
export MATCHD_ENVIRONMENT_URL="matchd.ch"
export MATCHD_ENVIRONMENT_SLUG="production"
export MATCHD_DEPLOYMENT_NAME="matchd-frontend-production"
export MATCHD_DEPLOYMENT_VERSION="v1.0.0-a4hsd3"
export MATCHD_IMAGE_TAG="v1.0.0"
export MATCHD_IMAGE_PULL_USERNAME="image-pull-username"
export MATCHD_IMAGE_PULL_PASSWORD="image-pull-password"
export MATCHD_IMAGE_PULL_REGISTRY="image-pull-registry"
