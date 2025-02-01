# FAQ Backend API

## Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`

## Docker Setup & Deployment
### Running the Project in Docker
1. **Build the Docker Image:**
   ```bash
   docker-compose build
   ```
2. **Start Containers:**
   ```bash
   docker-compose up -d
   ```
3. **Access the API:**
   - Open `http://localhost:8000/api/faqs/`
   - Admin Panel: `http://localhost:8000/admin`

### Stopping the Containers
```bash
docker-compose down
```

## API Usage
- Fetch FAQs: `GET /api/faqs/?lang=hi`
- Admin: `http://localhost:8000/admin`

## Caching
- Uses Redis to cache translations for 1 hour.

## Testing
Run tests inside the Docker container:
```bash
docker exec -it faq_backend pytest -v
```
