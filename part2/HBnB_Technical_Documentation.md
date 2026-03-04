# HBnb Part 2: Implementation of Business Logic and API Endpoints
## Business Logic & REST API Implementation
### Authors: Tommy Jouhans & James Roussel
---

## Project Objective

This phase implements the complete Business Logic Layer and REST API Layer of the HBnB application.

The goal is to build:

- A modular scalable architecture
- Strict data validation
- Full RESTful API
- In-memory persistence
- Relationship management between entities
- Unit and manual testing
- Swagger documentation


---

## Project Structure

![HBNB tree](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/hbnb-tree.png)

---


## Architecture Overview

The project follows a strict 3-layer architecture:

![HBNB UML Task 0](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/task0.png)

---

#  Installation & Setup

## 1️/ Clone the repository

Bash:
```shell
- git clone <repository_url>
- cd part2
```

## 2️/ Create a virtual environment (recommended)
```shell
- python3 -m venv venv
- source venv/bin/activate
```

## 3️/ Install dependencies
```shell
- pip install -r requirements.txt
```

Dependencies:

- flask
- flask-restx

▶ Running the Application
```shell
- python -m hbnb.run
```

If correctly configured, Flask should start successfully.

![Running app](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/running-app.png)

![Print server](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/print-server.png)


Swagger documentation will be available at:

http://127.0.0.1:5000/api/v1/

---

## TASK 0 – Project Initialization

### Objective

Set up scalable architecture using:

Flask App Factory Pattern

Repository Pattern

Facade Pattern

In-memory storage

### Key Files

app/init.py

Registers namespaces:

- api.add_namespace(users_ns, path="/api/v1/users")
- api.add_namespace(places_ns, path="/api/v1/places")
- api.add_namespace(amenities_ns, path="/api/v1/amenities")
- api.add_namespace(reviews_ns, path="/api/v1/reviews")

### persistence/repository.py

```python
class InMemoryRepository:
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)
        return obj

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

```
---
## TASK 1 – Core Business Models

###  BaseModel

Provides:

- UUID id
- created_at
- updated_at
- update() method
```python
class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def update(self, data):
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now()
```

### User Model

Validations:

- first_name required
- last_name required
- valid email format

```python
if not re.match(r'^[^@]+@[^@]+\.[^@]+$', email):
    raise ValueError("Invalid email format")
```

### Place Model

Validations:
- price ≥ 0
- latitude ∈ [-90, 90]
- longitude ∈ [-180, 180]

Supports both:

- owner object (tests)
- owner_id (API)

### Review Model

Supports both:

- user + place objects (tests)
- user_id + place_id (API)

Rating validation:
```python
if not (1 <= rating <= 5):
    raise ValueError("Rating must be between 1 and 5")
```

### Amenity Model
```python
class Amenity(BaseModel):
    def __init__(self, name, description=None):
        if not name:
            raise ValueError("Amenity name is required")
        super().__init__()
```
---
### TASK 2 – User Endpoints
### POST /api/v1/users
- Creates a new user
- Validates input data
- Returns created user with 201 status
- Error handling for missing fields and invalid email

```shell
curl -X POST http://localhost:5000/api/v1/users/ \
  -H "Content-Type: application/json" \
  -d '{"first_name": "John", "last_name": "Doe", "email": "john.doe@example.com"}'
```
Test in Postman:
---
![POST User](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/post-user.png)


### GET /api/v1/users/
- Retrieves all users
- Returns list of users with 200 status
- Supports pagination (optional)
- Error handling for empty database
- 
```shell
curl http://127.0.0.1:5000/api/v1/users/
```

Test in Postman:
---
![Get all Users](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/get-all-users.png)


### GET /api/v1/users/<user_id>
- Retrieves user by ID
- Returns user with 200 status
- Error handling for invalid user_id

```shell
curl http://127.0.0.1:5000/api/v1/users/<USER_ID>
```
Test in Postman:

![GET User by ID](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/get-id-user.png)

### PUT /api/v1/users/<user_id>
- Updates user information
- Validates input data
- Returns updated user with 200 status
- Error handling for invalid user_id and missing fields

```shell
curl -X PUT http://127.0.0.1:5000/api/v1/users/<USER_ID> \
-H "Content-Type: application/json" \
-d '{"first_name":"Jane","last_name":"Doe","email":"jane.doe@example.com"}'
```

