# Power BI Dashboard Implementation Guide

This guide details the steps to build a portfolio-quality Power BI dashboard using the cleaned dataset: `data/cleaned_data.csv`.

---

## 1. Data Source Confirmation

- **File Path**: `data/cleaned_data.csv` (Shape: 51,358 rows, 11 columns)
- **Data Load**: Import directly using `Get Data` -> `Text/CSV`.
- **Field Mappings & Formatting**:
  - `bhk`: Whole Number (Default Summary: Do Not Summarize)
  - `area`: Whole Number (Default Summary: Average)
  - `price_in_lakhs`: Decimal Number (Format: Currency/Decimal, Default Summary: Average)
  - `price_per_sqft`: Decimal Number (Format: Currency/Decimal, Default Summary: Average)
  - `type`, `locality`, `region`, `status`, `age`: Text / Categorical

---

## 2. Design System & Aesthetics (Midnight Slate & Warm Gold)

To elevate this dashboard to portfolio-quality, apply the following design guidelines:

- **Theme Palette**:
  - 🎨 **Canvas Background**: `#F4F6F9` (Very light cool gray)
  - 🎨 **Card/Visual Containers**: `#FFFFFF` (Pure white with 8-10px border radius and 5% opacity drop-shadow)
  - 🎨 **Primary Data Series / Text**: `#1B263B` (Deep Navy)
  - 🎨 **Secondary Accent / Gridlines**: `#E0A96D` (Warm Gold for highlights) or `#415A77` (Steel Blue)
- **Typography**:
  - Title/Headers: **Segoe UI Semibold** (Size 20-24, Deep Navy `#1B263B`)
  - Subheaders/Axis Titles: **Segoe UI** (Size 11-12, Muted Steel `#415A77`)
  - Data Labels: **Segoe UI Bold** (Size 9-10, Deep Navy `#1B263B`)

---

## 3. Visuals Configuration

Set up a single-page canvas with a top-bar banner for slicers, a middle row for KPIs, and a bottom section divided into grids for detailed charts.

### A. Top Banner: Slicers
Arrange these horizontally at the top of the canvas for interactive filtering:
1. **Region Slicer**: Dropdown or Tile visual (`region`)
2. **BHK Slicer**: Horizontal tile buttons (`bhk` values 1 to 5)
3. **Property Status Slicer**: Radio list (`status`: Ready To Move vs Under Construction)
4. **Property Type Slicer**: Dropdown list (`type`)

---

### B. KPI Cards (Row 1)
Use the **Multi-row card** or individual **Card** visuals placed side-by-side:

1. **Average Property Price**
   - **Field**: `price_in_lakhs` (Aggregate: **Average**)
   - **Label**: `Avg Price`
   - **Display Unit**: None (Suffix: " Lakhs" or formatted as currency e.g., ₹121.21 L)
2. **Average Price per Sqft**
   - **Field**: `price_per_sqft` (Aggregate: **Average**)
   - **Label**: `Avg Price/Sqft`
   - **Format**: ₹#,##0 (e.g., ₹13,481/sqft)
3. **Total Active Listings**
   - **Field**: `locality` or any field (Aggregate: **Count**)
   - **Label**: `Total Listings`
   - **Format**: #,##0 (e.g., 51,358)
4. **Most Expensive Region**
   - **Calculated DAX Measure**:
     ```dax
     Most Expensive Region = 
     TOPN(
         1, 
         VALUES(properties[region]), 
         CALCULATE(AVERAGE(properties[price_in_lakhs]))
     )
     ```
   - **Label**: `Premium Region`

---

### C. Analytical Visuals (Row 2 & 3 Grid)

#### 1. Average Price per Sqft by Region (Clustered Bar Chart)
*Position: Left-Middle Grid*
- **Axis (Y-axis)**: `region` (Sorted by average price_per_sqft descending)
- **Values (X-axis)**: `price_per_sqft` (Aggregate: **Average**)
- **Visual Title**: `Average Price per Sqft by Geographic Region`
- **Formatting**: Enable data labels, disable gridlines on X-axis, color bars using Primary Navy (`#1B263B`).

#### 2. Top 10 Localities by Average Price (Horizontal Bar Chart)
*Position: Right-Middle Grid*
- **Axis (Y-axis)**: `locality`
- **Values (X-axis)**: `price_in_lakhs` (Aggregate: **Average**)
- **Top N Filter**: Apply a Visual-level filter on `locality` -> "Top 10" by `price_in_lakhs` (Average).
- **Visual Title**: `Top 10 Most Expensive Localities (Average Price)`
- **Formatting**: Color bars using Warm Gold (`#E0A96D`) to highlight premium zones.

#### 3. Property Size vs Price (Scatter Plot)
*Position: Bottom Span*
- **X-axis**: `area` (Property size in sqft)
- **Y-axis**: `price_in_lakhs` (Total price)
- **Legend (Hue)**: `bhk` (Categorized)
- **Tooltip**: `locality`, `region`, `price_per_sqft`
- **Visual Title**: `Property Area (Sqft) vs. Total Price (Lakhs) by BHK Configuration`
- **Formatting**: Set bubble opacity to 60-70% to handle density overlap. Add a linear trendline.

---

## 4. Professional Formatting Checklist

- [ ] **Visual Boundaries**: Use rounded card containers with light grey borders (`1px`, `#E4E7EB`) and padding (`15px`) around each chart.
- [ ] **Title Standardization**: Titles must be concise, left-aligned, and structured: `[Metric] by [Dimensions]`.
- [ ] **Interaction Behavior**: Ensure cross-filtering is turned ON so selecting a region updates the Top 10 Localities and the Scatter Plot.
- [ ] **Number Formatting**: Always format financial fields to display currency indicators (₹) and proper decimal precision (1 or 2 decimals).
