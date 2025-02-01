# FAQ Backend API

## Installation
1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Run migrations: `python manage.py migrate`
4. Start server: `python manage.py runserver`

## API Usage
- Fetch FAQs: `GET /api/faqs/?lang=hi`
- Admin: `http://localhost:8000/admin`

## Caching
- Uses Redis to cache translations for 1 hour.

## Testing
Run tests with: `python manage.py test`