Test in Postman:

![PUT User by ID](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/put-id-user.png)


Validation errors return:

- 400 Bad Request
- 404 Not Found

---

### TASK 3 – Amenity Endpoints

### POST /api/v1/amenities
- Creates a new amenity
- Validates input data
- Returns created amenity with 201 status
- Error handling for missing fields

```shell
curl -X POST http://127.0.0.1:5000/api/v1/amenities/ \
-H "Content-Type: application/json" \
-d '{"name":"Wi-Fi"}'
```

Test in Postman:

![POST Amenity](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/post-amenities.png)

### GET /api/v1/amenities/
- Retrieves all amenities
- Returns list of amenities with 200 status
- Supports pagination (optional)
- Error handling for empty database

```shell
curl http://127.0.0.1:5000/api/v1/amenities/
```
Test in Postman:

![POST Amenity](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/get-all-amenities.png)


### GET /api/v1/amenities/<amenity_id>
- Retrieves amenity by ID
- Returns amenity with 200 status
- Error handling for invalid amenity_id

```shell
curl http://127.0.0.1:5000/api/v1/amenities/<AMENITY_ID>
```

Test in Postman:

![GET Amenity by ID](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/get-id-amenities.png)


### PUT /api/v1/amenities/<amenity_id>
- Updates amenity information
- Validates input data
- Returns updated amenity with 200 status
- Error handling for invalid amenity_id and missing fields

```shell
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/<AMENITY_ID> \
-H "Content-Type: application/json" \
-d '{"name": "Air Conditioning", "description": "Keeps you cool"}'
```

Test in Postman:

![PUT Amenity by ID](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/put-id-amenities.png)
---


### TASK 4 – Place Endpoints

### POST /api/v1/places
- Creates a new place
- Validates input data
- Returns created place with 201 status
- Error handling for missing fields and invalid data
- Supports both owner_id and owner object for testing
- Validation errors return:
- 400 Bad Request
- 404 Not Found

```shell
curl -X POST http://127.0.0.1:5000/api/v1/places/ \
-H "Content-Type: application/json" \
-d '{
  "title": "Cozy Apartment",
  "description": "A nice place to stay",
  "price": 100.0,
  "latitude": 37.7749,
  "longitude": -122.4194,
  "owner_id":"<USER_ID>"
}'
```
Test in Postman:

![POST Place](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/post-places.png)



### GET /api/v1/places/
- Retrieves all places
- Returns list of places with 200 status


```shell
curl http://127.0.0.1:5000/api/v1/places/

```

Test in Postman:

---

![GET all Places](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/get-all-places.png)


### GET /api/v1/places/<place_id>
- Retrieves place by ID
- Returns place with 200 status
- Error handling for invalid place_id

```shell
curl -X PUT http://127.0.0.1:5000/api/v1/amenities/<PLACE_ID>

```

Test in Postman:
---

![GET Place by ID](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/get-id-places.png)


### PUT /api/v1/places/<place_id>
- Updates place information
- Validates input data
- Returns updated place with 200 status
- Error handling for invalid place_id and missing fields
- Supports both owner_id and owner object for testing
- Validation errors return:
- 400 Bad Request
- 404 Not Found

```shell
curl -X PUT http://127.0.0.1:5000/api/v1/places/<PLACE_ID> \
-H "Content-Type: application/json" \
-d '{
  "title": "Luxury Condo",
  "description": "An upscale place to stay",
  "price": 200.0
}'
```

Test in Postman:
|:-------|:-------:|-------:|

![PUT Place by ID](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/put-id-places.png)


### POST Amenity for Place
- Associates an amenity with a place
- Validates place_id and amenity_id
- Returns updated place with 200 status
- Error handling for invalid place_id and amenity_id


```shell
 curl -X POST http://127.0.0.1:5000/api/v1/places/<PLACE_ID>/amenities/<amenities_id>
```

Test in Postman:


![POST Amenity for Place](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/post-amenity-for-place.png)



### Validations
- Owner must exist
- Coordinates valid
- Price ≥ 0

---

## TASK 5 – Review Endpoints

### Create Review
- Creates a new review
- Validates input data
- Returns created review with 201 status
- Error handling for missing fields and invalid data
- Supports both user + place objects (tests) and user_id + place_id (API)
- Validation errors return:
- 400 Bad Request
- 404 Not Found

