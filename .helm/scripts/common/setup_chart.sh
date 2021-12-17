#!/bin/bash

set -e

function setup_chart() {

  echo ""
  echo "Using deployment chart:"
  echo "$DEPLOYMENT_CHART"
  echo ""

  helm dependency update .helm/chart/

}
