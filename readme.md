# Bosta Case Study - Data Engineering

This project is a solution to the Bosta case study for a Data Engineering role. 


## Table of Contents
- [Project Overview](#project-overview)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the ETL Pipeline](#running-the-etl-pipeline)
- [Database Model Design](#database-model-design)
- [Query Optimization](#query-optimization)
- [Notification System](#notification-system)
- [Files in Repository](#files-in-repository)
- [Additional Information](#additional-information)

## Project Overview

This project follows these main objectives:
1. **Data Transformation**: Transform unstructured JSON data into a structured format using a flattening technique.
2. **Database Model Design**: Design a normalized database model to ensure data integrity.
3. **Query Optimization**: Implement optimizations for efficient database query performance.
4. **Notification System**: Set up a system to alert for ETL job failures.

## Prerequisites

- **Python 3.10+**
- **MySQL** or **Amazon Redshift**
- **SQLAlchemy** for database connections
- **pandas** for data manipulation
- **boto3** (if using AWS services for Redshift)

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/islambayoumy/bosta_case_study.git
   cd bosta_case_study
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the ETL Pipeline

1. **Prepare the JSON Data**: Place your JSON data in the `data/` folder.
    - Here I added a sample JSON file `sample_data.json` holding the sample record provided in the case study.
    - Another sample JSON file `sample_generated_data.json` holding a generated sample record (Generated using AI tool).

2. **Run the ETL Job**: The ETL job will read, and transform the JSON data into a structured format and create CSV files.
   ```bash
   python src/etls/data_flatten.py
   ```
3. **Generate CSV Files**: The ETL job will generate CSV files in the `output/` folder.
   - The CSV files will be named based on the JSON data keys.
   - The CSV files will be created in the `output/` folder.

## Database Model Design

The database model is designed to avoid redundancy and maintain data integrity. The main points of this model include:

- **Normalization**: Ensures minimal redundancy and maintains relationships between tables.
- **Entity-Relationship Diagram (ERD)**: An ER diagram is included to illustrate table structures and relationships.

For further details on the database design and justification, refer to the `sql_model_diagram/` folder.
- ***ER_diagram.png***: The ER diagram of the database model.
- ***schema.sql***: The SQL script to create the database schema. [Assuming MySQL is used]
- ***db_model_description.md***: Detailed explanation of the database model design.

## Query Optimization

To enhance query performance, indexing and partitioning strategies are used. Below are the main techniques:

- **Indexing**: Optimizes commonly queried columns.[Added indexes to the `Orders` table and the `City`, `Zone`, and `Country` tables.]
- **Partitioning**: Used if the dataset is large and stored on a system like Redshift.

## Notification System

The notification system is implemented to monitor ETL job failures. If a failure occurs, a notification (e.g., via email, slack, AWS notification service) is triggered. 

- **Implementation**: No implementation is provided in this repository.
- **Notification System Setup**: 
  - Generally, it starts by using a job orchestration tool like Apache Airflow or Dagster.
  - Then, set up a notification service (e.g., AWS SNS, Slack, email) to send alerts on job callbacks.

## Files in Repository

- `src/etls/data_flatten.py`: Script to perform the ETL transformation.
- `input_data/`: Folder containing sample JSON data.
- `output_data/`: Folder containing generated CSV files.
- `sql_model_diagram/`: Folder containing the database model design.
- `requirements.txt`: File containing the required Python packages.
- `src./utils/`: Folder containing utility functions.

## Additional Information

- This project is designed to be run as a python package with entry points for each task.
- It Can be extended to include more complex ETL tasks, data validation, and additional database optimizations.
- A Dockerfile can be added to containerize the application for easier deployment.
- I didn't configure a database connection in this repository, but it can be easily added using SQLAlchemy.


**Author**: Islam Bayoumy

**Documentation and Coding format done with the help of AI tool**.