```shell
curl -X POST http://127.0.0.1:5000/api/v1/reviews/ \
-H "Content-Type: application/json" \
-d '{
"text":"Great place to stay",
"rating":5,
"user_id":"<USER_ID>",
"place_id":"<PLACE_ID>"
}'
```
Test in Postman:

![POST Review](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/post-reviews.png)


### GET Review
- Retrieves all reviews
- Returns list of reviews with 200 status


```shell
curl http://127.0.0.1:5000/api/v1/reviews/

```

Test in Postman:

![GET all Reviews](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/get-all-reviews.png)


### GET Review by ID
- Retrieves review by ID
- Returns review with 200 status

```shell
curl http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID>

```

Test in Postman:

![GET Review by ID](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/get-id-reviews.png%20.png)


### PUT Review
- Updates review information
- Validates input data
- Returns updated review with 200 status
- Error handling for invalid review_id and missing fields
- Supports both user + place objects (tests) and user_id + place_id (API)

```shell
curl -X PUT http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID> \
-H "Content-Type: application/json" \
-d '{
"text": "Amazing stay!",
"rating": 4
}'
```

Test in Postman:

![PUT Review by ID](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/put-id-reviews.png)

![PUT Review by ID](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/put-id-reviews2.png)

### Delete Review
- Deletes a review by ID
- Returns 204 No Content on success
- Error handling for invalid review_id


```shell
curl -X DELETE http://127.0.0.1:5000/api/v1/reviews/<REVIEW_ID>

```

Test in Postman:

![DELETE Review by ID](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/delete-id-reviews.png)

![DELETE Review by ID](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/delete-id-reviews2.png)


### GET Reviews for Place
- Retrieves all reviews for a specific place
- Returns list of reviews with 200 status
- Error handling for invalid place_id

```shell
curl http://127.0.0.1:5000/api/v1/places/<PLACE_ID>/reviews

```
Test in Postman:

---

![GET Reviews for Place](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/get-reviews-for-places.png)

---




## TASK 6 – Testing & Validation

### Implemented Basic Validations in the Business Logic Layer
- User: first_name, last_name required; valid email format

![First name is required](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/no-first-name.png)

![Last name is required](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/no-last-name.png)

![Email is required](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/no-mail.png)

![Invalid email format](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/invalid-email.png)

- Place: price ≥ 0; latitude ∈ [-90, 90]; longitude ∈ [-180, 180]

![Price ≥ 0](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/price.png)

![Latitude ∈ (-90, 90)](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/error-latitude.png)

![Longitude ∈ (-180, 180)](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/error-longitude.png)

- Review: rating must be between 1 and 5, text is not empty, ensure that user_id and place_id reference valid entities

![Rating must be between 1 and 5](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/error-rating.png))

![Text is not empty](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/no-text-review.png)

![Ensure that user_id reference valid entities](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/no-user-reviews.png)

![Ensure that place_id reference valid entities](https://github.com/Tommy-JOUHANS/holbertonschool-hbnb/blob/main/part2/images/no-place-reviews.png)


### Automated Tests
- We test all business logic and API endpoints using Python's unittest framework
- Tests cover:
- User creation, retrieval, update
- Amenity creation, retrieval, update
- Place creation, retrieval, update, amenity association
- Review creation, retrieval, update, deletion
- Validations for all models


Run tests with:

```shell
python -m unittest discover -s hbnb/tests
```

Run test_users with:
```shell
python -m unittest hbnb.tests.test_users
```

Run test_places with:
```shell
python -m unittest hbnb.tests.test_places
```

Run test_amenities with:
```shell
python -m unittest hbnb.tests.test_amenities
```
Run test_reviews with:
```shell
python -m unittest hbnb.tests.test_reviews
```

Print All test:

![HBNB UML Task 0](https://github.com/TommyJOUHANSC28/holbertonschool-hbnb/blob/main/part2/images/test-unittest.png)


- ### Manual Testing
- Start the Flask application
- Use Postman or curl to test API endpoints
- Verify correct responses and error handling
- Check Swagger documentation for API reference
- http://127.0.0.1:5000/api/v1/

### Conclusion
This implementation provides:
- Clean architecture
- Strict validation
- Full CRUD REST API
- Relationship management
- Automated testing
- Production-ready structure

---
## Authors

- Tommy Jouhans

- James Roussel

