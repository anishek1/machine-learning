# =============================================================================
# Play Store Data Cleaning Script
# Copy these cells into your Jupyter notebook for EDA
# =============================================================================

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/krishnaik06/playstore-Dataset/main/googleplaystore.csv")

# =============================================================================
# CELL 1: Initial Data Exploration
# =============================================================================
print("="*50)
print("INITIAL DATA EXPLORATION")
print("="*50)

print(f"\nShape: {df.shape}")
print(f"\nColumns: {df.columns.tolist()}")
print(f"\nData Types:\n{df.dtypes}")
print(f"\nMissing Values:\n{df.isnull().sum()}")
print(f"\nDuplicate Rows: {df.duplicated().sum()}")

# =============================================================================
# CELL 2: Remove Duplicates
# =============================================================================
print("\n" + "="*50)
print("REMOVING DUPLICATES")
print("="*50)

print(f"Before: {df.shape[0]} rows")
df.drop_duplicates(inplace=True)
print(f"After: {df.shape[0]} rows")

# =============================================================================
# CELL 3: Handle Corrupted/Misaligned Row (Row 10472)
# =============================================================================
# There's a known corrupted row in this dataset where data is shifted
print("\n" + "="*50)
print("CHECKING FOR CORRUPTED ROWS")
print("="*50)

# Find rows where 'Category' has invalid values (numeric ratings in wrong column)
corrupted_rows = df[~df['Category'].str.match(r'^[A-Z_]+$', na=False)]
print(f"Corrupted rows found: {len(corrupted_rows)}")
if len(corrupted_rows) > 0:
    print(corrupted_rows)
    df = df[df['Category'].str.match(r'^[A-Z_]+$', na=False)]
    print(f"Rows after cleanup: {df.shape[0]}")

# =============================================================================
# CELL 4: Clean 'Rating' Column
# =============================================================================
print("\n" + "="*50)
print("CLEANING 'Rating' COLUMN")
print("="*50)

# Convert to numeric and handle NaN
df['Rating'] = pd.to_numeric(df['Rating'], errors='coerce')
print(f"Missing ratings: {df['Rating'].isnull().sum()}")

# Fill missing ratings with median
median_rating = df['Rating'].median()
df['Rating'].fillna(median_rating, inplace=True)
print(f"Filled missing with median: {median_rating}")

# =============================================================================
# CELL 5: Clean 'Reviews' Column
# =============================================================================
print("\n" + "="*50)
print("CLEANING 'Reviews' COLUMN")
print("="*50)

df['Reviews'] = pd.to_numeric(df['Reviews'], errors='coerce')
df['Reviews'].fillna(0, inplace=True)
df['Reviews'] = df['Reviews'].astype(int)
print(f"Reviews dtype: {df['Reviews'].dtype}")

# =============================================================================
# CELL 6: Clean 'Size' Column
# =============================================================================
print("\n" + "="*50)
print("CLEANING 'Size' COLUMN")
print("="*50)

def clean_size(size):
    """Convert size to MB (float)"""
    if pd.isna(size) or size == 'Varies with device':
        return np.nan
    if 'M' in str(size):
        return float(size.replace('M', ''))
    if 'k' in str(size):
        return float(size.replace('k', '')) / 1024  # Convert KB to MB
    return np.nan

df['Size_MB'] = df['Size'].apply(clean_size)
print(f"Missing sizes: {df['Size_MB'].isnull().sum()}")

# Fill missing with median
median_size = df['Size_MB'].median()
df['Size_MB'].fillna(median_size, inplace=True)
print(f"Filled with median: {median_size:.2f} MB")

# =============================================================================
# CELL 7: Clean 'Installs' Column
# =============================================================================
print("\n" + "="*50)
print("CLEANING 'Installs' COLUMN")
print("="*50)

def clean_installs(installs):
    """Remove + and , from install count"""
    if pd.isna(installs):
        return np.nan
    return int(str(installs).replace(',', '').replace('+', ''))

df['Installs_Numeric'] = df['Installs'].apply(clean_installs)
print(f"Installs dtype: {df['Installs_Numeric'].dtype}")
print(f"Sample values: {df['Installs_Numeric'].head().tolist()}")

# =============================================================================
# CELL 8: Clean 'Price' Column
# =============================================================================
print("\n" + "="*50)
print("CLEANING 'Price' COLUMN")
print("="*50)

