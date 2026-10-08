# ==========================================
# Project: Enterprise Sales Intelligence & Genie Agent
# Description: Creating Gold layer tables in Unity Catalog with rich metadata comments and foreign key relationships
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
# Step 2: Create Fact Table (Granular Sales Performance Data)
# ------------------------------------------
print("⏳ Creating the main Gold Fact Table...")

sales_data = [
    ("EMEA", "Software", "Direct", 1200000, 450000, "Alice", "2026-01-15", 320),
    ("EMEA", "Hardware", "Partner", 850000, 310000, "Alice", "2026-01-15", 150),
    ("AMER", "Software", "Direct", 3400000, 1200000, "Bob", "2026-01-15", 890),
    ("AMER", "Cloud", "Partner", 2100000, 950000, "Bob", "2026-01-15", 410),
    ("APAC", "Software", "Direct", 850000, 290000, "Charlie", "2026-01-15", 210),
    ("APAC", "Cloud", "Partner", 1100000, 480000, "Charlie", "2026-01-15", 300)
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
print(f"✅ Fact table successfully saved to: {fact_table_name}")


# ------------------------------------------
# Step 3: Add Detailed Metadata Comments to Fact Table (Critical for Genie Agent)
# ------------------------------------------
print("⏳ Adding metadata comments to the Fact Table...")

spark.sql(f"""
COMMENT ON TABLE {fact_table_name} IS 
'This Gold table contains aggregated regional sales performance, revenues, costs, and transaction metrics broken down by product category and sales channel. Use this table for all business queries regarding sales, revenue, profits, and regional managers.';
""")

spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN region COMMENT 'The global sales region. Valid values: EMEA, AMER, APAC. Foreign key to dim_regions.region_code.';")
spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN product_category COMMENT 'The category of the product sold. Examples: Software, Hardware, Cloud.';")
spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN sales_channel COMMENT 'The channel through which the sale was made. Values: Direct, Partner.';")
spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN total_revenue COMMENT 'Total gross revenue in USD. Use this column for calculating total sales volume.';")
spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN total_cost COMMENT 'Total operational and COGS cost in USD associated with the revenue.';")
spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN region_manager COMMENT 'The name of the executive manager responsible for the region (Alice, Bob, Charlie).';")
spark.sql(f"ALTER TABLE {fact_table_name} ALTER COLUMN report_date COMMENT 'The date of the sales report aggregation (YYYY-MM-DD format).';")
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
spark.sql(f"ALTER TABLE {dim_table_name} ALTER COLUMN manager_name COMMENT 'Full name of the regional executive manager.';")
spark.sql(f"ALTER TABLE {dim_table_name} ALTER COLUMN hq_location COMMENT 'The headquarters office location for the region.';")
spark.sql(f"ALTER TABLE {dim_table_name} ALTER COLUMN region_description COMMENT 'Geographical scope description of the region.';")

print("🎉 All tables, metadata, and relationships have been successfully created and configured in Unity Catalog!")