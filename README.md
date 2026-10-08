# Enterprise Sales Intelligence Agent & Gold Layer Architecture

## 🚀 Project Overview
This project demonstrates an end-to-end Data & AI architecture built on **Databricks**, featuring a structured **Gold Layer** (Fact and Dimension tables) registered in **Unity Catalog**, integrated with a managed **Genie AI Agent** for natural language querying (Text-to-SQL).

## 🛠️ Architecture & Tech Stack
* **Data Platform:** Databricks (Spark SQL, Unity Catalog)
* **Data Modeling:** Star Schema (Fact table + Dimension table with foreign key relationships & time-series data)
* **Metadata Governance:** Table & Column Comments for semantic context enhancement
* **AI Agent:** Databricks Genie Space (Managed Text-to-SQL Agent with Trusted Q&A and Instructions)

## 🤖 AI Agent (Genie Space) Configuration
The project includes a configured **Genie AI Agent** (`GlobalSales-Intelligence-Agent`) designed for business users to query data naturally. 

- **General Instructions:** Configured to enforce proper table joins (`gold_sales_performance` joined with `dim_regions` on `region = region_code`) and accurate metric aggregations.
- **Trusted Q&A Examples:** Curated examples built-in to eliminate hallucinations and ensure correct SQL generation for time-series trends and regional performance.

## 📂 Repository Structure
- `create_gold_tables.py`: PySpark script for generating and registering the Gold layer tables with rich metadata comments and foreign key definitions.

## 📊 Genie Agent in Action
![Genie Agent Demo](<img width="1705" height="898" alt="image" src="https://github.com/user-attachments/assets/598317d7-6f98-490e-b283-be5f734c912c" />
<img width="1711" height="846" alt="image" src="https://github.com/user-attachments/assets/87905769-58e0-4289-998b-ac499ba2019c" />
)
