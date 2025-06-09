# OpenEMR Data Export Tool

A Python utility for exporting OpenEMR patient data to Excel files for analysis.

## Features

- Connects to OpenEMR MariaDB database
- Extracts patient data into pandas DataFrames
- Exports data to Excel with separate sheets for different tables
- Supports one-to-many relationships in data structure
- Extensible design for adding more data exports

## Requirements

- Python 3.13 (as specified in .python-version)
- MariaDB/MySQL with OpenEMR database
- Dependencies managed with uv

## Installation

1. Clone this repository
2. Install dependencies using uv:

```bash
uv pip install -e .
```

## Usage

1. Update the database connection parameters in `main.py` with your OpenEMR database credentials
2. Run the script:

```bash
python main.py
```

The script will:
1. Connect to the specified OpenEMR database
2. Extract patient data from the `patient_data` table
3. Export the data to an Excel file in the `exports` directory
4. The filename includes a timestamp for versioning

## Customization

To export additional tables or modify the exported columns:

1. Update the SQL query in the `extract_patient_data()` function
2. Add new extraction functions for additional tables
3. Add the resulting DataFrames to the `dataframes` dictionary in the `main()` function

## License

MIT