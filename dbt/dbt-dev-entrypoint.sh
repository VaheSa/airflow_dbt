#!/usr/bin/env bash
set -u
cd /usr/app/dbt
echo "Generating initial dbt manifest..."
dbt parse || true
echo "Watching dbt project for changes..."
while true; do
  inotifywait -r -e modify,create,delete,move --exclude 'target|logs|dbt_packages|\.git' models macros tests snapshots dbt_project.yml 2>/dev/null || sleep 2
  echo "dbt project changed - regenerating manifest..."
  dbt parse || true
done
