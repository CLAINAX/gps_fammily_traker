# Live360 Family Tracker Clone

A modular real-time family tracking backend and web client built with FastAPI, Docker, and Leaflet.js. The system is designed with a focus on low resource consumption, utilizing database sharding, in-memory token rotation, and native GeoJSON support.

## Architecture and Features

* **Modular Backend:** Clean separation of concerns structured into distinct packages (`api/`, `core/`, `models/`, and `services/`).
* **Database Sharding:** User data is partitioned into separate JSON files based on the initial character of each UUID, optimizing input/output performance.
* **Geocoding Integration:** Automatic translation of raw geographical coordinates into physical addresses using the Nominatim API (OpenStreetMap).
* **Dynamic Security:** Background asynchronous tasks handle in-memory token rotation, protecting read endpoints while allowing unauthenticated location updates for mobile clients.
* **Interactive Frontend:** A responsive map interface built with Leaflet.js that computes real-time velocity (km/h), tracks idle/inactive duration at specific locations, and provides dynamic route styling.

## Tech Stack

* **Language:** Python 3.10
* **Framework:** FastAPI
* **Containerization:** Docker & Docker Compose
* **Client:** Leaflet.js, HTML5, JavaScript
* **Data Validation:** Pydantic

## Project Structure

```text
live360_modular/
├── api/
│   ├── dependencies.py
│   └── routes.py
├── core/
│   └── security.py
├── models/
│   └── schemas.py
├── services/
│   ├── db_manager.py
│   └── geocoding.py
├── templates/
│   └── map.html
├── data/
│   └── partitions/
├── Dockerfile
├── docker-compose.yml
├── main.py
├── test_app.py
└── requirements.txt

#SPECTS WITH AI

Getting Started
Prerequisites
Docker and Docker Compose installed on your host machine.

Installation and Execution
Clone the repository:

Bash
git clone [https://github.com/your-username/live360_modular.git](https://github.com/your-username/live360_modular.git)
cd live360_modular
Build and start the container using Docker Compose:

Bash
docker compose up -d --build
Access the web interface in your browser:

Plaintext
http://localhost:8000/map
API Endpoints
GET /: Health check endpoint.

GET /api/{user_id}: Retrieve specific user data (Requires authorization).

GET /refresh/?secret=max123: Generates and returns a valid master token.

POST /create-user: Register a new user profile (Requires master token).

PUT /update-location/{user_id}: Update user GPS coordinates (Open for client devices).

DELETE /delete-user/{user_id}: Remove a user profile (Requires master token).

GET /users: Retrieve all user records in GeoJSON format (Requires master token).

GET /status: Returns the internal health status of the automated test system.
<img width="1091" height="519" alt="screenshot_20260815_010808" src="https://github.com/user-attachments/assets/763e30e7-90d0-4088-a730-1b77d38e390f" />
