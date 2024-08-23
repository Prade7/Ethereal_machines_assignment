# Ethereal machines

## Overview
This project is designed to handle api request at the rate of 30 per minute to update the details in the db. It includes various functionalities accessible via defined API routes, with structured models for data handling and robust error handling mechanisms.

## File Structure

- **main.py**: The main entry point of the application, handling route definitions and application logic.
- **requirements.txt**: Lists the Python dependencies required to run the application.
- **cnc.txt**: Contains the data's that needs to be modified
- **application/**: Contains additional modules, models, and configurations for the application.
- **script/**: Includes scripts used for API request to the flask server
- **Dockerfile**: A script for building and running the application in a Docker container.
## API Routes and Their Functionality

### 1. **`POST /api/login`**
   - **Description**: Authenticates the user based on the provided username and assigns a role.
   - **Request**:
     ```json
     {
       "username": "manager"
     }
     ```
   - **Response**: Returns a JWT access token if the username is valid.
   - **Example Response**:
     ```json
     {
       "access_token": "your_jwt_token"
     }
     ```

### 2. **`GET /viewmachines`**
   - **Description**: Retrieves the list of all machines and their associated dynamic data.
   - **Response**: A JSON object containing the details of all machines, including their acceleration, velocity, latest timestamp, and dynamic data.
   - **Example Response**:
     ```json
     {
       "Machine1": {
         "acceleration": 5.0,
         "velocity": 10.0,
         "latest_timestamp": "2024-08-23T14:48:00.000Z",
         "dynamic_data": [
           {
             "actual_position": {"x": 1, "y": 2, "z": 3, "a": 4, "c": 5},
             "distance_to_go": {"x": 1, "y": 2, "z": 3, "a": 4, "c": 5},
             "homed": {"x": true, "y": true, "z": true, "a": true, "c": true},
             "tool_offset": {"x": 0.1, "y": 0.2, "z": 0.3, "a": 0.4, "c": 0.5}
           }
         ]
       }
     }
     ```

### 3. **`POST /updatemachine`**
   - **Description**: Updates the details of a specific machine. The update is permitted only if the user has the required role.
   - **Request**: A JSON object containing the updated machine details, including acceleration, velocity, and dynamic data.
   - **Request Example**:
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
   - **Response**: Returns a message indicating whether the machine was updated, added, or if no changes were detected.
   - **Example Response**:
     ```json
     {
       "message": "Machine Machine1 updated."
     }
     ```

### 4. **`DELETE /deletemachine/<string:machine_name>`**
   - **Description**: Deletes a specific machine from the database. This operation is allowed only for users with the required role.
   - **Request**: The machine name is passed as a URL parameter.
   - **Response**: A message indicating whether the machine was successfully deleted.
   - **Example Response**:
     ```json
     {
       "message": "Machine Machine1 deleted."
     }
     ```

## Models

### 1. **Machine Model**
   - **Attributes**:
     - `id`: Primary key (integer).
     - `name`: Name of the machine (string).
     - `acceleration`: Machine acceleration (float).
     - `velocity`: Machine velocity (float).
     - `timestamp`: Timestamp of the last update (datetime).

### 2. **DynamicData Model**
   - **Attributes**:
     - `id`: Primary key (integer).
     - `machine_name`: Name of the associated machine (string).
     - `actual_position`: Dictionary containing the actual position of machine axes (dict).
     - `distance_to_go`: Dictionary containing the distance to go for machine axes (dict).
     - `homed`: Dictionary indicating whether each axis is homed (dict).
     - `tool_offset`: Dictionary containing tool offset values for each axis (dict).

## Error Handling

### 1. **PermissionDeniedError**
   - **Description**: Raised when a user tries to perform an operation without sufficient permissions.
   - **Response**: 
     ```json
     {
       "message": "You do not have permission to perform this action."
     }
     ```
   - **Status Code**: 403 Forbidden

### 2. **MachineNotFoundError**
   - **Description**: Raised when a requested machine is not found in the database.
   - **Response**: 
     ```json
     {
       "message": "Machine Machine1 not found."
     }
     ```
   - **Status Code**: 404 Not Found

### 3. **InvalidDataError**
   - **Description**: Raised when the provided data is invalid or malformed.
   - **Response**: 
     ```json
     {
       "message": "Invalid data provided."
     }
     ```
   - **Status Code**: 400 Bad Request

## How to Run Locally

### Prerequisites
Ensure you have the following installed on your machine:
- Python 3.x
- Git




### Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Prade7/Ethereal_machines_assignment.git
   cd your-repo-name
Install Dependencies:
If running locally without Docker, install the required Python packages:

bash
Copy code
pip install -r requirements.txt

### Running the Application:
```
python main.py

```
```
python script/script.py
```
