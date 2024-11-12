#!/bin/bash

KEEP_COUNT=3
declare -a SERVICES=("audiora-app")

for SERVICE in "${SERVICES[@]}"; do
  echo "Deleting stale versions for service: $SERVICE, except the last $KEEP_COUNT versions"
  VERSIONS=$(gcloud app versions list --service "$SERVICE" --filter='traffic_split=0.00' --sort-by '~last_deployed_time' --format 'value(version.id)')
  
  COUNT=0
  for VERSION in $VERSIONS; do
    ((COUNT++))
    if [[ "$VERSION" == main-* && $COUNT -gt $KEEP_COUNT ]]; then
      echo "Deleting version $VERSION of the $SERVICE service."
      gcloud app versions delete "$VERSION" --service "$SERVICE" -q || true
    else
      echo "Keeping version $VERSION of the $SERVICE service."
    fi
  done
done
