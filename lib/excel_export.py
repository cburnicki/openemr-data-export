"""
Excel export functionality for OpenEMR data.
"""
import os
import pandas as pd
from datetime import datetime


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
