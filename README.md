# To-Do Microservices Project

This repository contains a microservices-based To-Do application. Each service is independently containerized and communicates over internal Docker networking.

## Services Overview

- **api-gateway** – Entry point for all external requests; handles routing and authentication.
- **auth-service** – Handles user registration, login, and JWT token verification.
- **tasks-service** – Manages personal task CRUD operations.
- **share-service** – Manages task sharing between users.

---

## Repository Structure

Each service contains:
- `app/` – Source code (FastAPI app, routes, services, models, etc.)
- `Dockerfile` – Image build instructions
- `requirements.txt` – Python dependencies

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/KhaledSheheri/To-Do.git
cd To-Do
```

### 2. Change db urls

DATABASE_URL=postgresql://user:pass@host.docker.internal:5432/db_name

### 3. Build Docker Images

```bash
docker build -t <service-name>-image .
```


### 4. Change db urls
```bash
docker run --name <container-name> -p <host-port>:<container-port> <service-name>-image
```
Note: Use the same ports provided in the DockerFiles


