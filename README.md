# DevATlas – Developer Learning Hub API

A scalable backend API built with **FastAPI** for a developer learning platform. The project follows a modular architecture and implements secure authentication, authorization, database management, caching, and containerized deployment.

## 🚀 Features

- User Registration & Login
- JWT Authentication
  - Access Token
  - Refresh Token
- Secure Password Hashing using Passlib
- HTTP Bearer Authentication
- Role-Based Access Control (RBAC)
- Token Revocation using Redis
- RESTful CRUD APIs
- MYSQL Database Integration
- SQLAlchemy ORM
- Database Migrations with Alembic
- Pydantic Request & Response Validation
- Dependency Injection
- Asynchronous API Endpoints
- Dockerized Application
- Environment-based Configuration
- Automatic Swagger API Documentation

---

## 🛠 Tech Stack

### Backend
- Python
- FastAPI

### Database
- MYSQL
- Redis

### ORM & Validation
- SQLAlchemy
- Pydantic

### Authentication & Security
- JWT
- HTTP Bearer Authentication
- Passlib
- Role-Based Access Control (RBAC)

### Database Migration
- Alembic


### DevOps
- Docker
- Docker Compose

---


# Authentication Flow

1. User registers.
2. Password is securely hashed using Passlib.
3. User logs in.
4. Server generates:
   - Access Token
   - Refresh Token
5. Protected endpoints require a valid JWT Access Token.
6. Logout revokes the token using Redis.
7. RBAC ensures users can only access authorized resources.

---

# API Modules

- Authentication
- Users
- Technologies
- Recommnendation
- Bookmarks
- Courses
- Quizes

---

# Installation

## Clone Repository

```bash
git clone https://github.com/techhub200/DevAtlas-Developer-Learning-Hub

cd DevAtlas-Developer-Learning-Hub
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate it

### Windows

```bash
venv\Scripts\activate
```

### Linux / macOS

```bash
source venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure Environment Variables

Create a `.env` file.

Example:

```env
DATABASE_URL=mysql+pmysql://user:password@localhost/devatlas

SECRET_KEY=your-secret-key

ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=30

REFRESH_TOKEN_EXPIRE_DAYS=7

REDIS_HOST=localhost

REDIS_PORT=6379
```

---

## Run Database Migrations
```bash
alembic upgrade head
```

---

## Run Server

```bash
uvicorn app.main:app --reload
```
or using FAST API - fastapi dev src/

Server runs at

```
http://127.0.0.1:8000
```

---

# Docker

Build

```bash
docker compose build
```

Run

```bash
docker compose up
```

---

# API Documentation

FastAPI automatically provides API documentation.

Swagger UI

```
http://localhost:8000/docs
```

ReDoc

```
http://localhost:8000/redoc
```

---


---

# Security Features

- JWT Authentication
- Access Token
- Refresh Token
- HTTP Bearer Authentication
- Password Hashing
- Token Revocation using Redis
- Role-Based Access Control
- Environment Variable Configuration

---

# Key Concepts Implemented

- Modular FastAPI Project Structure
- REST API Design
- SQLAlchemy ORM
- Database Relationships
- Dependency Injection
- Authentication & Authorization
- Asynchronous Programming
- Docker Containerization
- Redis Integration
- Alembic Migrations
- Unit Testing
- API Documentation

---

# Future Improvements

- Email Verification
- OAuth (Google/GitHub Login)
- Background Tasks with Celery
- Rate Limiting
- API Versioning
- CI/CD Pipeline
- Kubernetes Deployment
- Monitoring & Logging
- WebSocket Notifications

---

# Author

**Divyanshu Pant**

GitHub: https://github.com/techhub200
