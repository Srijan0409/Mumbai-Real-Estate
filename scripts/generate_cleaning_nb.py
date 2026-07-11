import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

def create_and_execute_notebook():
    nb = nbformat.v4.new_notebook()
    
    cells = []
    
    # 1. Title
    cells.append(nbformat.v4.new_markdown_cell(
        "# Part 1: Data Cleaning - Real Estate Price Analysis (City-wise)\n"
        "This notebook loads the raw real estate transaction records, performs data auditing, "
        "applies standardizations, removes outliers, and saves the cleaned dataset for SQL loading and EDA."
    ))
    
    # 2. Imports
    cells.append(nbformat.v4.new_markdown_cell("## 1. Import Libraries and Load Raw Dataset"))
    cells.append(nbformat.v4.new_code_cell(
        "import pandas as pd\n"
        "import numpy as np\n\n"
        "# Load raw CSV dataset\n"
        "raw_df = pd.read_csv('../data/raw_data.csv')\n"
        "print('Raw dataset loaded successfully.')\n"
        "print(f'Initial shape: {raw_df.shape}')"
    ))
    
    # 3. Inspections
    cells.append(nbformat.v4.new_markdown_cell("## 2. Check Missing Values, Duplicates, and Data Types"))
    cells.append(nbformat.v4.new_code_cell(
        "# Check missing values\n"
        "print('--- Missing Values ---')\n"
        "print(raw_df.isnull().sum())\n\n"
        "# Check duplicates\n"
        "duplicates_count = raw_df.duplicated().sum()\n"
        "print(f'\\nNumber of duplicate rows: {duplicates_count}')\n\n"
        "# Check data types\n"
        "print('\\n--- Data Types ---')\n"
        "print(raw_df.dtypes)"
    ))
    
    # 4. Remove duplicates and nulls
    cells.append(nbformat.v4.new_markdown_cell("## 3. Drop Duplicates and Handle Missing Values"))
    cells.append(nbformat.v4.new_code_cell(
        "# Drop duplicate rows\n"
        "df = raw_df.drop_duplicates()\n"
        "print(f'Shape after dropping duplicates: {df.shape}')\n\n"
        "# Drop rows missing critical fields (price, area, locality, type, region)\n"
        "critical_cols = ['price', 'area', 'locality', 'type', 'region']\n"
        "df = df.dropna(subset=critical_cols)\n"
        "print(f'Shape after dropping critical missing values: {df.shape}')"
    ))
    
    # 5. Standardize text columns
    cells.append(nbformat.v4.new_markdown_cell("## 4. Standardize Text Columns (Trim & Proper Case)"))
    cells.append(nbformat.v4.new_code_cell(
        "# Standardize text columns (type, locality, region, status, age)\n"
        "text_cols = ['type', 'locality', 'region', 'status', 'age']\n"
        "for col in text_cols:\n"
        "    df[col] = df[col].astype(str).str.strip().str.title()\n\n"
        "print('Sample standardized text fields:')\n"
        "print(df[text_cols].head())"
    ))
    
    # 6. Convert price
    cells.append(nbformat.v4.new_markdown_cell("## 5. Convert Price to `price_in_lakhs`"))
    cells.append(nbformat.v4.new_code_cell(
        "# Convert price into a single unit called price_in_lakhs (1 Cr = 100 L)\n"
        "def convert_price_to_lakhs(row):\n"
        "    val = row['price']\n"
        "    unit = str(row['price_unit']).strip()\n"
        "    if unit == 'Cr':\n"
        "        return val * 100\n"
        "    elif unit == 'L':\n"
        "        return val\n"
        "    else:\n"
        "        return val\n\n"
        "df['price_in_lakhs'] = df.apply(convert_price_to_lakhs, axis=1)\n"
        "print(df[['price', 'price_unit', 'price_in_lakhs']].head())"
    ))
    
    # 7. Create price_per_sqft
    cells.append(nbformat.v4.new_markdown_cell("## 6. Calculate Derived Field: `price_per_sqft`"))
    cells.append(nbformat.v4.new_code_cell(
        "# Derived column: price_per_sqft = (price_in_lakhs * 100,000) / area\n"
        "df['price_per_sqft'] = (df['price_in_lakhs'] * 100000) / df['area']\n"
        "print(df[['area', 'price_in_lakhs', 'price_per_sqft']].head())"
    ))
    
    # 8. Outliers
    cells.append(nbformat.v4.new_markdown_cell("## 7. Outlier Removal for Area and Price per Sqft (IQR Method)"))
    cells.append(nbformat.v4.new_code_cell(
        "# Outlier removal using IQR method\n"
        "def remove_outliers_iqr(dataframe, column):\n"
        "    Q1 = dataframe[column].quantile(0.25)\n"
        "    Q3 = dataframe[column].quantile(0.75)\n"
        "    IQR = Q3 - Q1\n"
        "    lower_bound = Q1 - 1.5 * IQR\n"
        "    upper_bound = Q3 + 1.5 * IQR\n"
        "    return dataframe[(dataframe[column] >= lower_bound) & (dataframe[column] <= upper_bound)], lower_bound, upper_bound\n\n"
        "# Remove outliers from area\n"
        "df, lower_a, upper_a = remove_outliers_iqr(df, 'area')\n"
        "print(f'Area range after IQR: [{lower_a:.2f}, {upper_a:.2f}]')\n\n"
        "# Remove outliers from price_per_sqft\n"
        "df, lower_p, upper_p = remove_outliers_iqr(df, 'price_per_sqft')\n"
        "print(f'Price per sqft range after IQR: [{lower_p:.2f}, {upper_p:.2f}]')\n"
        "print(f'Shape after outlier removal: {df.shape}')"
    ))
    
    # 9. BHK range
    cells.append(nbformat.v4.new_markdown_cell("## 8. Filter BHK values (Keep only 1 to 10)"))
    cells.append(nbformat.v4.new_code_cell(
        "# Remove unrealistic BHK values (keep 1 to 10)\n"
        "initial_count = len(df)\n"
        "df = df[(df['bhk'] >= 1) & (df['bhk'] <= 10)]\n"
        "final_count = len(df)\n"
        "print(f'Rows before BHK filter: {initial_count}')\n"
        "print(f'Rows after BHK filter: {final_count}')\n"
        "print(f'Removed {initial_count - final_count} records with BHK out of range [1, 10].')"
    ))
    
    # 10. Print describe and shape
    cells.append(nbformat.v4.new_markdown_cell("## 9. Final Shape and Summary Statistics"))
    cells.append(nbformat.v4.new_code_cell(
        "print(f'Final Cleaned Dataset Shape: {df.shape}')\n"
        "print('\\n--- Summary Statistics ---')\n"
        "print(df.describe())"
    ))
    
    # 11. Export
    cells.append(nbformat.v4.new_markdown_cell("## 10. Export Cleaned Dataset to CSV"))
    cells.append(nbformat.v4.new_code_cell(
        "output_path = '../data/cleaned_data.csv'\n"
        "df.to_csv(output_path, index=False)\n"
        "print(f'Cleaned dataset exported to {output_path} successfully!')"
    ))
    
    nb['cells'] = cells
    
    os.makedirs('notebooks', exist_ok=True)
    nb_path = 'notebooks/01_data_cleaning.ipynb'
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"Jupyter Notebook skeleton written to {nb_path}")
    
    # Execute notebook
    print("Executing notebook cells...")
    ep = ExecutePreprocessor(timeout=600, kernel_name='python3')
    ep.preprocess(nb, {'metadata': {'path': 'notebooks'}})
    
    # Save executed notebook
    with open(nb_path, 'w', encoding='utf-8') as f:
        nbformat.write(nb, f)
    print(f"Executed Jupyter Notebook saved to {nb_path}")

if __name__ == '__main__':
    create_and_execute_notebook()
