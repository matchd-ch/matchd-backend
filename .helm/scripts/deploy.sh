#!/bin/bash

set -e

function deploy() {

  source .helm/scripts/helpers.sh
  source .helm/scripts/variables.sh

  if [ -z ${MATCHD_DEFAULT_REPLICAS+x} ]; then
    echo "In order to deploy, MATCHD_DEFAULT_REPLICAS must be set as a variable in the CI config."
    return 1
  fi

  if [ -z ${MATCHD_DEFAULT_STABLE_REPLICAS+x} ]; then
    echo "In order to deploy, MATCHD_DEFAULT_STABLE_REPLICAS must be set as a variable in the CI config."
    return 1
  fi

  REPLICAS="$MATCHD_DEFAULT_REPLICAS"
  STABLE_REPLICAS="$MATCHD_DEFAULT_STABLE_REPLICAS"

  eval NEW_REPLICAS=\$MATCHD_${MATCHD_ENV_SLUG}_REPLICAS
  eval NEW_STABLE_REPLICAS=\$MATCHD_${MATCHD_ENV_SLUG}_STABLE_REPLICAS

  if [ -n "$NEW_REPLICAS" ]; then
    REPLICAS="$NEW_REPLICAS"
  fi

  echo "REPLICAS: $REPLICAS"

  if [ -n "$NEW_STABLE_REPLICAS" ]; then
    STABLE_REPLICAS="$NEW_STABLE_REPLICAS"
  fi

  echo "STABLE_REPLICAS: $STABLE_REPLICAS"

  helm upgrade --install \
    --wait \
    --debug \
    --timeout 10m \
    \
    --set replicaCount="$REPLICAS" \
    --set stableReplicaCount="$STABLE_REPLICAS" \
    --set deployment.variants.regular.replicaCount="$REPLICAS" \
    --set deployment.variants.stable.replicaCount="$STABLE_REPLICAS" \
    \
    --version="$MATCHD_DEPLOYMENT_VERSION" \
    --namespace="$MATCHD_KUBE_NAMESPACE" \
    \
    --set version="$MATCHD_IMAGE_TAG" \
    --set name="$MATCHD_DEPLOYMENT_NAME" \
    --set environment="$MATCHD_ENVIRONMENT_SLUG" \
    \
    --set image.repository="$MATCHD_IMAGE_PULL_REGISTRY" \
    --set image.tag="$MATCHD_IMAGE_TAG" \
    --set image.pullPolicy="$MATCHD_IMAGE_PULL_POLICY" \
    --set image.secrets[0].name="$MATCHD_IMAGE_PULL_SECRET_NAME" \
    \
    --set ingress.hosts[0].host="$MATCHD_DOMAIN" \
    --set ingress.hosts[0].name="http" \
    --set ingress.hosts[0].port="$MATCHD_SERVICE_INTERNAL_PORT" \
    --set ingress.letsencrypt=$MATCHD_USE_LETSENCRYPT \
    --set ingress.monitoring=$MATCHD_MONITORING_ENABLED \
    --set ingress.tlsSecretName="$MATCHD_TLS_SECRET_NAME" \
    --set-string ingress.annotations."nginx\.ingress\.kubernetes\.io/from-to-www-redirect"="$MATCHD_WWW_REDIRECT" \
    \
    --set deployment.variants.stable.autoscaling.enabled="$MATCHD_STABLE_AUTOSCALING_ENABLED" \
    --set deployment.variants.regular.autoscaling.enabled="$MATCHD_REGULAR_AUTOSCALING_ENABLED" \
    \
    --set maildev.enabled=$MATCHD_MAILDEV_ENABLED \
    \
    --set elasticsearch.enabled=$MATCHD_ELASTICSEARCH_ENABLED \
    \
    "$@" \
    "$MATCHD_DEPLOYMENT_NAME" \
    .helm/chart/

}
