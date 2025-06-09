"""
SQL database connection and query functionality for OpenEMR data.
"""
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


def drop_columns(df, columns_to_drop):
    """
    Remove specified columns from a pandas DataFrame if they exist
    
    Args:
        df: pandas DataFrame to modify
        columns_to_drop: list of column names to remove
        
    Returns:
        DataFrame: Modified pandas DataFrame with columns removed
    """
    # Create a copy to avoid modifying the original DataFrame
    result_df = df.copy()
    
    # Remove specified columns if they exist
    for col in columns_to_drop:
        if col in result_df.columns:
            result_df = result_df.drop(col, axis=1)
    
    return result_df


def extract_history_data(engine):
    """
    Extract history data from the database, excluding uuid and created_by fields
    
    Args:
        engine: SQLAlchemy engine for database connection
        
    Returns:
        DataFrame: Pandas DataFrame with history data
    """
    query = """
    SELECT * FROM history_data
    """
    
    # Get all columns
    df = pd.read_sql(query, engine)
    
    # Remove uuid and created_by columns
    columns_to_drop = ['uuid', 'created_by']
    df = drop_columns(df, columns_to_drop)
    
    return df
