# Betfair Trading Platform

## Overview

This project is a Betfair trading platform that automates the process of monitoring live games, logging significant changes, and handling messages efficiently. It uses Docker, Kafka, and Airflow to create a robust and scalable system.

## Features

- **Automated Data Retrieval**: Fetches pre-game odds for specified markets using the Betfair API.
- **Live Game Monitoring**: Continuously monitors live games for significant changes in the total games value.
- **Logging and Messaging**: Logs changes and sends messages to Kafka for further processing.
- **Scheduled Tasks**: Uses Airflow to schedule and run tasks daily.

## Getting Started

### Prerequisites

- Docker
- Docker Compose
- Python 3.11

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/Prasalaitis/SportsBetting/.git SportsBetting
    ```

2. **Create a `.env` file** with the following content:
    ```env
    APP_KEY=your_app_key
    SESSION_TOKEN=your_session_token
    KAFKA_BOOTSTRAP_SERVERS=localhost:9092
    KAFKA_TOPIC=betfair_topic
    ```

3. **Build and run the Docker containers**:
    ```bash
    docker-compose up --build
    ```

### Usage

1. **Main Application**:
    - The main application is defined in `main.py` and is executed when the Docker container starts.
    - It initializes the Betfair API client, retrieves pre-game odds, monitors live games, and consumes messages from Kafka.

2. **Pre-Game Odds**:
    - The `pre_odds.py` script fetches and logs pre-game odds for NBA total points markets.

3. **Airflow DAG**:
    - The Airflow DAG defined in `dags/betfair_dag.py` schedules and runs the `main` function daily.

### Running Tests

1. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2. **Run tests**:
    ```bash
    pytest
    ```

## Configuration

- **Environment Variables**: Configuration is managed through environment variables defined in the `.env` file.
- **Airflow Configuration**: Airflow is configured to use a local SQLite database and runs with the LocalExecutor.

## Contributing

1. **Fork the repository**.
2. **Create a new branch**:
    ```bash
    git checkout -b feature/your-feature-name
    ```
3. **Make your changes**.
4. **Commit your changes**:
    ```bash
    git commit -m 'Add some feature'
    ```
5. **Push to the branch**:
    ```bash
    git push origin feature/your-feature-name
    ```
6. **Open a pull request**.


## Acknowledgements

- Betfair API Documentation
- Docker
- Apache Kafka
- Apache Airflow