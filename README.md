# BharatQuest 🗺️

BharatQuest is a full-stack, Django-powered web application designed as an interactive cultural exploration platform. The platform enables users to discover, search, and engage with rich content celebrating heritage, geography, and historical narratives.

## 🚀 Features

- **User Authentication:** Secure user registration, login, and profile management utilizing a custom User model (`accounts` app).
- **Advanced Content Management:** A rich blogging engine (`blog` app) integrated with CKEditor 5 for beautifully formatted articles, media handling, and cultural storytelling.
- **Robust Search Architecture:** Dedicated query processing (`search` app) allowing users to dynamically filter and discover platform content.
- **Production-Ready Security:** Configured with decoupled environment variables (`python-decouple`), strict secure cookie flags, and automated media/static file optimization utilities (`django-cleanup`).

## 🛠️ Tech Stack

- **Backend Framework:** Django (Python)
- **Rich Text Editing:** Django CKEditor 5
- **Environment Management:** Python-Decouple (with `.env` isolation)
- **Database:** SQLite (Development) / Scalable to PostgreSQL/MySQL
- **Frontend Infrastructure:** Semantic HTML5, CSS3, JavaScript, Django Template Engine

## 💻 Local Development Setup

To get a local copy of BharatQuest up and running on your machine, follow these steps:

### 1. Clone the Repository
git clone https://github.com/Swadesh-India/BharatQuest
cd BharatQuest

### 2. Set Up a Virtual Environment
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate

### 3. Install Dependencies
pip install -r requirements.txt

### 4. Configure Environment Variables
Create a .env file in the root directory (alongside manage.py) and add your local keys:
SECRET_KEY=your_local_django_secret_key
DEBUG=True
ALLOWED_HOSTS=127.0.0.1,localhost
EMAIL_HOST_USER=your_email@gmail.com
EMAIL_HOST_PASSWORD=your_google_app_password

### 5. Initialize the Database & Run
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver

Navigate to http://127.0.0.1:8000/ in your browser to view the application.

## 📁 Project Structure

BharatQuest/
│
├── accounts/          # Custom user authentication and profiles
├── blog/              # Content generation, categories, and articles
├── core/              # Global views, landing pages, and shared utilities
├── search/            # Site-wide search processing and filtering
├── web/               # Core project configuration (settings.py, urls.py)
│
├── static/            # Global CSS, JS, and image assets
├── templates/         # Shared HTML layout files
├── .gitignore         # Explicitly ignores venv, .env, and db.sqlite3
├── manage.py          # Django management script
└── requirements.txt   # Project dependencies