def clean_price(price):
    """Remove $ and convert to float"""
    if pd.isna(price):
        return 0.0
    price_str = str(price).replace('$', '').replace(',', '')
    try:
        return float(price_str)
    except:
        return 0.0

df['Price_USD'] = df['Price'].apply(clean_price)
print(f"Unique prices: {df['Price_USD'].nunique()}")
print(f"Price range: ${df['Price_USD'].min():.2f} - ${df['Price_USD'].max():.2f}")

# =============================================================================
# CELL 9: Clean 'Last Updated' Column
# =============================================================================
print("\n" + "="*50)
print("CLEANING 'Last Updated' COLUMN")
print("="*50)

df['Last_Updated_Date'] = pd.to_datetime(df['Last Updated'], format='%B %d, %Y', errors='coerce')
print(f"Date range: {df['Last_Updated_Date'].min()} to {df['Last_Updated_Date'].max()}")

# =============================================================================
# CELL 10: Clean 'Android Ver' Column
# =============================================================================
print("\n" + "="*50)
print("CLEANING 'Android Ver' COLUMN")
print("="*50)

def extract_android_version(ver):
    """Extract minimum Android version as float"""
    if pd.isna(ver) or ver == 'Varies with device':
        return np.nan
    try:
        # Extract first number (e.g., "4.0.3 and up" -> 4.0)
        ver_str = str(ver).split()[0]
        parts = ver_str.split('.')
        if len(parts) >= 2:
            return float(f"{parts[0]}.{parts[1]}")
        return float(parts[0])
    except:
        return np.nan

df['Min_Android_Ver'] = df['Android Ver'].apply(extract_android_version)
print(f"Missing Android versions: {df['Min_Android_Ver'].isnull().sum()}")

# Fill with mode (most common version)
mode_ver = df['Min_Android_Ver'].mode()[0]
df['Min_Android_Ver'].fillna(mode_ver, inplace=True)
print(f"Filled with mode: {mode_ver}")

# =============================================================================
# CELL 11: Handle Missing Values in 'Type' Column
# =============================================================================
print("\n" + "="*50)
print("CLEANING 'Type' COLUMN")
print("="*50)

print(f"Missing Type values: {df['Type'].isnull().sum()}")
# Most apps are Free, fill missing with 'Free'
df['Type'].fillna('Free', inplace=True)
print(f"Type distribution:\n{df['Type'].value_counts()}")

# =============================================================================
# CELL 12: Handle Missing 'Content Rating'
# =============================================================================
print("\n" + "="*50)
print("CLEANING 'Content Rating' COLUMN")
print("="*50)

print(f"Missing: {df['Content Rating'].isnull().sum()}")
df['Content Rating'].fillna('Everyone', inplace=True)
print(f"Values:\n{df['Content Rating'].value_counts()}")

# =============================================================================
# CELL 13: Final Cleaned DataFrame Summary
# =============================================================================
print("\n" + "="*50)
print("FINAL CLEANED DATAFRAME")
print("="*50)

# Select relevant cleaned columns
df_cleaned = df[[
    'App', 'Category', 'Rating', 'Reviews', 'Size_MB', 
    'Installs_Numeric', 'Type', 'Price_USD', 'Content Rating',
    'Genres', 'Last_Updated_Date', 'Min_Android_Ver'
]].copy()

# Rename for clarity
df_cleaned.columns = [
    'App', 'Category', 'Rating', 'Reviews', 'Size_MB',
    'Installs', 'Type', 'Price_USD', 'Content_Rating',
    'Genres', 'Last_Updated', 'Min_Android_Ver'
]

print(f"\nCleaned DataFrame Shape: {df_cleaned.shape}")
print(f"\nData Types:\n{df_cleaned.dtypes}")
print(f"\nMissing Values:\n{df_cleaned.isnull().sum()}")
print(f"\nFirst 5 rows:\n{df_cleaned.head()}")

# =============================================================================
# CELL 14: Summary Statistics
# =============================================================================
print("\n" + "="*50)
print("SUMMARY STATISTICS")
print("="*50)

print(df_cleaned.describe())

# Save cleaned data (optional)
# df_cleaned.to_csv('playstore_cleaned.csv', index=False)
# print("\nCleaned data saved to 'playstore_cleaned.csv'")
