# Stock Trading Project

## Overview

This project is a stock trading application built with Django and PostgreSQL. It is containerized using Docker for development and deployment. The application includes features for stock trading and integrates with an AWS-hosted PostgreSQL database.

## Prerequisites

- Docker
- Docker Compose
- Python 3.12 or higher (for local testing)
- Django 
- PostgresSql
- AWS RDS

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/fasihmuhammadvirk/stock-trading-project.git
cd stock-trading-project

### 2.Create a .env file where in your main folder

```bash 
DB_PASSWORD=your_db_password 
DB_HOST=your_aws_rds_endpoint 

Replace your_db_password and your_aws_rds_endpoint with your actual database password and RDS endpoint.
### 3. Build and Run 
Use Docker Compose to build and start the application:
```bash
docker-compose up --build

This command will build the Docker image and start the application in a Docker container.

### 4. Apply Database Migrations
Once the container is up and running, apply the initial migrations to set up the database schema:

```bash 
docker-compose exec web python manage.py migrate

### 5. Access the Application

After starting the containers, you can access the application at http://localhost:8000.

### 6. Run Tests

```bash 
docker-compose exec web python manage.py test

### 7. Stopping the Containers

```bash 
docker-compose down

## Without Docker (Local Development)

### 1. Clone the Repository
```bash 
git clone https://github.com/yourusername/stock-trading-project.git
cd stock-trading-project

### 2. Create and Activate a Virtual Environment

```bash 
python -m venv env
source env/bin/activate  # On Windows use `env\Scripts\activate`

### 3. Install Dependencies

```bash
pip install -r requirements.txt

### 4. Create and Configure .env File

Create a .env file in the root directory of the project (where manage.py is located) with the following content:
```bash 
DB_PASSWORD=your_db_password
DB_HOST=your_aws_rds_endpoint

Replace your_db_password and your_aws_rds_endpoint with your actual database password and RDS endpoint.

### 5. Apply Database Migrations

Run the following command to set up the database schema:

```bash
python manage.py migrate

### 6. Run the Development Server
Start the Django development server:
```bash 
python manage.py runserver

Access the application at http://localhost:8000.

### 7. Run Tests

To run tests, use the following command:

```bash 
python manage.py test



## Troubleshooting
**Connection** Issues: Ensure that your .env file has the correct database credentials and that your AWS RDS instance allows connections from your Docker container or local machine.
**Database** Migrations: If you encounter issues with migrations, check your database configuration and make sure your database is correctly set up.