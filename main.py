#!/usr/bin/env python3
"""
OpenEMR Data Export Tool

This script exports patient data from an OpenEMR database to Excel files.
"""
from lib.sql_reader import connect_to_db, extract_patient_data, extract_history_data
from lib.excel_export import export_to_excel


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
        
        # Extract patient data
        patient_df = extract_patient_data(engine)
        print(f"Extracted {len(patient_df)} patient records")
        
        # Extract history data
        history_df = extract_history_data(engine)
        print(f"Extracted {len(history_df)} history records")
        
        # Organize dataframes for export
        dataframes = {
            'patient_data': patient_df,
            'history_data': history_df
        }
        
        # Export to Excel
        output_file = export_to_excel(dataframes)
        print(f"Data exported successfully to {output_file}")
        
    except Exception as e:
        print(f"Error during export: {e}")


if __name__ == "__main__":
    main()
