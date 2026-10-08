# Enterprise Sales Intelligence Agent & Gold Layer Architecture

## 🚀 Project Overview
This project demonstrates an end-to-end Data & AI architecture built on **Databricks**, featuring a structured **Gold Layer** (Fact and Dimension tables) registered in **Unity Catalog**, integrated with a managed **Genie AI Agent** for natural language querying (Text-to-SQL).

## 🛠️ Architecture & Tech Stack
* **Data Platform:** Databricks (Spark SQL, Unity Catalog)
* **Data Modeling:** Star Schema (Fact table + Dimension table with foreign key relationships)
* **Metadata Governance:** Table & Column Comments for semantic context enhancement
* **AI Agent:** Databricks Genie Space (Managed Text-to-SQL Agent with Trusted Q&A)

## 📂 Repository Structure
- `create_gold_tables.py`: PySpark script for generating and registering the Gold layer tables with rich metadata comments and foreign key definitions.
