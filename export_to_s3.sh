#!/bin/bash
# OpenEMR Data Export to S3 Script

# Get arguments or use defaults
DB_HOST=${1:-"mysql"}
S3_BUCKET=${2:-"openemr-data-exports"}
DOCKER_NETWORK="openemr-network"

# Run the export container
docker run --rm --network $DOCKER_NETWORK -v "$(pwd)/exports:/app/exports" openemr-export --host $DB_HOST
# Find the latest export file
EXPORT_FILE=$(ls -t exports/patient_data_export_*.xlsx 2>/dev/null | head -n 1)

# Delete existing files from S3
aws s3 rm "s3://$S3_BUCKET/" --recursive

# Upload the new export file to S3
aws s3 cp "$EXPORT_FILE" "s3://$S3_BUCKET/$(basename "$EXPORT_FILE")"

