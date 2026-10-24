# Fridays

Fridays is a Django REST API backend for managing a weekly class/meetup group. Members sign up (with invitation codes), mark attendance for classes, keep a wallet balance that is charged per class, upload payment receipts, and share comments, quotes, and videos per class. Admins can create classes, assign tasks, and update member wallets.

## Features

- Custom user model with username login, profile image, and premium flag
- Token/JWT authentication (signup, login, profile view and update)
- Invitation codes for registration
- Wallets per user, payment image uploads, admin wallet updates
- Classes with date, description, charge amount, availability, and finished state
- Attendance toggling, class history, and attended-classes list
- Tasks with deadlines, creator, and assigned users
- Comments and quotes per class
- Video uploads per class

## Tech stack

- Python 3, Django 5.0
- Django REST Framework, `djangorestframework-simplejwt`, DRF token auth
- SQLite
- Pillow, python-dotenv
- Passenger WSGI (`passenger_wsgi.py`) for shared-hosting deployment

## Project structure

```
fridays/    Project settings and root URLs
account/    Custom user, invitation codes, wallet, auth API
members/    Classes, attendance, wallet admin API
task/       Tasks API
comment/    Comments and quotes API ("quommento")
upload/     Class video uploads API
req.txt     Python dependencies
```

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r req.txt
python manage.py migrate
python manage.py createsuperuser
```

Note: `req.txt` is saved as UTF-16; if pip fails to read it, convert it first, e.g. `iconv -f utf-16 -t utf-8 req.txt > requirements.txt`.

## Configuration

Create a `.env` file in the project root:

```
DEBUG=1
HOST=https://your-domain.example
```

`DEBUG` is enabled when the variable has any non-empty value; leave it unset for production. `SECRET_KEY` is currently set in `fridays/settings.py` and should be replaced with your own value.

## Running

```bash
python manage.py runserver
```

All API routes are under `/api/` (e.g. `/api/login/`, `/api/signup/`, `/api/tasks/`, `/api/class-history/`, `/api/videos/`). The admin is at `/admin/`.
