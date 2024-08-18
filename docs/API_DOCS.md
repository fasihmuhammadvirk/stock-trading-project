
# Stock Trading API Documentation

## API Endpoints

### 1. **User Management**

#### Create a New User

- **Endpoint**: `POST /users/`
- **Description**: Registers a new user with a username and initial balance.
- **Request Body**:
  ```json
  {
    "username": "newuser",
    "balance": 500.00
  }
  ```
- **Response**:
  - **201 Created**: If the user is successfully created.
  - **400 Bad Request**: If the request data is invalid.
  ```json
  {
    "user_id": 1,
    "username": "newuser",
    "balance": "500.00"
  }
  ```

#### Retrieve User Data

- **Endpoint**: `GET /users/{username}/`
- **Description**: Retrieves the data for a specific user by username.
- **Response**:
  - **200 OK**: If the user is found.
  - **404 Not Found**: If the user does not exist.
  ```json
  {
    "user_id": 1,
    "username": "newuser",
    "balance": "500.00"
  }
  ```

### 2. **Stock Data Management**

#### Ingest Stock Data

- **Endpoint**: `POST /stocks/`
- **Description**: Adds or updates stock data in the database.
- **Request Body**:
  ```json
  {
    "ticker": "AAPL",
    "open_price": 145.00,
    "close_price": 150.00,
    "high": 155.00,
    "low": 140.00,
    "volume": 1000000,
    "timestamp": "2023-08-17T14:00:00Z"
  }
  ```
- **Response**:
  - **201 Created**: If the stock data is successfully ingested.
  - **400 Bad Request**: If the request data is invalid.
  ```json
  {
    "ticker": "AAPL",
    "open_price": "145.00",
    "close_price": "150.00",
    "high": "155.00",
    "low": "140.00",
    "volume": 1000000,
    "timestamp": "2023-08-17T14:00:00Z"
  }
  ```

#### Retrieve All Stock Data

- **Endpoint**: `GET /stocks/`
- **Description**: Retrieves data for all stocks.
- **Response**:
  - **200 OK**: Returns a list of all stock data.
  ```json
  [
    {
      "ticker": "AAPL",
      "open_price": "145.00",
      "close_price": "150.00",
      "high": "155.00",
      "low": "140.00",
      "volume": 1000000,
      "timestamp": "2023-08-17T14:00:00Z"
    },
    {
      "ticker": "GOOGL",
      "open_price": "2700.00",
      "close_price": "2750.00",
      "high": "2800.00",
      "low": "2650.00",
      "volume": 1500000,
      "timestamp": "2023-08-17T14:00:00Z"
    }
  ]
  ```

#### Retrieve Specific Stock Data

- **Endpoint**: `GET /stocks/{ticker}/`
- **Description**: Retrieves data for a specific stock by ticker symbol.
- **Response**:
  - **200 OK**: If the stock data is found.
  - **404 Not Found**: If the stock data does not exist.
  ```json
  {
    "ticker": "AAPL",
    "open_price": "145.00",
    "close_price": "150.00",
    "high": "155.00",
    "low": "140.00",
    "volume": 1000000,
    "timestamp": "2023-08-17T14:00:00Z"
  }
  ```

### 3. **Transaction Management**

#### Create a Transaction

- **Endpoint**: `POST /transactions/`
- **Description**: Creates a new transaction (buy/sell) for a user.
- **Request Body**:
  ```json
  {
    "user_id": 1,
    "ticker": "AAPL",
    "transaction_type": "buy",
    "transaction_volume": 2
  }
  ```
- **Response**:
  - **201 Created**: If the transaction is successfully created.
  - **400 Bad Request**: If the user does not have sufficient balance or request data is invalid.
  ```json
  {
    "transaction_id": 1,
    "user": 1,
    "ticker": "AAPL",
    "transaction_type": "buy",
    "transaction_volume": 2,
    "transaction_price": "300.00",
    "timestamp": "2023-08-17T14:00:00Z"
  }
  ```

#### Retrieve All Transactions for a User

- **Endpoint**: `GET /transactions/{user_id}/`
- **Description**: Retrieves all transactions for a specific user.
- **Response**:
  - **200 OK**: Returns a list of transactions for the user.
  ```json
  [
    {
      "transaction_id": 1,
      "user": 1,
      "ticker": "AAPL",
      "transaction_type": "buy",
      "transaction_volume": 2,
      "transaction_price": "300.00",
      "timestamp": "2023-08-17T14:00:00Z"
    },
    {
      "transaction_id": 2,
      "user": 1,
      "ticker": "GOOGL",
      "transaction_type": "sell",
      "transaction_volume": 1,
      "transaction_price": "2750.00",
      "timestamp": "2023-08-18T10:00:00Z"
    }
  ]
  ```

#### Retrieve Transactions for a User within a Date Range

- **Endpoint**: `GET /transactions/{user_id}/{start_timestamp}/{end_timestamp}/`
- **Description**: Retrieves all transactions for a user within a specific date and time range.
- **Response**:
  - **200 OK**: Returns a list of transactions within the specified date range.
  ```json
  [
    {
      "transaction_id": 1,
      "user": 1,
      "ticker": "AAPL",
      "transaction_type": "buy",
      "transaction_volume": 2,
      "transaction_price": "300.00",
      "timestamp": "2023-08-17T14:00:00Z"
    }
  ]
  ```

## Error Handling

- **400 Bad Request**: The server could not understand the request due to invalid syntax or insufficient user balance for transactions.
- **404 Not Found**: The requested resource (user, stock, or transaction) does not exist.
- **500 Internal Server Error**: The server encountered a situation it doesn't know how to handle.

## Status Codes

- **200 OK**: The request was successful.
- **201 Created**: The resource was successfully created.
- **400 Bad Request**: There was an error with the request.
- **404 Not Found**: The requested resource was not found.
- **500 Internal Server Error**: The server encountered an error.

## Notes

- Timestamps should be provided in ISO 8601 format (e.g., `"2023-08-17T14:00:00Z"`).
- Prices and balances are handled as decimal values with up to two decimal places.
- Ensure that all required fields are provided in the request body for POST endpoints.
