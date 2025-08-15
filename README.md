# r-ztm-f-d

# Title: Task Manager API

## 🚀 Setup Instructions

### Create Virtual Environment
```bash
python -m venv venv
```
### Activate Virtual Environment
```bash
venv\Scripts\activate
```
### Install Dependencies
```bash
pip install -r requirements.txt
```
### Run the Application
```bash
python -m flask run
```
### Run Tests
```bash
pytest
```
# Task Management API

A simple Flask-based API for user authentication and task management.

---

## Setup

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
python -m flask run
```
Authentication

All task-related routes require an auth header with a Bearer token.

Header format:
```bash
auth: Bearer <JWT_TOKEN>
```
Tokens are obtained from /auth/signup or /auth/signin.

API Reference
Auth Routes
POST /auth/signup
```bash
STATUS_CODES = {
    200: "Success",
    400: "Wrong inputs",
    401: "Wrong password",
    403: "Not authorized",
    404: "Resource not found",
    409: "Resource already exists",
    500: "Internal server error"
}
```

Create a new user and get a token.

Request:
```bash
{
  "name": "John Doe",          // min: 1 char
  "userid": "johndoe123",      // min: 1 char
  "password": "password123"    // min: 8 chars
}
```
Response:
```bash
{
  "message": "OK",
  "id": "<user_uuid>",
  "auth": "<JWT_TOKEN>"
}
```
POST /auth/signin

Login and get a token.

Request:
```bash
{
  "userid": "johndoe123",      // min: 1 char
  "password": "password123"    // min: 6 chars
}
```
Response:
```bash
{
  "message": "OK",
  "id": "<user_uuid>",
  "auth": "<JWT_TOKEN>"
}
```
Task Routes (Require Auth Header)
GET /tasks

Get all tasks for the authenticated user.

Response:
```bash
{
  "message": "OK",
  "tasks": [
    {
      "id": "<task_uuid>",
      "title": "Example Task",
      "description": "Details",
      "completed": false,
      "created_at": "2025-08-15T10:00:00"
    }
  ]
}
```
GET /tasks/<task_id>

Get a single task.

Response:
```bash
{
  "message": "OK",
  "task": {
    "id": "<task_uuid>",
    "title": "Example Task",
    "description": "Details",
    "completed": false,
    "created_at": "2025-08-15T10:00:00"
  }
}

```
POST /tasks

Create a task.

Request:
```bash
{
  "title": "New Task",         // required, max: 255 chars
  "description": "Optional"    // optional
}
```
Response:
```bash
{
  "message": "Created",
  "task": { ... }
}
```
PUT /tasks/<task_id>

Update a task.

Request:
```bash
{
  "title": "Updated Title",     // optional, max: 255 chars
  "description": "Optional",    // optional
  "completed": true             // optional
}
```
Response:
```bash
{
  "message": "Success",
  "task": { ... }
}
```
DELETE /tasks/<task_id>

Delete a task.

Response:
```bash
{
  "message": "Success"
}
```








## Objective:
Build a RESTful API for a simple task manager application using either Flask or Django. The API should allow users to perform basic CRUD operations on tasks and should include user authentication.

## Requirements:

1. Task Model:

* Create a model for tasks with the following fields:
** id (auto-generated)
** title (string)
** description (text)
** completed (boolean)
** created_at (timestamp)
** updated_at (timestamp)

2. API Endpoints:

* Implement the following endpoints:
** GET /tasks: Retrieve a list of all tasks.
** GET /tasks/{id}: Retrieve details of a specific task.
** POST /tasks: Create a new task.
** PUT /tasks/{id}: Update details of a specific task.
** DELETE /tasks/{id}: Delete a specific task.

3. User Authentication:

* Implement user authentication using either JWT or session-based authentication.
* Users should be able to register and log in.
* Only authenticated users should be able to create, update, or delete tasks.

4. Documentation:

* Provide clear and concise API documentation, including examples of requests and responses.
* Use any documentation tool of your choice (e.g., Swagger, ReDoc).

5. Testing:

* Write unit tests to ensure the correctness of your API endpoints.
* Include instructions on how to run the tests.

## Bonus Points (Optional):

* Implement pagination for the list of tasks.
* Add filtering options for tasks (e.g., filter by completed status).
* Include user roles (e.g., admin, regular user) with different permissions.

## Submission:

* Share your codebase via a version control system (e.g., GitHub).
* Include a README.md file with instructions on how to set up and run the application.
* Provide any additional notes or explanations you think are necessary.
## Evaluation Criteria:

* Code organization and structure.
* Correct implementation of CRUD operations.
* User authentication and authorization.
* Quality and coverage of tests.
* Clarity and completeness of documentation.
