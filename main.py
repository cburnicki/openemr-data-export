#!/usr/bin/env python3
"""
OpenEMR Data Export Tool

This script exports patient data from an OpenEMR database to Excel files.
"""
import os
import time
import argparse
from lib.export_utils import extract_data, connect_to_db, export_to_excel


def main():
    """
    Main function to orchestrate the data export process.
    """
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='OpenEMR Data Export Tool')
    parser.add_argument('--host', default=os.environ.get('DB_HOST', 'localhost'),
                        help='Database host (default: value of DB_HOST env var or localhost)')
    parser.add_argument('--port', default=os.environ.get('DB_PORT', '3306'),
                        help='Database port (default: value of DB_PORT env var or 3306)')
    parser.add_argument('--user', default=os.environ.get('DB_USER', 'openemr'),
                        help='Database user (default: value of DB_USER env var or openemr)')
    parser.add_argument('--password', default=os.environ.get('DB_PASSWORD', 'openemr'),
                        help='Database password (default: value of DB_PASSWORD env var or openemr)')
    parser.add_argument('--database', default=os.environ.get('DB_NAME', 'openemr'),
                        help='Database name (default: value of DB_NAME env var or openemr)')
    
    args = parser.parse_args()
    
    print("Starting OpenEMR data export...")
    print(f"Connecting to database at {args.host}:{args.port}")
    
    # Start timing the export process
    start_time = time.time()
    
    try:
        # Connect to database
        host_with_port = f"{args.host}:{args.port}"
        engine = connect_to_db(
            host=host_with_port,
            user=args.user,
            password=args.password,
            database=args.database
        )
        
        # Organize dataframes for export
        dataframes = {
            'patient_data': extract_data(engine, 'patient_data', include_cols=[
                'pubpid', 
                'DOB', 
                'sex', 
                'sexual_orientation', 
                'gender_identity', 
                'status', 
                'street', 
                'deceased_date', 
                'deceased_reason'
            ]),
            'history_data': extract_data(engine, 'history_data'),
            'issues': extract_data(engine, 'lists'),
            'prescriptions': extract_data(engine, 'prescriptions'),
            'vitals': extract_data(engine, 'form_vitals'),
            'encounters': extract_data(engine, 'form_encounter'),
            'clinical_notes': extract_data(engine, 'form_clinical_notes'),
            'SOAP': extract_data(engine, 'form_soap'),
        }
        
        # Export to Excel
        output_file = export_to_excel(dataframes)
        
        # Calculate and log the export duration
        end_time = time.time()
        duration_seconds = end_time - start_time
        minutes, seconds = divmod(duration_seconds, 60)
        print(f"Data exported successfully to {output_file}")
        print(f"Export completed in {int(minutes)} minutes and {seconds:.2f} seconds")
        
    except Exception as e:
        # Log duration even if there was an error
        end_time = time.time()
        duration_seconds = end_time - start_time
        minutes, seconds = divmod(duration_seconds, 60)
        print(f"Error during export: {e}")
        print(f"Export failed after {int(minutes)} minutes and {seconds:.2f} seconds")


if __name__ == "__main__":
    main()
