import pandas as pd
import pymysql
from sqlalchemy import create_engine
import os
from datetime import datetime


def connect_to_db(host='localhost', user='openemr', password='openemr', database='openemr'):
    """
    Connect to the MariaDB database
    
    Args:
        host (str): Database host
        user (str): Database user
        password (str): Database password
        database (str): Database name
        
    Returns:
        engine: SQLAlchemy engine for database connection
    """
    connection_string = f"mysql+pymysql://{user}:{password}@{host}/{database}"
    engine = create_engine(connection_string)
    return engine


def extract_patient_data(engine):
    """
    Extract patient data from the database
    
    Args:
        engine: SQLAlchemy engine for database connection
        
    Returns:
        DataFrame: Pandas DataFrame with patient data
    """
    query = """
    SELECT 
        pubpid, 
        DOB, 
        sex, 
        sexual_orientation, 
        gender_identity, 
        status, 
        street, 
        deceased_date, 
        deceased_reason
    FROM 
        patient_data
    """
    
    df = pd.read_sql(query, engine)
    return df


def export_to_excel(dataframes, output_dir='exports'):
    """
    Export dataframes to Excel file
    
    Args:
        dataframes (dict): Dictionary of dataframes with sheet names as keys
        output_dir (str): Directory to save the Excel file
        
    Returns:
        str: Path to the saved Excel file
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"patient_data_export_{timestamp}.xlsx"
    filepath = os.path.join(output_dir, filename)
    
    # Create Excel writer
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        # Write each dataframe to a separate sheet
        for sheet_name, df in dataframes.items():
            df.to_excel(writer, sheet_name=sheet_name, index=False)
    
    return filepath


def main():
    print("Starting OpenEMR data export...")
    
    try:
        # Connect to database
        # Replace these with your actual database credentials
        engine = connect_to_db(
            host='localhost',
            user='openemr',
            password='openemr',
            database='openemr'
        )
        
        # Extract patient data
        patient_df = extract_patient_data(engine)
        print(f"Extracted {len(patient_df)} patient records")
        
        # Organize dataframes for export
        dataframes = {
            'patient_data': patient_df
        }
        
        # Export to Excel
        output_file = export_to_excel(dataframes)
        print(f"Data exported successfully to {output_file}")
        
    except Exception as e:
        print(f"Error during export: {e}")


if __name__ == "__main__":
    main()
