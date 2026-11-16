#!/bin/sh
set -eu

cd "$(dirname "$0")"
newman run postman/Products.postman_collection.json \
  --env-var "base_url=${1:-http://127.0.0.1:5000}" --timeout-request 5000
