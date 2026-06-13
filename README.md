# EPP SLA AI Business Intelligence Agent

Natural Language to Business Intelligence for EPP SLA Analytics

## Overview

EPP SLA AI BI Agent is an AI-powered analytics application that converts natural language questions into SQL queries, executes them against an EPP SLA analytics database, and visualizes the results through an interactive dashboard.

The application enables business users, operations teams, and engineers to analyze EPP registry performance metrics without writing SQL.

### Example Questions

* Show average response time for ADD-DOMAIN operations over the last 7 days
* Display hourly volume trends for ADD-DOMAIN requests
* List top 10 clients by transaction volume
* Show failed transactions by TLD
* Compare SLA performance before and after a release

---

## Architecture

```text
┌─────────────────────┐
│   Streamlit UI      │
│  AI BI Dashboard    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│   AI Text-to-SQL    │
│      Models         │
│                     │
│ • Custom Flan-T5    │
│ • OpenAI            │
│ • Hugging Face      │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Generated SQL Query │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ SQLite Analytics DB │
│   EPP SLA Dataset   │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Tables & Charts     │
│ Business Insights   │
└─────────────────────┘
```

---

## Features

### AI-Powered Text-to-SQL

Convert natural language questions into executable SQL using:

* Custom Flan-T5 LoRA Model
* OpenAI Models
* Hugging Face Models

### Multi-Model Comparison

Generate and compare SQL output from multiple AI models simultaneously.

### Interactive Analytics Dashboard

* Query execution against SQLite
* Data tables
* Automatic chart generation
* Time-series visualizations
* Trend analysis

### Dynamic Data Generation

* Synthetic EPP SLA dataset generation
* Rolling 100-day history
* Realistic EPP command patterns
* Release deployment simulation

### Database Management

* Automatic SQLite initialization
* S3 database synchronization
* Versioned database support

### User Experience

* Theme selection
* Query history
* Example prompts
* Status tracking
* Responsive dashboard

---

## EPP Data Model

### epp_sla

Operational SLA metrics.

| Column        | Description        |
| ------------- | ------------------ |
| date          | Transaction date   |
| hour          | Hour of day        |
| command       | EPP command        |
| tld           | Top-level domain   |
| response_time | Response latency   |
| result        | Success or failure |
| volume        | Transaction volume |
| client_name   | Registrar          |
| failed_reason | Failure reason     |

### epp_client

Registrar metadata.

| Column            | Description         |
| ----------------- | ------------------- |
| client_name       | Registrar name      |
| client_group      | Customer group      |
| client_location   | Geographic location |
| client_ip_version | IPv4 / IPv6         |

### epp_release

Release deployment information.

| Column           | Description        |
| ---------------- | ------------------ |
| release_name     | Release identifier |
| release_start    | Start date         |
| release_end      | End date           |
| release_location | Deployment region  |

---

## Installation

### Clone Repository

```bash
git clone https://github.com/Garutmanaya/epp-sla-ai-bi-agent.git
cd epp-sla-ai-bi-agent
```

### Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Configure model endpoints using environment variables.

### Custom Model

```bash
export CUSTOM_MODEL_URL=http://localhost:8000/predict
```

### OpenAI

```bash
export OPENAI_API_URL=https://your-api-endpoint
```

### Hugging Face

```bash
export HF_API_URL=https://your-api-endpoint
```

### Optional S3 Configuration

```bash
export AWS_REGION=us-east-1
export S3_BUCKET=my-bucket
export S3_PREFIX=hub
export DB_VERSION=v1
```

---

## Running the Application

```bash
streamlit run src/uiv2/app.py
```

Open:

```text
http://localhost:8501
```

---

## Supported Analytics

### Trend Analysis

* Daily trends
* Hourly trends
* Weekly patterns
* Release impact analysis

### SLA Monitoring

* Response time metrics
* Failure analysis
* Success rate tracking
* Volume monitoring

### Business Intelligence

* Top clients
* Geographic insights
* TLD analytics
* Release comparisons

---

## Example Queries

```text
Show average response time for ADD-DOMAIN over the last 30 days
```

```text
Display hourly transaction volume for COM-DOMAIN yesterday
```

```text
List top 10 registrars by volume
```

```text
Show failures grouped by failure reason
```

```text
Compare response time before and after Release-2
```

---

## Technology Stack

### Frontend

* Streamlit
* Plotly
* Pandas

### Backend

* FastAPI
* Python

### AI / ML

* Google Flan-T5 Base
* LoRA Fine-Tuning
* Hugging Face Transformers

### Data

* SQLite
* Amazon S3

### Cloud

* AWS
* SageMaker
* API Gateway

---

## Related Projects

### EPP SLA AI Text-to-SQL Model

AI model repository responsible for converting natural language into SQL.

```text
epp-sla-ai-text2sql-flant5
```

### EPP SLA AI BI Agent

Business Intelligence dashboard and query execution engine.

```text
epp-sla-ai-bi-agent
```

---

## Vision

Enable business users to interact with operational registry data using natural language and receive immediate business intelligence insights without requiring SQL expertise.

Natural Language → SQL → Analytics → Business Intelligence

