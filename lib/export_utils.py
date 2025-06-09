"""
SQL database connection and query functionality for OpenEMR data.
"""
import os
from datetime import datetime
import pandas as pd
from sqlalchemy import create_engine


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


def extract_data(engine, table_name, include_cols=None, drop_cols=None):
    """
    Extract data from a specified table with options to include or drop columns
    Always drops uuid and created_by columns if they exist
    
    Args:
        engine: SQLAlchemy engine for database connection
        table_name (str): Name of the table to extract data from
        include_cols (list, optional): List of columns to include. If None, all columns are included
        drop_cols (list, optional): List of columns to drop from the result
        
    Returns:
        DataFrame: Pandas DataFrame with the extracted data
    """
    # Build the SELECT clause
    if include_cols:
        columns = ", ".join(include_cols)
        select_clause = f"SELECT {columns}"
    else:
        select_clause = "SELECT *"
    
    # Build and execute the query
    query = f"{select_clause} FROM {table_name}"
    df = pd.read_sql(query, engine)
    
    # Always drop uuid and created_by columns
    standard_cols_to_drop = ['uuid', 'created_by', 'updated_by']
    df = drop_columns(df, standard_cols_to_drop)
    
    # Drop additional specified columns if any
    if drop_cols:
        df = drop_columns(df, drop_cols)
    
    print(f"Extracted {len(df)} records from {table_name}")

    return df


def drop_columns(df, columns_to_drop):
    """
    Remove specified columns from a pandas DataFrame if they exist
    Safely handles columns that don't exist in the DataFrame
    
    Args:
        df: pandas DataFrame to modify
        columns_to_drop: list of column names to remove
        
    Returns:
        DataFrame: Modified pandas DataFrame with columns removed
    """
    # Create a copy to avoid modifying the original DataFrame
    result_df = df.copy()
    
    # Filter to only include columns that exist in the DataFrame
    existing_columns = [col for col in columns_to_drop if col in result_df.columns]
    
    # Drop the existing columns all at once if any exist
    if existing_columns:
        result_df = result_df.drop(columns=existing_columns)
    
    return result_df


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
