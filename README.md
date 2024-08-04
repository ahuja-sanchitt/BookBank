
## Overview

This project is  built with Django and Django REST Framework.
Created By: Sanchit Ahuja(sanchitahujafas@gmail.com)

## Features

- User Registration
- User Login
- View Recommendations,Submit Recommendations
- Filter Recommendations
- Search Books(Google Books API)
- Like Recommendations

## Project Setup Instructions

1. **Clone the repository:**
    ```
    git clone https://github.com/ahuja-sanchitt/BookBank
    ```

2. **Navigate to the project directory:**
    ```
    cd book_recommendation
    ```

3. **Create and activate a virtual environment:**
    ```
    python -m venv venv
    venv\Scripts\activate
    ```

4. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```

5. **Configure DB Settings in settings.py:**
    ```         

6. **Run migrations:**
    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

7. **Start the server:**
    ```
    python manage.py runserver
    ```

## API Endpoints

### User Registration

- **URL:** `/registeruser/`
- **Method:** `POST`
- **Request Payload:**
    ```json
    {
      "username": "string",
      "password": "string",
      "email": "string@example.com"
    }
    ```
- **Response:**
    - `201 Created` - User registered successfully
    - `400 Bad Request` - Invalid input data

### User Login

- **URL:** `/loginuser/`
- **Method:** `POST`
- **Request Payload:**
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
- **Response:**
    - `200 OK` - Returns JWT access and refresh tokens
    - `401 Unauthorized` - Invalid credentials

### Obtain JWT Token

- **URL:** `/token/`
- **Method:** `POST`
- **Request Payload:**
    ```json
    {
      "username": "string",
      "password": "string"
    }
    ```
- **Response:**
    - `200 OK` - Returns JWT tokens (access and refresh)
    - `401 Unauthorized` - Invalid credentials

### Search Books

- **URL:** `/searchbooks/`
- **Method:** `GET`
- **Request Params:**
    - `q` - The query string to search for books
- **Response:**
    - `200 OK` - Returns a list of books matching the query
    - `500 Internal Server Error` - API call to Google Books failed

### Submit Recommendation

- **URL:** `/submit_recommendation/`
- **Method:** `POST`
- **Request Payload:** (Authenticated)
    ```json
    {
      "title": "string",
      "author": "string",
      "description": "string",
      "rating": float
    }
    ```
- **Response:**
    - `201 Created` - Recommendation submitted successfully
    - `400 Bad Request` - Invalid input data

### Get Recommendations

- **URL:** `/get_recommendation/`
- **Method:** `GET`
- **Response:**
    - `200 OK` - Returns a list of all recommendations

### Submit Comment

- **URL:** `/comment/`
- **Method:** `POST`
- **Request Payload:** (Authenticated)
    ```json
    {
      "recommendation_id": integer,
      "comment": "string"
    }
    ```
- **Response:**
    - `201 Created` - Comment added successfully
    - `400 Bad Request` - Invalid input data

### Like Recommendation

- **URL:** `/like/`
- **Method:** `PATCH`
- **Request Payload:** (Authenticated)
    ```json
    {
      "recommendation": integer
    }
    ```
- **Response:**
    - `200 OK` - Recommendation liked successfully
    - `400 Bad Request` - Recommendation ID missing or invalid
    - `404 Not Found` - Recommendation not found

### Filter Recommendations

- **URL:** `/filter/`
- **Method:** `GET`
- **Request Params:**
    - `rating` (optional) - Minimum rating filter
    - `publication_date` (optional) - Filter by publication date
    - `sort_by` (optional) - Sort by `rating` or `publication_date`
- **Response:**
    - `200 OK` - Returns a list of filtered recommendations
    - `400 Bad Request` - Invalid filter or sort parameter

### SWAGGER UI Documentation    
**URL:** `/swagger/`

## External Dependencies

- **Google Books API:** Used to search for books.
- **Django REST Framework:** Used to create and manage API endpoints.
- **JWT (JSON Web Tokens):** Used for authentication.
