# FastAPI Stock Price App

This is a simple FastAPI application that provides functionality to fetch real-time stock prices using the Alpha Vantage API and store the stock data in a database. Additionally, it supports user authentication with JWT (JSON Web Tokens) for secure access to store stock data.

## Features
- **Get real-time stock prices**: Fetch the latest stock prices using the Alpha Vantage API.
- **Store stock data**: Save stock prices in a database.
- **User Authentication**: JWT-based authentication for secure endpoints.
- **Dockerized Application**: The app is packaged and can be run in a Docker container for easy deployment.

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- Docker (for containerization)
- PostgreSQL (or any preferred database)

## Setup and Installation

### 1. Clone the Repository
```bash
git clone https://github.com/yourusername/fastapi-stockprice-app.git
cd fastapi-stockprice-app
