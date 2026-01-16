# 🌡️ nest_data

> Collect Google Nest thermostat data and visualize it in Grafana

[![Python](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.123.9-009688.svg)](https://fastapi.tiangolo.com/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## 📋 Overview

This project connects to Google Nest devices via the Smart Device Management API, stores temperature and HVAC data in PostgreSQL, and enables visualization through Grafana dashboards.

## ✨ Features

- 🔐 OAuth2 authentication with Google Nest API
- 📊 Real-time thermostat data collection
- 💾 PostgreSQL database storage with TimescaleDB support
- 🚀 FastAPI REST endpoints
- 📈 Grafana-ready data structure

## 🛠️ Tech Stack

- **Backend**: FastAPI, Python 3.12
- **Database**: PostgreSQL with psycopg3
- **Auth**: Google OAuth2
- **API**: Google Smart Device Management API

## Quick Start

### Prerequisites

- Python 3.12+
- PostgreSQL database
- Google Cloud Project with Smart Device Management API enabled
- Google Nest Device Access credentials

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/nest_data.git
cd nest_data
```
2. **Create virtual environment**
```bash
python -m venv nest_project
source nest_project/bin/activate
```
# On Windows: nest_project\Scripts\activate

3. **Install dependencies**
```bash
    pip install -r requirements.txt
```
4.**Configure environment variables**
```bash
cp .env.example .env
```
# Edit .env with your credentials

5. **Set up your .env file**
```.env
CLIENT_SECRET_FILE=/path/to/client_secret.json
REDIRECT_URI=http://localhost:8080/auth/callback
PROJECT_ID=your-google-project-id
DB_HOST=localhost
DB_USER=postgres
DB_NAME=nest_data
DB_PASSWORD=your-password
DB_PORT=5432
```
**Running the Application**
```bash
uvicorn app.auth.auth:app --host 0.0.0.0 --port 8080
```

## 📡 API Endpoints
Endpoint	Method	Description
/auth/login	GET	Initiate OAuth2 flow
/auth/callback	GET	OAuth2 callback handler
/nest/devices	GET	Fetch current device data

## 🗄️ Database Schema
PostgreSQL database with `thermostat_readings` table for storing temperature, humidity, and HVAC mode data with timestamps.



## 🔒 Security
All credentials are stored in .env (not committed to git)

OAuth tokens stored locally in tokens.json (gitignored)

Ready for migration to HashiCorp Vault

## 📝 License
This project is licensed under the MIT License - see the LICENSE file for details.