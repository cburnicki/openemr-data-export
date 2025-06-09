#!/usr/bin/env python3
"""
OpenEMR Data Export Tool

This script exports patient data from an OpenEMR database to Excel files.
"""
from lib.export_utils import extract_data, connect_to_db, export_to_excel


def main():
    """
    Main function to orchestrate the data export process.
    """
    print("Starting OpenEMR data export...")
    
    try:
        # Connect to database
        engine = connect_to_db(
            host='localhost',
            user='openemr',
            password='openemr',
            database='openemr'
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
        print(f"Data exported successfully to {output_file}")
        
    except Exception as e:
        print(f"Error during export: {e}")


if __name__ == "__main__":
    main()
