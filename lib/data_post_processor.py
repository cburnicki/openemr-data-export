"""
Data post-processing utilities for OpenEMR exports.
Handles unit conversions from US/Imperial to metric system.
"""
import pandas as pd
import numpy as np


# Converter functions
def inches_to_cm(value):
    return value * 2.54

def lbs_to_kg(value):
    return value * 0.453592

def fahrenheit_to_celsius(value):
    return (value - 32) / 1.8


def apply_converter(df, column, converter_func):
    """
    Apply a converter function to a dataframe column if the column exists and values are not empty.
    
    Args:
        df (DataFrame): Input dataframe
        column (str): Column name to convert
        converter_func (function): Function to apply to the column values
        
    Returns:
        DataFrame: Dataframe with converted column
    """
    if column not in df.columns:
        return df
    
    result = df.copy()
    
    # Create mask for non-null numeric values
    mask = pd.notna(result[column])
    
    # Try to convert to numeric, ignoring errors
    numeric_values = pd.to_numeric(result.loc[mask, column], errors='coerce')
    numeric_mask = pd.notna(numeric_values)
    
    # Apply conversion only to valid numeric values
    if numeric_mask.any():
        # Use proper chained indexing to avoid SettingWithCopyWarning
        result.loc[mask.values & numeric_mask.values, column] = numeric_values[numeric_mask].apply(converter_func)
    
    return result


def convert_to_metric(dataframes):
    # Check if vitals table exists in the dataframes
    if 'vitals' in dataframes:
        # Create a copy to avoid modifying the original
        vitals_df = dataframes['vitals'].copy()
        
        # Apply each conversion
        vitals_df = apply_converter(vitals_df, 'height', inches_to_cm)
        vitals_df = apply_converter(vitals_df, 'weight', lbs_to_kg)
        vitals_df = apply_converter(vitals_df, 'temperature', fahrenheit_to_celsius)
        vitals_df = apply_converter(vitals_df, 'head_circ', inches_to_cm)
        vitals_df = apply_converter(vitals_df, 'waist_circ', inches_to_cm)
        
        # Update the dataframes dictionary with the modified copy
        dataframes['vitals'] = vitals_df
    
    # Return the modified dataframes dictionary
    return dataframes
