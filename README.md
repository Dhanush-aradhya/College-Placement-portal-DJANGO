# Placement Portal

A Django-based placement management system for educational institutions.

## Features

- Student profile management
- Domain and skill tracking
- File upload for photos and resumes
- Admin portal for faculty
- Professional links integration (LinkedIn, GitHub, LeetCode, HackerRank)
- Certification tracking

## Setup Instructions

### Prerequisites
- Python 3.8+
- PostgreSQL
- Virtual environment (recommended)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/Dhanush-aradhya/College-Placement-Portal.git
cd College-Placement-Portal
```

2. Create and activate virtual environment:
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Environment Setup:
   - Copy `.env.example` to `.env`
   - Update database credentials and secret key

5. Database Setup:
```bash
python manage.py makemigrations
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run the development server:
```bash
python manage.py runserver
```

## Environment Variables

Create a `.env` file with the following variables:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
DB_NAME=placement_portal_db
DB_USER=placement_user
DB_PASSWORD=your-password
DB_HOST=localhost
DB_PORT=5432
```

## Project Structure

```
College-Placement-Portal/
├── home/                 # Main Django application
├── django_project/       # Django project settings
├── templates/           # HTML templates
├── static/             # Static files (CSS, JS, images)
├── mediafiles/         # User uploads (not in git)
├── manage.py           # Django management script
├── requirements.txt    # Python dependencies
├── .env.example       # Environment variables template
└── README.md          # This file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Security Notes

- Never commit sensitive data (database files, media uploads, CSV files)
- Keep SECRET_KEY and database credentials in environment variables
- Use `.gitignore` to exclude sensitive files

## License

[Add your license information here]
