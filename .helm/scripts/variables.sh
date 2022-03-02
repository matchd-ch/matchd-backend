#!/bin/bash

set -e

## CHECK MANDATORY VARIABLES

check_variable "MATCHD_KUBE_NAMESPACE"
check_variable "MATCHD_ENVIRONMENT_URL"
check_variable "MATCHD_ENVIRONMENT_SLUG"
check_variable "MATCHD_DEPLOYMENT_NAME"
check_variable "MATCHD_DEPLOYMENT_VERSION"
check_variable "MATCHD_IMAGE_TAG"
check_variable "MATCHD_IMAGE_PULL_USERNAME"
check_variable "MATCHD_IMAGE_PULL_PASSWORD"
check_variable "MATCHD_IMAGE_PULL_REGISTRY"

## IMAGES

variable_default "MATCHD_IMAGE_PULL_POLICY" "IfNotPresent"
variable_default "MATCHD_IMAGE_PULL_SECRET_NAME" "docker-registry"

### ENV SLUG

MATCHD_ENV_SLUG=$(echo ${MATCHD_ENVIRONMENT_SLUG//-/_} | tr '[:lower:]' '[:upper:]')
dump_variable "MATCHD_ENV_SLUG"
export MATCHD_ENV_SLUG

## Replicas

variable_default "MATCHD_DEFAULT_REPLICAS" "1"
variable_default "MATCHD_DEFAULT_STABLE_REPLICAS" "0"
variable_default "MATCHD_PRODUCTION_REPLICAS" "2"
variable_default "MATCHD_PRODUCTION_STABLE_REPLICAS" "0"

## DOMAIN

MATCHD_DOMAIN="${MATCHD_ENVIRONMENT_URL#*//}"
dump_variable "MATCHD_DOMAIN"
export MATCHD_DOMAIN

## LB

variable_default "MATCHD_WWW_REDIRECT" "false"
variable_default "MATCHD_MONITORING_ENABLED" "false"

## TLS

variable_default "MATCHD_TLS_SECRET_NAME" "$MATCHD_ENVIRONMENT_SLUG-tls"

## Autoscaling

variable_default "MATCHD_STABLE_AUTOSCALING_ENABLED" "true"
variable_default "MATCHD_REGULAR_AUTOSCALING_ENABLED" "true"

## Network

variable_default "MATCHD_SERVICE_INTERNAL_PORT" 80

## Maildev

variable_default "MATCHD_MAILDEV_ENABLED" "true"

## Elasticsearch

variable_default "MATCHD_ELASTICSEARCH_ENABLED" "true"