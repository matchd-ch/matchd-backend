# Deployment

## Requirements

- Helm (v3)
- kubectl

---

## Usage

Use the deployment by sourcing the deploy script and then calling it.

```bash
source scripts/deploy.sh

deploy
```

All arguments given to the deploy script are expanded upon helm.

```bash
source scripts/deploy.sh

deploy \
  --set image.tag="v1.0.0" \
  --set image.pullPolicy="Always" \
```

---

## Variables

### Required

All required variables must be set to use the scripts and the Helm chart.

#### `MATCHD_KUBE_NAMESPACE`

The namespace to which the deployment should go.

#### `MATCHD_ENVIRONMENT_URL`

The URL on which the environment should run.

#### `MATCHD_ENVIRONMENT_SLUG`

A safe slug for the environment (eg. `production`)

#### `MATCHD_DEPLOYMENT_NAME`

A name for the deployment (eg. `matchd-frontend-production`).

#### `MATCHD_DEPLOYMENT_VERSION`

The version of the deployment by which Helm will track it.

#### `MATCHD_IMAGE_TAG`

The tag of the Docker image used by the deployment.

#### `MATCHD_IMAGE_PULL_USERNAME`

The username for the Docker pull secret.

#### `MATCHD_IMAGE_PULL_PASSWORD`

The password for the Docker pull secret.

#### `MATCHD_IMAGE_PULL_REGISTRY`

The registry URL for the Docker image registry.

### Optional

All optional variables have smart defaults and can be set if necessary.

`MATCHD_IMAGE_PULL_POLICY`

`MATCHD_IMAGE_PULL_SECRET_NAME`

`MATCHD_DEFAULT_REPLICAS`

`MATCHD_DEFAULT_STABLE_REPLICAS`

`MATCHD_PRODUCTION_REPLICAS`

`MATCHD_PRODUCTION_STABLE_REPLICAS`

`MATCHD_WWW_REDIRECT`

`MATCHD_MONITORING_ENABLED`

`MATCHD_USE_LETSENCRYPT`

`MATCHD_TLS_SECRET_NAME`

`MATCHD_STABLE_AUTOSCALING_ENABLED`

`MATCHD_REGULAR_AUTOSCALING_ENABLED`

`MATCHD_SERVICE_INTERNAL_PORT`

`MATCHD_MAILDEV_ENABLED`

`MATCHD_ELASTICSEARCH_ENABLED`

---

## Scripts

This directory includes various scripts for assisting with deployment processes.

### Common

#### `scripts/common/create_secret.sh`

Creates a Docker pull secret inside Kubernetes.

#### `scripts/common/ensure_namespace.sh`

Ensures that the wanted namespace exists by checking and creating if necessary.

#### `scripts/common/setup_chart.sh`

Sets up the chart (including dependencies).

### Core

#### `scripts/deploy.sh`

Deploys the application using the Helm chart.

#### `scripts/delete.sh`

Deletes a Helm deployment.

#### `scripts/helpers.sh`

Adds some helper functions (mostly for variables handling).
**`scripts/deploy.sh` sources this interally.**

#### `scripts/variables.sh`

Checks and sets up all variables for the deployments.
**`scripts/deploy.sh` sources this interally.**

### Test

#### `scripts/test/test.sh`

Uses predefined test variables and calls a dry-run deployment to test the chart.
