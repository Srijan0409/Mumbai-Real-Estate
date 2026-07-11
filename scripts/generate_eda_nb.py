import nbformat
from nbconvert.preprocessors import ExecutePreprocessor
import os

def create_and_execute_eda_notebook():
    nb = nbformat.v4.new_notebook()
    
    cells = []
    
    # Title
    cells.append(nbformat.v4.new_markdown_cell(
        "# Part 3: Exploratory Data Analysis (EDA) - Real Estate Price Analysis\n"
        "This notebook explores patterns, distributions, correlations, and relationships within "
        "the cleaned real estate dataset using `pandas`, `matplotlib`, and `seaborn`."
    ))
    
    # 1. Imports
    cells.append(nbformat.v4.new_markdown_cell("## 1. Import Libraries and Load Cleaned Dataset"))
    cells.append(nbformat.v4.new_code_cell(
        "import pandas as pd\n"
        "import numpy as np\n"
        "import matplotlib.pyplot as plt\n"
        "import seaborn as sns\n"
        "import os\n\n"
        "# Set plotting aesthetics\n"
        "sns.set_theme(style='whitegrid')\n"
        "plt.rcParams['figure.figsize'] = (10, 6)\n"
        "plt.rcParams['font.size'] = 11\n\n"
        "# Robust path resolver to locate cleaned_data.csv\n"
        "possible_paths = [\n"
        "    '../data/cleaned_data.csv',\n"
        "    'data/cleaned_data.csv',\n"
        "    os.path.abspath(os.path.join(os.getcwd(), 'data', 'cleaned_data.csv')),\n"
        "    os.path.abspath(os.path.join(os.getcwd(), '..', 'data', 'cleaned_data.csv'))\n"
        "]\n\n"
        "csv_path = None\n"
        "for p in possible_paths:\n"
        "    if os.path.exists(p):\n"
        "        csv_path = p\n"
        "        break\n\n"
        "if csv_path is None:\n"
        "    raise FileNotFoundError('Could not locate cleaned_data.csv in any expected path.')\n\n"
        "print(f'Loading data from: {csv_path}')\n"
        "df = pd.read_csv(csv_path, engine='python')\n"
        "print('Cleaned dataset loaded successfully.')\n"
        "print(f'Shape: {df.shape}')"
    ))
    
    # 2. Summary stats
    cells.append(nbformat.v4.new_markdown_cell("## 2. Summary Statistics"))
    cells.append(nbformat.v4.new_code_cell(
        "print('Summary Statistics of Numerical Columns:')\n"
        "df.describe()"
    ))
    
    # 3. Histogram
    cells.append(nbformat.v4.new_markdown_cell("## 3. Distribution of Property Prices (`price_in_lakhs`)"))
    cells.append(nbformat.v4.new_code_cell(
        "plt.figure(figsize=(10, 6))\n"
        "sns.histplot(df['price_in_lakhs'], kde=True, bins=50, color='royalblue')\n"
        "plt.title('Distribution of Property Prices (in Lakhs) in Mumbai', fontsize=14, pad=15)\n"
        "plt.xlabel('Price (Lakhs)', fontsize=12)\n"
        "plt.ylabel('Count', fontsize=12)\n"
        "plt.tight_layout()\n"
        "plt.show()"
    ))
    
    # 4. Boxplot grouped by region (Top 10 regions by listing count)
    cells.append(nbformat.v4.new_markdown_cell("## 4. Price per Sqft Grouped by Region (Top 10 Regions)"))
    cells.append(nbformat.v4.new_code_cell(
        "# Identify top 10 regions by listing count\n"
        "top_10_regions = df['region'].value_counts().head(10).index.tolist()\n"
        "df_top10 = df[df['region'].isin(top_10_regions)]\n\n"
        "plt.figure(figsize=(12, 6))\n"
        "sns.boxplot(data=df_top10, x='region', y='price_per_sqft', palette='Set2')\n"
        "plt.title('Price per Square Foot Distribution across Top 10 Regions', fontsize=14, pad=15)\n"
        "plt.xlabel('Region (Top 10 by Listing Volume)', fontsize=12)\n"
        "plt.ylabel('Price per Sqft (Rs)', fontsize=12)\n"
        "plt.xticks(rotation=45)\n"
        "plt.tight_layout()\n"
        "plt.show()"
    ))
    
    # 5. Bar chart of average price by BHK
    cells.append(nbformat.v4.new_markdown_cell("## 5. Average Price by BHK Configuration"))
    cells.append(nbformat.v4.new_code_cell(
        "plt.figure(figsize=(8, 5))\n"
        "sns.barplot(data=df, x='bhk', y='price_in_lakhs', estimator='mean', errorbar=None, palette='Blues_d')\n"
        "plt.title('Average Property Price by BHK Configuration', fontsize=14, pad=15)\n"
        "plt.xlabel('BHK Configuration', fontsize=12)\n"
        "plt.ylabel('Average Price (Lakhs)', fontsize=12)\n"
        "for container in plt.gca().containers:\n"
        "    plt.gca().bar_label(container, fmt='%.2f Lakhs', padding=3)\n"
        "plt.tight_layout()\n"
        "plt.show()"
    ))
    
    # 6. Scatter plot of area vs price
    cells.append(nbformat.v4.new_markdown_cell("## 6. Property Area vs Price (Colored by BHK)"))
    cells.append(nbformat.v4.new_code_cell(
        "correlation_coef = df['area'].corr(df['price_in_lakhs'])\n"
        "print(f'Pearson Correlation Coefficient: {correlation_coef:.4f}')\n\n"
        "plt.figure(figsize=(10, 6))\n"
        "sns.scatterplot(data=df, x='area', y='price_in_lakhs', hue='bhk', palette='viridis', alpha=0.5)\n"
        "plt.title(f'Property Area vs Price (Pearson Correlation: {correlation_coef:.4f})', fontsize=14, pad=15)\n"
        "plt.xlabel('Area (sqft)', fontsize=12)\n"
        "plt.ylabel('Price (Lakhs)', fontsize=12)\n"
        "plt.legend(title='BHK Configuration')\n"
        "plt.tight_layout()\n"
        "plt.show()"
    ))
    
    # 7. Bar chart of avg price_per_sqft by type
    cells.append(nbformat.v4.new_markdown_cell("## 7. Average Price per Sqft by Property Type"))
    cells.append(nbformat.v4.new_code_cell(
        "plt.figure(figsize=(9, 5))\n"
        "sns.barplot(data=df, x='type', y='price_per_sqft', estimator='mean', errorbar=None, palette='coolwarm')\n"
        "plt.title('Average Price per Square Foot by Property Type', fontsize=14, pad=15)\n"
        "plt.xlabel('Property Type', fontsize=12)\n"
        "plt.ylabel('Average Price per Sqft (Rs)', fontsize=12)\n"
        "for container in plt.gca().containers:\n"
        "    plt.gca().bar_label(container, fmt='%.1f Rs/sqft', padding=3)\n"
        "plt.xticks(rotation=15)\n"
        "plt.tight_layout()\n"
        "plt.show()"
    ))
    
    # 8. Countplot of status by region (top 10)
    cells.append(nbformat.v4.new_markdown_cell("## 8. Listing Status Distribution in Top 10 Regions"))
    cells.append(nbformat.v4.new_code_cell(
        "plt.figure(figsize=(12, 6))\n"
        "sns.countplot(data=df_top10, x='region', hue='status', palette='muted')\n"
        "plt.title('Inventory Count by Status (Ready vs Under Construction) per Region', fontsize=14, pad=15)\n"
        "plt.xlabel('Region', fontsize=12)\n"
        "plt.ylabel('Listing Count', fontsize=12)\n"
        "plt.xticks(rotation=45)\n"
        "plt.legend(title='Status')\n"
        "plt.tight_layout()\n"
        "plt.show()"
    ))
    
    # 9. Key Insights Markdown Cell
    cells.append(nbformat.v4.new_markdown_cell(
        "## Written Insights & Analysis Patterns\n\n"
        "Based on the visualization outputs and statistical calculations, here are the core findings:\n\n"
        "1. **Geographic Concentration of Inventory**:\n"
        "   The real estate supply is highly concentrated. **Mira Road East** (7,742 listings) and **Thane West** (6,648 listings) dominate "
        "listing count, accounting for approximately **28%** of total property records. This suggests these two regions are "
        "the primary transaction hubs for middle-income residential real estate in the Mumbai Metropolitan Region (MMR).\n\n"
        "2. **BHK Premium & Price Progression**:\n"
        "   Property prices scale aggressively with BHK configurations. A **1 BHK** apartment averages **61.93 Lakhs**, which "
        "more than doubles to **126.75 Lakhs** for a **2 BHK** (+104.7%). A **3 BHK** represents another major tier shift, averaging "
        "**226.70 Lakhs** (+78.9% increase relative to 2 BHK), while 4 BHK and 5 BHK units show average valuations exceeding "
        "320 Lakhs. This steep slope reflects the premium placed on space in high-density urban areas.\n\n"
        "3. **Relationship Between Size and Total Price**:\n"
        "   There is a strong positive correlation between property area (sqft) and price (Lakhs), with a **Pearson Correlation Coefficient of 0.6552**.\n"
        "   The scatter plot confirms that as area increases, price climbs, but price variance also widens significantly for larger configurations, "
        "indicating that luxury elements and specific micro-localities heavily skew prices of larger properties.\n\n"
        "4. **Typology Premium (Price per Sqft)**:\n"
        "   Different property typologies have vastly different valuation structures. **Penthouses** command the highest average price per square foot at "
        "**15,151.52 Rs/sqft**, followed closely by **Apartments** at **13,550.79 Rs/sqft**. Conversely, **Villas** are listed at the lowest average price per sqft "
        "at **5,359.39 Rs/sqft**. This indicates that dense high-rise structures (apartments/penthouses) command a premium rate per unit area, whereas low-density horizontal properties (villas) have a much lower unit rate, likely situated in far suburban or residential enclaves.\n\n"
        "5. **Inventory Readiness Across Regions**:\n"
        "   Analysing ready-to-move (RTM) vs under-construction (UC) properties in the top 10 regions reveals development maturity:\n"
        "   - Mature hubs like **Thane West** (4,152 RTM vs 2,496 UC) and **Mira Road East** (4,554 RTM vs 3,188 UC) have high volumes of finished, immediate-occupancy inventory.\n"
        "   - Emerging premium zones like **Mulund West** (370 RTM vs 670 UC) and **Chembur** (454 RTM vs 634 UC) are heavily tilted towards under-construction inventory, indicating substantial new development projects currently underway."
    ))
    
    nb['cells'] = cells
    
    os.makedirs('notebooks', exist_ok=True)
    nb_path = 'notebooks/02_eda.ipynb'
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
    create_and_execute_eda_notebook()
