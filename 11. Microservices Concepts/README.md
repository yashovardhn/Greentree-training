# Django Authentication Microservice

A secure and scalable authentication microservice built with Django REST Framework and JWT (JSON Web Tokens).

## Features

- User registration with email and password
- JWT-based authentication
- Token refresh functionality
- Password change functionality
- User profile management
- RESTful API endpoints
- API documentation with Swagger/ReDoc

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <project-directory>
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Copy `.env.example` to `.env` and update the values:
   ```bash
   cp .env.example .env
   ```

5. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

6. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

## Running the Server

```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

## API Documentation

- **Swagger UI**: http://127.0.0.1:8000/api/docs/
- **ReDoc**: http://127.0.0.1:8000/api/redoc/

## Available Endpoints

- `POST /api/auth/register/` - Register a new user
- `POST /api/auth/login/` - Login and get JWT tokens
- `POST /api/auth/logout/` - Logout (blacklist refresh token)
- `GET /api/auth/profile/` - Get or update user profile
- `POST /api/auth/change-password/` - Change user password
- `POST /api/auth/token/refresh/` - Refresh JWT token
- `POST /api/auth/token/verify/` - Verify JWT token

## Environment Variables

- `DEBUG` - Set to `True` for development, `False` for production
- `SECRET_KEY` - Django secret key
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts
- `ACCESS_TOKEN_LIFETIME` - Access token lifetime in seconds (default: 3600)
- `REFRESH_TOKEN_LIFETIME` - Refresh token lifetime in days (default: 7)

## License

MIT
