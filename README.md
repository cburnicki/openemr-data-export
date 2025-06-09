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