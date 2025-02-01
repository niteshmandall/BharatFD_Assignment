# FAQ Backend API

## Overview
This project is a Django-based backend API for managing Frequently Asked Questions (FAQs) with multi-language support. It integrates a WYSIWYG editor for better content management and utilizes caching for optimized performance.

## Features
- **Multi-language Support**: Automatically translates FAQs into multiple languages (English, Hindi, Bengali) using Google Translate.
- **WYSIWYG Editor**: Uses `django-ckeditor` for rich text formatting in the admin panel.
- **REST API**: Provides endpoints for CRUD operations on FAQs.
- **Caching with Redis**: Enhances performance by caching translations.
- **Dockerized Deployment**: Supports easy setup and deployment using Docker and `docker-compose`.
- **Automated Testing**: Includes unit tests using `pytest-django`.

---

## AWS Deployment Notes
The application has been deployed on AWS with the following details:
- **Base URL:** [http://35.174.5.10:8000](http://35.174.5.10:8000)
- The project is running within a Dockerized environment.
- Ensure that the necessary AWS security groups allow inbound traffic on port **8000**.

---

## Installation
### Prerequisites
Ensure you have the following installed:
- Python 3.9+
- Docker & Docker Compose (if using Docker)
- Redis (for caching)

### Clone the Repository
```bash
git clone https://github.com/niteshmandall/BharatFD_Assignment
cd BharatFD_Assignment
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Apply Migrations
```bash
python manage.py migrate
```

### Run the Server
```bash
python manage.py runserver
```

---

## Setting Up Redis Locally
To run Redis locally, follow these steps:

1. **Install Redis** (if not already installed):
   ```bash
   sudo apt update && sudo apt install redis-server
   ```
   On macOS, use:
   ```bash
   brew install redis
   ```

2. **Start Redis Server**:
   ```bash
   redis-server
   ```

3. **Verify Redis is Running**:
   ```bash
   redis-cli ping
   ```
   It should return `PONG` if Redis is running correctly.
   
---

## Creating Admin Credentials
To create a superuser for accessing the Django admin panel, run the following command:
```bash
python manage.py createsuperuser
```
Follow the prompts to enter a username, email, and password. Once created, you can log in to the admin panel at:
```
http://localhost:8000/admin/
```

---

## Docker Setup
### Running with Docker
1. **Build the Docker Image**:
   ```bash
   docker-compose build
   ```
2. **Start Containers**:
   ```bash
   docker-compose up -d
   ```
3. **Access the API**:
   - Open `http://localhost:8000/api/faqs/`
   - Admin Panel: `http://localhost:8000/admin`

### Stopping the Containers
```bash
docker-compose down
```

---

## API Usage
### Endpoints
#### Fetch FAQs
```bash
GET /api/faqs/?lang=<language>
```
- Example:
  ```bash
  curl http://localhost:8000/api/faqs/?lang=hi
  ```

#### Create an FAQ
```bash
POST /api/faqs/
Content-Type: application/json
{
  "question_en": "What is Django?",
  "answer_en": "Django is a web framework."
}
```

#### Update an FAQ
```bash
PATCH /api/faqs/{id}/
Content-Type: application/json
{
  "answer_en": "Django is a high-level Python web framework."
}
```

#### Delete an FAQ
```bash
DELETE /api/faqs/{id}/
```

---

## Caching
- Uses Redis to cache translated responses for **1 hour**.
- Reduces API latency by avoiding redundant translations.

---

## Running Tests
Execute tests inside the Docker container:
```bash
docker exec -it faq_backend pytest -v
```
Or run locally:
```bash
pytest -v
```

---

## Contribution Guidelines
1. Fork the repository.
2. Create a feature branch.
3. Follow conventional commits (e.g., `feat: add new API endpoint`).
4. Submit a Pull Request.

