# ==========================================
# Project: Enterprise Sales Intelligence & Genie Agent
# Description: Creating Gold layer tables in Unity Catalog with rich metadata comments, time-series data, and foreign keys
# ==========================================

import pandas as pd

# ------------------------------------------
# Step 1: Initialize Catalog and Schema
# ------------------------------------------
print("⏳ Creating catalog and schema in Unity Catalog...")
spark.sql("CREATE CATALOG IF NOT EXISTS enterprise_catalog;")
spark.sql("CREATE DATABASE IF NOT EXISTS enterprise_catalog.gold_layer;")
print("✅ Catalog and schema ready successfully!")


# ------------------------------------------
# Step 2: Create Fact Table with Time-Series Data (Granular Monthly Sales)
# ------------------------------------------
print("⏳ Creating the main Gold Fact Table with time-series data...")

sales_data = [
    # January 2026
    ("EMEA", "Software", "Direct", 1200000, 450000, "Alice", "2026-01-15", 320),
    ("EMEA", "Hardware", "Partner", 850000, 310000, "Alice", "2026-01-15", 150),
    ("AMER", "Software", "Direct", 3400000, 1200000, "Bob", "2026-01-15", 890),
    ("AMER", "Cloud", "Partner", 2100000, 950000, "Bob", "2026-01-15", 410),
    ("APAC", "Software", "Direct", 850000, 290000, "Charlie", "2026-01-15", 210),
    ("APAC", "Cloud", "Partner", 1100000, 480000, "Charlie", "2026-01-15", 300),
    
    # February 2026
    ("EMEA", "Software", "Direct", 1450000, 520000, "Alice", "2026-02-15", 380),
    ("EMEA", "Cloud", "Partner", 980000, 340000, "Alice", "2026-02-15", 190),
    ("AMER", "Software", "Direct", 3900000, 1350000, "Bob", "2026-02-15", 950),
    ("AMER", "Cloud", "Partner", 2400000, 1020000, "Bob", "2026-02-15", 460),
    ("APAC", "Software", "Direct", 920000, 310000, "Charlie", "2026-02-15", 240),
    ("APAC", "Hardware", "Partner", 780000, 270000, "Charlie", "2026-02-15", 160),

    # March 2026
    ("EMEA", "Software", "Direct", 1600000, 580000, "Alice", "2026-03-15", 420),
    ("EMEA", "Hardware", "Partner", 910000, 330000, "Alice", "2026-03-15", 170),
    ("AMER", "Software", "Direct", 4200000, 1450000, "Bob", "2026-03-15", 1020),
    ("AMER", "Cloud", "Partner", 2650000, 1100000, "Bob", "2026-03-15", 510),
    ("APAC", "Software", "Direct", 1050000, 350000, "Charlie", "2026-03-15", 280),
    ("APAC", "Cloud", "Partner", 1300000, 520000, "Charlie", "2026-03-15", 340)
]

sales_columns = [
    "region", "product_category", "sales_channel", 
    "total_revenue", "total_cost", "region_manager", 
    "report_date", "total_transactions"
]

df_sales = pd.DataFrame(sales_data, columns=sales_columns)
spark_sales_df = spark.createDataFrame(df_sales)

fact_table_name = "enterprise_catalog.gold_layer.gold_sales_performance"
spark_sales_df.write.mode("overwrite").saveAsTable(fact_table_name)
print(f"✅ Fact table with time-series data successfully saved to: {fact_table_name}")


# ------------------------------------------
# Step 3: Add Detailed Metadata Comments to Fact Table
# ------------------------------------------
print("⏳ Adding metadata comments to the Fact Table...")

spark.sql(f"""
COMMENT ON TABLE {fact_table_name} IS 
'This Gold table contains aggregated regional sales performance, revenues, costs, and transaction metrics broken down by product category and sales channel over time. Use this table for time-series trend analysis, revenue growth, and regional comparisons.';
""")

spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN region COMMENT 'The global sales region. Valid values: EMEA, AMER, APAC. Foreign key to dim_regions.region_code.';")
spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN product_category COMMENT 'The category of the product sold. Examples: Software, Hardware, Cloud.';")
spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN sales_channel COMMENT 'The channel through which the sale was made. Values: Direct, Partner.';")
spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN total_revenue COMMENT 'Total gross revenue in USD. Use this column for calculating total sales volume and revenue trends.';")
spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN total_cost COMMENT 'Total operational and COGS cost in USD associated with the revenue.';")
spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN region_manager COMMENT 'The name of the executive manager responsible for the region (Alice, Bob, Charlie).';")
spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN report_date COMMENT 'The date of the sales report aggregation in YYYY-MM-DD format. Essential for time-series and monthly trend charts.';")
spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN total_transactions COMMENT 'The absolute count of completed customer transactions.';")


# ------------------------------------------
# Step 4: Create Dimension Table (Regions and Managers Metadata)
# ------------------------------------------
print("⏳ Creating the Dimension Table...")

regions_data = [
    ("EMEA", "Alice", "London HQ", "Europe, Middle East & Africa"),
    ("AMER", "Bob", "New York HQ", "North & South America"),
    ("APAC", "Charlie", "Singapore HQ", "Asia-Pacific")
]

regions_columns = ["region_code", "manager_name", "hq_location", "region_description"]
df_regions = pd.DataFrame(regions_data, columns=regions_columns)
spark_regions_df = spark.createDataFrame(df_regions)

dim_table_name = "enterprise_catalog.gold_layer.dim_regions"
spark_regions_df.write.mode("overwrite").saveAsTable(dim_table_name)
print(f"✅ Dimension table successfully saved to: {dim_table_name}")


# ------------------------------------------
# Step 5: Add Metadata Comments to Dimension Table
# ------------------------------------------
print("⏳ Adding metadata comments to the Dimension Table...")

spark.sql(f"""
COMMENT ON TABLE {dim_table_name} IS 
'Dimension table containing metadata about regions, including managers, headquarters, and descriptions. Can be joined with gold_sales_performance using region = region_code.';
""")

spark.sql(f"ALTER TABLE {dim_table_name} ALTER COLUMN region_code COMMENT 'The unique region identifier (EMEA, AMER, APAC). Primary key / Foreign key to gold_sales_performance.region.';")
spark.sql(f"ALTER TABLE {dim_table_name} ALTER MANAGER_NAME COMMENT 'Full name of the regional executive manager.'") # תיקון תחבירי קטן
spark.sql(f"ALTER TABLE {dim_table_name} ALTER COLUMN manager_name COMMENT 'Full name of the regional executive manager.';")
spark.sql(f"ALTER TABLE {dim_table_name} ALTER COLUMN hq_location COMMENT 'The headquarters office location for the region.';")
spark.sql(f"ALTER TABLE {dim_table_name} ALTER COLUMN region_description COMMENT 'Geographical scope description of the region.';")

print("🎉 Time-series data, tables, and metadata have been successfully created and configured in Unity Catalog!")
