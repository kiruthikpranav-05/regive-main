# ReWear

ReWear is a Flask and MySQL clothing-donation platform. Donors publish usable clothing, NGOs securely claim available listings, and administrators can monitor the platform.

## Features

- Donor, NGO, and Admin roles with protected routes
- Secure password hashing and Flask-Login sessions
- Donation image uploads and donor history
- NGO search/filtering, collection history, and atomic single-NGO claims
- Admin user and donation management screens
- Responsive, modern social-impact interface

## Setup

Prerequisites: Python 3.10+, MySQL 8+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
```

Create a MySQL database:

```sql
CREATE DATABASE rewear CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Edit `.env` and set `SECRET_KEY` plus `DATABASE_URL`, for example:

```text
DATABASE_URL=mysql+pymysql://root:your-password@localhost/rewear
```

Load environment variables before running Flask (PowerShell):

```powershell
Get-Content .env | ForEach-Object { if ($_ -match '^([^#=]+)=(.*)$') { [Environment]::SetEnvironmentVariable($matches[1], $matches[2], 'Process') } }
$env:FLASK_APP='app:create_app'
flask init-db
flask create-admin
flask run
```

Open `http://127.0.0.1:5000`.

## Test flow

Register one donor and two NGOs. Create a donation as the donor, then log in as each NGO to see it. Claim it using one NGO: it immediately disappears for the other, and a repeated direct POST claim is rejected. Create an administrator with `flask create-admin` to inspect both users and the donation.

## Project layout

```text
app.py             Flask app factory and CLI commands
models.py          SQLAlchemy models
routes/            Authentication and role-specific blueprints
templates/         Jinja pages by role
static/uploads/    Locally uploaded donation images
```

Never commit `.env` or real credentials. For production, set environment variables in the host environment, use HTTPS, and set a strong random `SECRET_KEY`.
