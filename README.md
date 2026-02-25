# Sweet Crumbs Bakery - Full Stack Django Application

A modern e-commerce bakery website built with Django 5.0, featuring product catalog, order management, user authentication, and an AI-powered chatbot.

## 🏗️ Architecture

### Project Structure
```
bakery/
├── bakery/                 # Main Django project
│   ├── settings.py         # Project configuration
│   ├── urls.py            # Root URL routing
│   └── wsgi.py            # WSGI application
├── core/                   # Core application
│   ├── models.py          # Site configuration model
│   ├── views.py           # Home, contact, chatbot API
│   └── management/        # Custom management commands
├── products/               # Product catalog
│   ├── models.py          # Product model with categories
│   ├── views.py           # Product listing and detail views
│   └── admin.py           # Product admin interface
├── orders/                 # Order management
│   ├── models.py          # Order and OrderItem models
│   ├── views.py           # Order processing and tracking
│   └── admin.py           # Order admin interface
├── accounts/               # User management (django-allauth)
├── templates/              # HTML templates
├── static/                 # Static files (CSS, JS, images)
└── media/                  # User uploaded content
```

### Technology Stack
- **Backend**: Django 5.0.7 with Python 3.13
- **Database**: SQLite (development), PostgreSQL ready (production)
- **Authentication**: django-allauth for email-based authentication
- **Frontend**: Tailwind CSS via CDN
- **Static Files**: Whitenoise for production serving
- **AI Features**: OpenAI GPT-4o-mini for chatbot (optional)
- **Environment**: python-dotenv for configuration management

### Key Features
- **Product Catalog**: Categorized bakery items with images
- **Shopping Cart**: Session-based cart with checkout
- **Order Management**: Complete order lifecycle with tracking
- **User Authentication**: Email-based login/registration
- **AI Chatbot**: Knowledge base + OpenAI-powered customer service
- **Admin Interface**: Django admin for products and orders
- **Responsive Design**: Mobile-friendly Tailwind CSS UI

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- pip and virtualenv

### Installation

1. **Clone and setup environment**
```bash
git clone <repository-url>
cd bakery
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Environment setup**
```bash
# Create .env file (optional for development)
cp .env.example .env
# Edit .env with your settings
```

4. **Database setup**
```bash
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Run development server**
```bash
python manage.py runserver
```

7. **Seed sample data (optional)**
```bash
python manage.py seed_products
```

### Access Points
- **Website**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Shop**: http://127.0.0.1:8000/shop/
- **Order Tracking**: http://127.0.0.1:8000/orders/track/

## ⚙️ Configuration

### Environment Variables
Create a `.env` file in the project root:

```env
# Database (optional, defaults to SQLite)
DATABASE_URL=sqlite:///db.sqlite3

# Email (production)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True

# OpenAI (optional, for chatbot)
OPENAI_API_KEY=your-openai-api-key
LLM_ENABLED=true

# Security (production)
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### Database Configuration

#### SQLite (Default)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### PostgreSQL (Production)
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'bakery_db',
        'USER': 'bakery_user',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## 🛠️ Development

### Management Commands
- `python manage.py seed_products` - Load sample product data
- `python manage.py collectstatic` - Collect static files for production

### Testing
```bash
python manage.py test
```

### Code Style
- Follow PEP 8 for Python code
- Use descriptive variable names
- Add docstrings for functions and classes

## 📦 Production Deployment

### Static Files
Static files are served using Whitenoise in production:
```bash
python manage.py collectstatic --noinput
```

### Security Considerations
- Set `DEBUG=False` in production
- Use environment variables for sensitive data
- Configure proper `ALLOWED_HOSTS`
- Use HTTPS in production
- Set up proper database permissions

### Example Production Settings
```python
import os

SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME'),
        'USER': os.getenv('DB_USER'),
        'PASSWORD': os.getenv('DB_PASSWORD'),
        'HOST': os.getenv('DB_HOST'),
        'PORT': os.getenv('DB_PORT'),
    }
}

# Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = int(os.getenv('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = True
```

## 🤖 AI Chatbot Features

The application includes an intelligent chatbot with two modes:

1. **Knowledge Base**: Pre-programmed responses for common queries
2. **OpenAI Integration**: GPT-4o-mini for advanced conversations (optional)

### Chatbot Configuration
- Enable/disable via `LLM_ENABLED` environment variable
- Configure OpenAI API key for advanced features
- Fallback to knowledge base if AI is unavailable

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions:
- Create an issue in the repository
- Contact the development team
- Use the built-in chatbot on the website
