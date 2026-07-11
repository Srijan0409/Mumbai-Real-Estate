# Real Estate Price Analysis (City-wise) - Mumbai Housing Market

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MySQL](https://img.shields.io/badge/MySQL-8.0+-orange.svg?style=for-the-badge&logo=mysql&logoColor=white)](https://www.mysql.com/)
[![Power BI](https://img.shields.io/badge/Power_BI-Portfolio-yellow.svg?style=for-the-badge&logo=powerbi&logoColor=white)](https://powerbi.microsoft.com/)
[![Pandas](https://img.shields.io/badge/Pandas-Data_Cleaning-darkgreen.svg?style=for-the-badge&logo=pandas&logoColor=white)](https://pandas.pydata.org/)

An end-to-end data analytics and business intelligence project establishing a reproducible pipeline to ingest, clean, store, and visualize real estate pricing trends across Mumbai's regional micro-markets.

---

## Table of Contents

- [1. Problem Statement](#1-problem-statement)
- [2. Dataset Overview](#2-dataset-overview)
- [3. Tech Stack](#3-tech-stack)
- [4. Project Architecture](#4-project-architecture)
- [5. Methodology & Pipeline](#5-methodology--pipeline)
  - [Phase 1: Data Cleaning (Python)](#phase-1-data-cleaning-python)
  - [Phase 2: Database Design & Ingestion (MySQL)](#phase-2-database-design--ingestion-mysql)
  - [Phase 3: Exploratory Data Analysis (Python)](#phase-3-exploratory-data-analysis-python)
  - [Phase 4: Dashboard Prep (Power BI)](#phase-4-dashboard-prep-power-bi)
- [6. Key Insights](#6-key-insights)
- [7. Interactive Dashboard Showcase](#7-interactive-dashboard-showcase)
- [8. How to Run Locally](#8-how-to-run-locally)
- [9. Future Improvements](#9-future-improvements)
- [10. Author / Contact](#10-author--contact)
- [11. Acknowledgements](#11-acknowledgements)

---

## 1. Problem Statement

The Mumbai Metropolitan Region (MMR) is one of the most dense, volatile, and expensive real estate markets globally. Real estate listing prices in Mumbai vary wildly based on micro-market location, developer branding, carpet area, configuration, and property status. For stakeholders such as individual buyers, real estate investors, property developers, and brokers, making decisions without structured data yields significant financial risk.

This project addresses this complexity by establishing an end-to-end data pipeline. By consolidating raw transaction listings, applying rigorous statistical outlier removal, storing structured records in a relational database, and presenting visual trends, this project extracts the core pricing drivers of the Mumbai housing market. 

Ultimately, this analysis allows buyers to detect undervalued units, enables investors to compare micro-market yields, assists developers in matching property dimensions to local demand, and empowers agents with empirical pricing data.

---

## 2. Dataset Overview

- **Source**: Mumbai House Prices raw transactions dataset (derived from `archive.zip`).
- **Raw Dimensions**: $76,038$ records across $9$ attributes.
- **Clean Dimensions**: $51,358$ records across $11$ attributes (after deduplication, range filtering, and statistical outlier removal).

### Data Dictionary

| Column Name | Description | Data Type | Source/Type |
| :--- | :--- | :--- | :--- |
| **bhk** | Number of bedrooms in the property (Range: 1 - 10) | Integer | Original |
| **type** | Property typology (e.g., Apartment, Villa, Penthouse) | Text / Categorical | Original |
| **locality** | Micro-market neighborhood name (e.g., Jogeshwari East) | Text / Categorical | Original |
| **area** | Carpet area of the property in square feet (sqft) | Integer | Original |
| **price** | Numeric listing price as reported | Float | Original |
| **price_unit** | Unit of the reported price ('Cr' = Crore, 'L' = Lakh) | Text / Categorical | Original |
| **region** | Broader municipal division (e.g., Thane West, Mira Road East) | Text / Categorical | Original |
| **status** | Listing readiness ('Ready To Move' vs 'Under Construction') | Text / Categorical | Original |
| **age** | Age classification of the building structure (New, Resale, etc.) | Text / Categorical | Original |
| **price_in_lakhs** | Standardized listing price converted entirely into Lakhs | Float | Derived (Engineered) |
| **price_per_sqft** | Standardized unit pricing: (price_in_lakhs * 100,000) / area | Float | Derived (Engineered) |

---

## 3. Tech Stack

| Tool / Technology | Purpose |
| :--- | :--- |
| **Python 3.9+** | Core programming language for data cleaning and ETL pipeline. |
| **Pandas / NumPy** | Data manipulation, type auditing, unit conversion, and statistical IQR profiling. |
| **Matplotlib / Seaborn** | Visual exploratory data analysis, plotting distributions, correlation heatmaps, and boxplots. |
| **MySQL / PyMySQL** | Relational database engine storing structured property records and running business queries. |
| **SQLAlchemy** | Python Object Relational Mapper (ORM) used to manage database connections and stream dataframes. |
| **Power BI** | Business Intelligence software used to build the interactive, client-facing dashboard. |
| **Jupyter Notebook** | Interactive development environment for prototyping pipelines and auditing steps. |

---

## 4. Project Architecture

```text
Real-Estate-Analysis/
  ├── data/
  │     ├── raw_data.csv            # Original raw housing records
  │     └── cleaned_data.csv        # Preprocessed, outlier-free transaction records
  ├── notebooks/
  │     ├── 01_data_cleaning.ipynb  # Interactive notebook outlining Phase 1 data cleaning
  │     └── 02_eda.ipynb            # Interactive notebook outlining Phase 3 exploratory plots
  ├── sql/
  │     ├── create_schema.sql       # Database schema and table definition DDL script
  │     └── analysis_queries.sql    # Core business queries answering key market questions
  ├── scripts/
  │     ├── generate_cleaning_nb.py # Python script to generate and run notebooks/01_data_cleaning.ipynb
  │     ├── generate_eda_nb.py      # Python script to generate and run notebooks/02_eda.ipynb
  │     └── load_to_mysql.py        # Database loading script executing SQL schema and appending records
  ├── dashboard/
  │     ├── power_bi_guide.md       # Complete setup instructions, color palettes, and visuals checklist
  │     └── dashboard_screenshot.png # High-fidelity dashboard design mockup preview
  ├── requirements.txt            # Python library dependencies file
  └── README.md                   # Detailed project documentation and portfolio entry
```

---

## 5. Methodology & Pipeline

### Phase 1: Data Cleaning (Python)
- **Actions Taken**:
  - Read `data/raw_data.csv` into a Pandas DataFrame.
  - Audited the data schema: identified $0$ null values but detected **$10,132$ duplicate records**, which were dropped.
  - Standardized string columns (`type`, `locality`, `region`, `status`, `age`) by trimming leading/trailing whitespace and converting them to proper Title Case to fix input inconsistency.
  - Converted mixed price denominations into a single numeric field: `price_in_lakhs`. Any record with `price_unit == 'Cr'` was scaled by multiplying the price by $100$.
  - Engineered the unit pricing metric: `price_per_sqft = (price_in_lakhs * 100,000) / area`.
  - Removed unrealistic configuration entries by filtering `bhk` to keep values only within the $[1, 10]$ range.
  - Applied the Interquartile Range (IQR) method to detect and filter size and pricing outliers.
- **Design Rationale**:
  - String cleaning is mandatory prior to SQL group-by aggregations to prevent split groups (e.g. "ready to move" vs "Ready To Move").
  - Outliers skew averages and charts. The IQR method was applied separately on `area` and `price_per_sqft` to ensure the final models analyze typical, representative properties.
- **Results**:
  - **Carpet Area bounds**: $[136.00, 1,907.00]$ sqft.
  - **Unit Price bounds**: $[646.77, 35,268.51]$ Rs/sqft.
  - **Final Output**: Saved $51,358$ cleaned records to `data/cleaned_data.csv`.

### Phase 2: Database Design & Ingestion (MySQL)
- **Actions Taken**:
  - Created [sql/create_schema.sql](sql/create_schema.sql) containing DDL statements to set up database `real_estate` and table `properties` with optimized columns (`DOUBLE` for metrics, explicit `VARCHAR` for strings).
  - Developed [scripts/load_to_mysql.py](scripts/load_to_mysql.py) utilizing PyMySQL and SQLAlchemy. The script programmatically ensures the schema is reset before appending the cleaned dataset.
  - Authored [sql/analysis_queries.sql](sql/analysis_queries.sql) containing 7 analytical queries.
- **Design Rationale**:
  - Using an ETL load script in Python guarantees database reproducibility across environments.
  - Custom column types (e.g. `VARCHAR(255)` for locality) prevent the database from defaulting to heavy, unindexed `TEXT` types, optimizing lookup performance.
- **Results**:
  - Successfully structured and loaded $51,358$ records into the `properties` table.
  - SQL queries cover:
    1. Average price per sqft by region (sorted descending).
    2. Top 10 most expensive localities by average price.
    3. Average price by BHK type.
    4. Count of listings by status per region.
    5. Average area and price for each property type.
    6. Regions with the highest number of listings.
    7. Price range (min/max/avg) grouped by BHK.

### Phase 3: Exploratory Data Analysis (Python)
- **Actions Taken**:
  - Developed [notebooks/02_eda.ipynb](notebooks/02_eda.ipynb) using Matplotlib and Seaborn.
  - Plotted a histogram visualizing property price distribution.
  - Generated boxplots mapping `price_per_sqft` variations across the top 10 regions by listing count.
  - Created a bar chart displaying average listing prices across BHK configurations.
  - Constructed a scatter plot relating carpet area and price, colored by BHK, and computed the Pearson correlation coefficient.
  - Plotted comparative bar charts of average price per sqft by typology, and countplots of listing status by region.
- **Design Rationale**:
  - Boxplots are chosen to visually verify the effectiveness of the IQR outlier removal and show the pricing spread.
  - Scatter plots with BHK coloring clarify how carpet area interacts with bedroom counts to drive total valuation.
- **Results**:
  - Discovered a strong linear correlation between area and price (**Pearson Correlation: 0.6552**).
  - Identified major regional pricing and supply disparities (detailed in the Key Insights section).

### Phase 4: Dashboard Prep (Power BI)
- **Actions Taken**:
  - Confirmed the clean structure of the final CSV for Power BI ingestion.
  - Wrote [dashboard/power_bi_guide.md](dashboard/power_bi_guide.md) to serve as a design framework.
  - Outlined specific visuals: KPI Cards, Clustered Bar Charts, Top 10 Localities Bar Chart, Area vs Price Scatter Chart, and Slicer filters.
- **Design Rationale**:
  - Establishing a design layout first ensures visual consistency, alignment, and a cohesive color palette (Midnight Navy `#1B263B` and Warm Gold `#E0A96D`).
- **Results**:
  - Generated a clean design mockup preview saved as `dashboard/dashboard_screenshot.png`.

---

## 6. Key Insights

- 📍 **High Regional Supply Concentration**: 
  The Mumbai residential housing supply is highly centralized. **Mira Road East** (7,742 listings) and **Thane West** (6,648 listings) dominate listing count, accounting for approximately **28%** of the entire inventory in the cleaned dataset. For developers, this indicates high competition and saturation in these sectors, while buyers can find a wide range of price options.
- 💰 **Steep BHK Price Progression**: 
  Property prices scale aggressively with bedroom configurations. While a **1 BHK** apartment averages **61.93 Lakhs**, a **2 BHK** averages **126.75 Lakhs** (a 104.7% premium), and a **3 BHK** averages **226.70 Lakhs** (a 78.9% increase over a 2 BHK). This steep progression represents the significant premium placed on square footage and space in high-density urban areas.
- 📐 **Strong Carpet Area Correlation**: 
  There is a strong positive correlation between property carpet area (sqft) and price (Lakhs), with a **Pearson Correlation Coefficient of 0.6552**. The scatter plot reveals that price variance widens heavily as the carpet area grows, demonstrating that luxury additions and specific premium building projects strongly influence pricing in larger properties.
- 🏢 **Vertical Density Premium**: 
  High-rise residential typologies command a significant unit valuation premium. **Penthouses** lead with an average of **15,151.52 Rs/sqft**, followed by standard **Apartments** at **13,550.79 Rs/sqft**. In contrast, horizontal **Villas** represent the lowest average unit rate at **5,359.39 Rs/sqft**, showing that high-density vertical living spaces in prime locations command premium pricing over outlying land plots.
- 🏗️ **Inventory Readiness Across Suburbs**: 
  Regional analysis reveals distinct developmental phases across neighborhoods. Mature residential suburbs like **Thane West** (4,152 Ready vs 2,496 Under Construction) and **Mira Road East** (4,554 Ready vs 3,188 Under Construction) possess substantial immediate-occupancy inventory. Conversely, premium emerging corridors like **Mulund West** (370 Ready vs 670 Under Construction) and **Chembur** (454 Ready vs 634 Under Construction) are dominated by active construction, pointing to high developer investment and future supply shifts.

---

## 7. Interactive Dashboard Showcase

The Power BI dashboard provides an interactive reporting interface for exploring properties. Users can use slicers (Region, BHK, Status, and Type) to instantly filter the dataset, causing all charts to cross-filter dynamically.

*Example mockup layout designed using the styling parameters:*

![Power BI Dashboard Mockup](dashboard/dashboard_screenshot.png)

---

## 8. How to Run Locally

### Prerequisites
- Python 3.9 or higher
- MySQL Server installed and running locally
- Power BI Desktop (optional, to view dashboard file)

### Step 1: Clone the Repository
Clone the project repository to your local system and navigate to the project directory:
```bash
git clone https://github.com/yourusername/Real-Estate-Analysis.git
cd Real-Estate-Analysis
```

### Step 2: Install Python Libraries
Install all required libraries, including pandas, matplotlib, seaborn, sqlalchemy, and pymysql from the requirements file:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Data Cleaning Pipeline
Execute the data cleaning notebook generator. This script creates, executes, and saves the cleaned dataset:
```bash
python scripts/generate_cleaning_nb.py
```
This generates the file `data/cleaned_data.csv` and compiles `notebooks/01_data_cleaning.ipynb` with code outputs.

### Step 4: Set Up MySQL Database & Ingest Data
Verify that your local MySQL server is running. Set your database credentials as environment variables if they differ from the defaults (Host: `127.0.0.1`, User: `root`, Password: ``, Port: `3306`), then execute the ingestion script:
```bash
# Windows PowerShell
$env:DB_PASSWORD="yourpassword"
python scripts/load_to_mysql.py

# Linux/macOS Bash
export DB_PASSWORD="yourpassword"
python scripts/load_to_mysql.py
```
This runs the DDL script in `sql/create_schema.sql` to structure the database and appends all cleaned records.

### Step 5: Run the EDA Pipeline
Generate the exploratory data analysis notebook to inspect all statistical charts:
```bash
python scripts/generate_eda_nb.py
```
This creates and runs `notebooks/02_eda.ipynb`.

### Step 6: Connect to Power BI
Launch Power BI Desktop and follow the configuration checklist in `dashboard/power_bi_guide.md` to import `data/cleaned_data.csv` and replicate the visual layout.

---

## 9. Future Improvements

- 🤖 **Predictive Pricing Model**: Integrate a Machine Learning regression module (e.g. Random Forest Regressor or XGBoost) to predict home values based on carpet area, region, BHK, and age.
- ☁️ **Cloud Database Deployment**: Move the MySQL storage instance to a cloud service (e.g. AWS RDS or GCP Cloud SQL) and configure a scheduled data ingestion task.
- 🗺️ **Geospatial Mapping Integration**: Integrate a Power BI Mapbox visual using geographic coordinates for each locality to create spatial heatmaps of price hotspots.
- 🕒 **Pipeline Automation**: Build an Apache Airflow DAG or GitHub Actions workflow to automate the cleaning, database updates, and Power BI refresh cycles.

---

## 10. Author / Contact

- **Name**: [Your Name Here]
- **GitHub**: [github.com/yourusername](https://github.com/yourusername)
- **LinkedIn**: [linkedin.com/in/yourprofile](https://linkedin.com/in/yourprofile)
- **Email**: [your.email@example.com]

---

## 11. Acknowledgements

- The raw Mumbai house transaction dataset was sourced from public real estate aggregators.
- Built as part of a vocational training program in Data Analytics, showcasing a complete Python-SQL-BI data pipeline.
