# HBnB Project presented by Tommy JOUHANS and James ROUSSEL

## Enhanced Backend with Authentication and Database Integration

**Overview**

In this third phase of the HBnB project, the backend was significantly improved by introducing secure authentication mechanisms, database persistence, and a scalable architecture that follows industry standards.

In previous parts of the project, the system relied on in-memory storage, which was useful for rapid prototyping but unsuitable for production environments. In this phase, the application was redesigned to support persistent storage using SQLAlchemy with SQLite for development and MySQL for production, as well as secure user authentication using JSON Web Tokens (JWT).

The main objective of this phase was to transform the backend into a secure, scalable, and production-ready REST API capable of managing users, places, reviews, and amenities while enforcing proper access control rules.

The project also introduces:

- Role-Based Access Control (RBAC) using the is_admin attribute

- Password hashing with bcrypt

- JWT-based authentication

- Database ORM mapping with SQLAlchemy

- Repository pattern for database operations

- ER diagrams and SQL schema scripts

---

## Project Architecture

The backend follows a layered architecture that separates concerns across different components.

Client
   |
REST API (Flask + Flask-Restx)
   |
Service Layer (Facade)
   |
Repository Layer
   |
SQLAlchemy ORM
   |
Database (SQLite / MySQL)

**Each layer plays a specific role:**

- API Layer handles HTTP requests and responses.

- Service Layer (Facade) contains business logic.

- Repository Layer abstracts database access.

- ORM Layer (SQLAlchemy) maps Python models to database tables.

- Database Layer stores persistent data.

---

### Task 0/ Modify the Application Factory to Include the Configuration

**Objective**

The application factory pattern allows the application to be created dynamically with different configurations. 

This makes it easier to support multiple environments such as development, testing, and production.


**Implementation**

The create_app() function was modified to accept a configuration class and initialize the extensions required by the application.
---
```python
def create_app(config_class=DevelopmentConfig):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    from app.api.v1 import api_v1
    app.register_blueprint(api_v1, url_prefix="/api/v1")

    return app

```
**Key Components Initialized**

|Component	|Purpose     |
|-------|----------------|
|SQLAlchemy	|ORM for database interactions|
|JWTManager	|Authentication with JWT|
|Bcrypt	|Password hashing|

#  Installation & Setup

### 1️/ Clone the repository

Bash:
```shell
- git clone <repository_url>
- cd part3
```

### 2️/ Create a virtual environment (recommended)
```shell
- python3 -m venv venv
- source venv/bin/activate
```

### 3️/ Install dependencies
```shell
- pip install -r requirements.txt
```

**Dependencies:**
- Flask==3.1.2
- Flask-Bcrypt==1.0.1
- Flask-RESTful==0.3.10
- flask-restx==1.3.2
- Flask-SQLAlchemy==3.1.1
- Flask-JWT-Extended==4.7.1
- SQLAlchemy==2.0.48
- PyJWT==2.11.0
- pytest==9.0.2


**Running the Application**
```shell
- python -m hbnb.run
```

### Task 1/ Modify the User Model to Include Password Hashing

**Objective**

The user model was updated to securely store passwords using bcrypt hashing instead of storing plain-text passwords.

This ensures that even if the database is compromised, user passwords cannot be easily recovered.

**Implementation**

Two methods were added to the User model:


**Password Hashing**

```python
def hash_password(self, password):
    self.password = bcrypt.generate_password_hash(password).decode("utf-8")

---
### Task 2/ Implement JWT Authentication with `flask-jwt-extended`

---
### Task 3/ Implement Authenticated User Access Endpoints

---
### Task 4/ Implement Administrator Access Endpoints

---
### Task 5/ Implement SQLAlchemy Repository

---
### Task 6/ Map the User Entity to SQLAlchemy Model

---
### Task 7/ Map the Place, Review, and Amenity Entities

---
### Task 8/ Map Relationships Between Entities Using SQLAlchemy


---
### Task 9/ SQL Scripts for Table Generation and Initial Data

---
### Task 10/ Generate Database Diagrams

---
## Authors

**- Tommy JOUHANS**
**- James ROUSSEL**


**Holberton School – Dijon, FRANCE**