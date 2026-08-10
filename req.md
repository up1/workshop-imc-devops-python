# API :: Create a new employee

## API Specification
- **Method**: POST
- **Endpoint**: /api/employees
- **Request Body**: JSON object 
```
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "position": "Software Engineer"
}
```
- **Response**:
  - **Success**: HTTP 201 Created
  ```
  {
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@example.com",
    "position": "Software Engineer"
  }
  ```
  - **Error**: HTTP 400 Bad Request
  ```
  {
    "error": "Invalid request body"
  }
  ```
  - **Error**: HTTP 500 Internal Server Error
  ```
  {
    "error": "Internal server error"
  }
  ```

## Business flow
1. The client sends a POST request to the /api/employees endpoint with the employee details in the request body.
2. The server validates the request body to ensure all required fields are present and correctly formatted.
3. If the validation fails, the server responds with a 400 Bad Request status and an error message indicating the issue.
4. If the validation passes, the server creates a new employee record in the database and responds with a 201 Created status and the newly created employee object  

## Input Validation in table format
| Field | Type | Required | Validation |
|-------|------|----------|------------|
| name | string | Yes | Must be a non-empty string |
| email | string | Yes | Must be a valid email address |
| position | string | Yes | Must be a non-empty string |

## Database Schema
- **Table Name**: employees
- **Columns**:
| Column | Type | Constraints |
|--------|------|------------|
| id | SERIAL | PRIMARY KEY |
| name | VARCHAR(255) | NOT NULL |
| email | VARCHAR(255) | NOT NULL, UNIQUE | 
| position | VARCHAR(255) | NOT NULL |
| created_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |
| updated_at | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP |