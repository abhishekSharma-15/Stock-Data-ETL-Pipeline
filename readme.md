# Stock Data ETL Pipeline with Apache Airflow

## Project Overview

This project is an end-to-end **Data Engineering pipeline** that fetches daily stock market data from the Yahoo Finance API, processes it using Python, engineers financial features, and loads the transformed data into a PostgreSQL database.

The pipeline is fully automated and orchestrated using **Apache Airflow**, enabling scheduled and reliable execution of ETL workflows.

The primary aim of this project is to demonstrate real-world Data Engineering concepts including:

- API ingestion  
- Data transformation  
- Feature engineering  
- Database design  
- Workflow orchestration  
- Containerization  
- Modular ETL development  

---

## Key Features

### ETL Capabilities
- Fetches real-time stock price data from Yahoo Finance API  
- Parses raw JSON responses into structured tabular data  
- Cleans and validates financial time-series data  
- Engineers quantitative features such as:
  - Daily returns  
  - Log returns  
  - Rolling volatility  
  - Moving averages  
- Loads transformed data into PostgreSQL  
- Implements modular, object-oriented ETL design  
- Config-driven architecture for easy extensibility  

### Orchestration
- Fully automated using **Apache Airflow**
- DAG-based scheduling
- Runs every 5 minutes via cron scheduling
- Task retries and logging
- Multi-stock parallel processing
- Dockerized Airflow environment

---

## Technologies Used

- **Python** – Core programming language  
- **Pandas** – Data manipulation  
- **Requests** – API interaction  
- **PostgreSQL** – Data storage  
- **SQLAlchemy** – Database ORM  
- **Apache Airflow** – Workflow orchestration  
- **Docker & Docker Compose** – Containerization  
- **Object-Oriented Programming (OOP)**  
- **Logging & Config Management**

---

## Project Architecture

The project follows a modular ETL architecture integrated with Airflow scheduling.

### Updated Folder Structure

```bash
Stock-Data-ETL-Pipeline/
│
├── airflow/
│   ├── dags/
│   │   └── stock_etl_dag.py
│   └── docker-compose.yml
│
├── src/
│   ├── ingestion/
│   │   ├── stock_fetcher.py
│   │   └── stock_parser.py
│   ├── transformation/
│   │   └── stock_transformer.py
│   ├── db/
│   │   ├── db_loader.py
│   │   └── engine.py
│   ├── pipeline/
│   │   └── etl_pipeline.py
│   └── utils/
│       ├── config.py
│       └── logger.py
│
├── data/
│   └── raw/
│
├── requirements.txt
├── main.py
└── README.md
---

## Technologies Used

- **Python** – Core programming language  
- **Pandas** – Data manipulation  
- **Requests** – API interaction  
- **PostgreSQL** – Data storage  
- **SQLAlchemy** – Database connection  
- **Object-Oriented Programming (OOP)**  
- **Logging & Config Management**

---

## Data Pipeline Flow

1. **Extract**  
   - Fetches daily stock price data using Yahoo Finance API  
   - Stores raw API responses for audit and reproducibility  

2. **Transform**  
   - Converts JSON to structured DataFrame  
   - Cleans missing values  
   - Generates financial analytics features  

3. **Load**  
   - Stores processed data in PostgreSQL  
   - Uses normalized schema with indexing  
   - Ensures data integrity via constraints  

---

## Database Design

### Tables
**stocks**

| Column    | Type    | Description      |
|----------|---------|------------------|
| stock_id | SERIAL  | Primary Key      |
| symbol   | VARCHAR | Unique Stock Code|

**daily_prices**

| Column         | Description          |
|----------------|----------------------|
| stock_id       | Foreign Key          |
| date           | Trading date         |
| open           | Opening price        |
| high           | High price           |
| low            | Low price            |
| close          | Closing price        |
| volume         | Traded volume        |
| daily_return   | Simple return        |
| log_return     | Log return           |
| volatility_20d | Rolling volatility   |
| ma_20d         | 20-day moving avg    |
| ma_50d         | 50-day moving avg    |

```

## How to Run the Project with Airflow

### 2. Run Docker and Postgres

```bash
git clone https://github.com/augustusHarts/Stock-Data-ETL-Pipeline.git
cd stock_pipeline
```

### 2. Run Docker and Postgres

For docker:
```bash
desktop docker 
```

For Postgres:
```bash
psql -h postgres -h localhost -U postgres
```

### 3. Start Airflow using Docker

```bash
cd airflow
docker-compose up -d
```

### 4. Access Airflow UI

```
https://localhost:8080/login/

username: airflow
password: airflow
```

## How to Run the Project without Airflow

### 1. Create Virtual Environment

```bash
python -m venv etlenv
source etlenv/bin/activate
etlenv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Setup PostgreSQL Database

Create Database:
```
stock_pipeline
```

Configure credentails in:
```
src/utils/config.py
```

Add your local PostgreSQL connection details such as:

- host  
- username  
- password  
- database name  

---

### 5. Run the Pipeline

```bash
python main.py
```

---

## Output

- Raw API responses are stored in:

```
data/raw/
```

- Transformed and cleaned data is loaded into PostgreSQL tables:

```
stocks  
daily_prices
```

---

## Future Enhancements

Planned improvements:

- Automate pipeline using Apache Airflow  
- Add Docker support  
- Implement incremental data loading  
- Add unit tests  
- Build analytics dashboard on top of processed data  

---

## About

This project was built as a portfolio project to showcase foundational Data Engineering and Python development skills.
