# OpenEMR Data Export Tool

A tool that exports patient data from an OpenEMR database to Excel files.

## Docker Usage

### With Docker Network (OpenEMR running in Docker)

```bash
docker build -t openemr-export .
docker run --network openemr-network -v $(pwd)/exports:/app/exports openemr-export
```

### With Host Connection (OpenEMR running on host)

```bash
docker build -t openemr-export .
docker run -v $(pwd)/exports:/app/exports openemr-export --host host.docker.internal
```

### Specifying Database Connection Parameters

You can specify the database host using command-line arguments:

```bash
docker run --network openemr-network -v $(pwd)/exports:/app/exports openemr-export --host openemr_mysql_1
```

Or using environment variables:

```bash
docker run --network openemr-network -v $(pwd)/exports:/app/exports \
  -e DB_HOST=openemr_mysql_1 \
  openemr-export
```

## AWS S3 Export Script

The repository includes a script to export data to an AWS S3 bucket. You can run it with optional parameters for the database host and S3 bucket name:

```bash
./export_to_s3.sh [db_host] [s3_bucket]
```

Examples:

```bash
# Use default values (mysql host and openemr-data-exports bucket)
./export_to_s3.sh

# Specify database host only
./export_to_s3.sh openemr_mysql_1

# Specify both database host and S3 bucket
./export_to_s3.sh openemr_mysql_1 my-openemr-exports
```