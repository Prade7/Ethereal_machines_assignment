
# Machine Data Management API

This API is built using Flask and SQLAlchemy to manage machine data and user authentication. It provides routes for creating, updating, retrieving, and deleting machine entries, as well as user login and authentication using JWT.

## Table of Contents
- [Setup](#setup)
- [Routes](#routes)
  - [Authentication](#authentication)
  - [Machine Data Management](#machine-data-management)
- [Usage](#usage)
  - [Authentication](#authentication-usage)
  - [Machine Data Management](#machine-data-management-usage)

## Setup

1. **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2. **Environment Variables**
   Make sure to set the following environment variables:
   - `SECRET_KEY`: Secret key for JWT encoding/decoding.
   - `DATABASE_URI`: URI for your SQLAlchemy database.
   
3. **Run the Application**
    ```bash
    flask main.py
    ```

## Routes

### Authentication

- **Login**

    **Endpoint**: `/api/login`  
    **Method**: `POST`  
    **Description**: Authenticates a user using employee ID and password. Returns a JWT on successful authentication.

    **Request Body**:
    ```json
    {
        "employee_id": "string",
        "password": "string",
        "role":"string"
    }
    ```

    **Response**:
    - `200 OK`: Returns a JWT token.
    - `401 Unauthorized`: Invalid employee ID or password.

    - **Example Response**:
     ```json
     {
       "access_token": "your_jwt_token"
     }
     ```

### Machine Data Management

- **Create Machine Data**

    **Endpoint**: `/machines`  
    **Method**: `POST`  
    **Description**: Creates a new machine entry if the machine name does not exist.

    **Request Body**:
    Needs JWT in the header
    ```json
    {
        "name": "string",
        "data": "object"
    }
    ```
    ```json
     {
       "name": "Machine1",
       "acceleration": 6.0,
       "velocity": 12.0,
       "actual_position": [[1, 2, 3, 4, 5]],
       "distance_to_go": [[1, 2, 3, 4, 5]],
       "homed": [[true, true, true, true, true]],
       "tool_offset": [[0.1, 0.2, 0.3, 0.4, 0.5]]
     }
     ```
    **Response**:
    - `201 Created`: Machine data successfully created.
    - `409 Conflict`: Machine with the same name already exists.

- **Update Machine Data**

    **Endpoint**: `/machines/`  
    **Method**: `PUT`  
    **Description**: Updates the machine data if there are changes. Records the employee ID making the change.

    **Request Body**:
    ```json
    {
        "data": "object"
    }
    ```

    **Response**:
    - `200 OK`: Machine data updated successfully.
    - `204 No Content`: No changes detected in the machine data.

- **Delete Machine Data**

    **Endpoint**: `/machines`  
    **Method**: `DELETE`  
    **Description**: No Role has the permission to delete data

    **Response**:
    - `200 OK`: Machine data successfully deleted.
    - `404 Not Found`: Machine with the specified name does not exist.

- **Get Machine Data**

    **Endpoint**: `/machines`  
    **Method**: `GET`  
    **Description**: Retrieves the machine data

    **Response**:
    - `200 OK`: Returns the machine data.

## Usage

### Authentication Usage

- **Login**

    Use the following curl command to log in and obtain a JWT token:

    ```bash
    curl -X POST http://localhost:5000/api/login -H "Content-Type: application/json" -d '{
      "employee_id": "your_employee_id",
      "password": "your_password"
    }'
    ```

### Machine Data Management Usage

- **Create Machine Data**

    ```bash
    curl -X POST http://127.0.0.1:5000/machine \
    -H "Authorization: Bearer <your_jwt_token>" \
    -H "Content-Type: application/json" \
    -d '{
    "name": "Machine_1",
    "acceleration": 10.5,
    "velocity": 200.0,
    "actual_position": {
        "x": 12.5,
        "y": 22.5,
        "z": 35.5,
        "a": 45.5,
        "c": 55.5
    },
    "distance_to_go": {
        "x": 1.5,
        "y": 2.5,
        "z": 3.5,
        "a": 4.5,
        "c": 5.5
    },
    "homed": {
        "x": true,
        "y": false,
        "z": true,
        "a": false,
        "c": true
    },
    "tool_offset": {
        "x": 0.1,
        "y": 0.2,
        "z": 0.3,
        "a": 0.4,
        "c": 0.5
    }
    }'

    ```

- **Update Machine Data**

    ```bash
    curl -X PUT http://127.0.0.1:5000/machine \
    -H "Authorization: Bearer <your_jwt_token>" \
    -H "Content-Type: application/json" \
    -d '{
    "name": "Machine_1",
    "acceleration": 12.0,
    "velocity": 220.0,
    "actual_position": {
        "x": 13.0,
        "y": 23.0,
        "z": 36.0,
        "a": 46.0,
        "c": 56.0
    },
    "distance_to_go": {
        "x": 2.0,
        "y": 3.0,
        "z": 4.0,
        "a": 5.0,
        "c": 6.0
    },
    "homed": {
        "x": true,
        "y": true,
        "z": true,
        "a": true,
        "c": true
    },
    "tool_offset": {
        "x": 0.2,
        "y": 0.3,
        "z": 0.4,
        "a": 0.5,
        "c": 0.6
    }
    }'

    ```


- **Get Machine Data**

    ```bash
    curl -X GET http://localhost:5000/machines/ -H "Authorization: Bearer <your_jwt_token>"
    ```
