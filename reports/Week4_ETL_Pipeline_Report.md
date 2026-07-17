# Week 4 ETL Pipeline Project Report

## Operational Data ETL Pipeline with Automated Data Quality Validation

---

# 1. Project Overview

This project implements an end-to-end ETL (Extract, Transform, Load) pipeline that processes operational sensor data.

The pipeline extracts raw data, cleans and transforms it, validates data quality using Great Expectations, and loads the final validated dataset into SQLite.

The objective was to build a reliable and automated data engineering workflow capable of handling real-world data quality issues.

---

# 2. Problem Statement

Operational datasets often contain data quality problems such as:

- Missing values
- Duplicate records
- Invalid sensor measurements
- Incorrect data types
- Inconsistent categorical values

Poor-quality data can affect analytics and decision-making.

This project solves this problem by creating an automated pipeline that cleans, validates, and stores reliable operational data.

---

# 3. ETL Pipeline Architecture

```text
Raw Sensor CSV Data

        |
        v

Extraction Layer

        |
        v

Transformation Layer

        |
        +----------------+
        |                |
        v                v

Data Cleaning      Data Standardization

        |
        v

Great Expectations
Data Validation

        |
        v

SQLite Database

        |
        v

Validated Dataset
```