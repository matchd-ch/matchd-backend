#!/bin/sh

set -eux

./setup.sh

exec "$@"