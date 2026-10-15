#!/usr/bin/env bash
set -euo pipefail

cd /usr/app/dbt

mkdir -p models macros tests snapshots target

generate_manifest() {
    echo "Generating dbt manifest..."

    dbt --no-partial-parse compile \
        --project-dir /usr/app/dbt \
        --profiles-dir /usr/app/dbt

    test -s /usr/app/dbt/target/manifest.json
    echo "Manifest generated successfully."
}

generate_manifest

while true; do
    inotifywait -r \
        -e modify,create,delete,move \
        models macros tests snapshots

    echo "dbt project changed - regenerating manifest..."
    generate_manifest
done