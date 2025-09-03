# Telegram Market Bot - Multi-page Website

A comprehensive e-commerce platform for selling ready-made Telegram bot templates, built with Django 5.2 and Bootstrap 5.

## Features

### Core Functionality
- **Multi-page Website**: Home, catalog, template details, user dashboard, admin panel
- **Template Catalog**: Browse, search, filter, and purchase bot templates
- **User Management**: Registration, authentication, profile management
- **Order System**: Complete order processing with status tracking
- **Payment Integration**: Framework ready for Telegram Payments API and crypto payments
- **Demo Bot Generation**: Live demo bot creation for templates (mock implementation)
- **Admin Interface**: Comprehensive admin panel for content management
- **REST API**: Full API endpoints for all major functionality

### Technical Features
- **Responsive Design**: Bootstrap 5 with custom CSS
- **Modern Architecture**: Clean separation of concerns with Django apps
- **Database Models**: Comprehensive relationships between users, templates, orders, payments
- **File Management**: Template file upload and secure download system
- **Security**: CSRF protection, secure authentication, input validation
- **API Documentation**: RESTful API with proper serialization

## Technology Stack

- **Backend**: Django 5.2, Django REST Framework
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (development), PostgreSQL ready
- **APIs**: Telegram Bot API integration framework
- **Authentication**: Django's built-in auth system

## Installation & Setup

### Prerequisites
- Python 3.8+
- Virtual environment (recommended)

### Quick Start

1. **Clone and Setup**:
```bash
cd /home/win/dev/landing-page
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. **Database Setup**:
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

3. **Load Sample Data** (Optional):
```bash
python create_sample_data.py
```

4. **Run Development Server**:
```bash
python manage.py runserver
```

5. **Access the Application**:
- Website: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/
- API Root: http://localhost:8000/api/v1/

## Project Structure

```
telegram_market/
├── core/                 # Main app with home page and shared functionality
├── users/                # User management and authentication
├── templates/            # Bot template catalog and management
├── orders/               # Order processing and tracking
├── payments/             # Payment processing and integration
├── static/               # CSS, JavaScript, images
├── templates/            # HTML templates
├── media/                # User uploaded files
└── telegram_market/      # Django project settings
```

## Key Models

- **User**: Extended Django user with Telegram username
- **Category**: Template categories for organization
- **Template**: Bot templates with features, pricing, files
- **Order**: Purchase orders with status tracking
- **Payment**: Payment processing with multiple methods
- **Review**: User reviews and ratings for templates

## API Endpoints

### Templates
- `GET /api/v1/templates/` - List all templates
- `GET /api/v1/templates/{id}/` - Template details
- `GET /api/v1/templates/featured/` - Featured templates
- `GET /api/v1/templates/popular/` - Popular templates

### Orders
- `GET /api/v1/orders/` - User's orders
- `POST /api/v1/orders/` - Create new order
- `GET /api/v1/orders/{id}/` - Order details
- `PATCH /api/v1/orders/{id}/cancel/` - Cancel order

### Payments
- `GET /api/v1/payments/` - User's payments
- `POST /api/v1/payments/` - Create payment
- `PATCH /api/v1/payments/{id}/update_status/` - Update payment status

## Configuration

### Telegram Integration
Add to `settings.py`:
```python
# Telegram Bot Settings
TELEGRAM_BOT_TOKEN = 'your-bot-token'
TELEGRAM_WEBHOOK_URL = 'https://yourdomain.com/webhook/'

# Payment Settings
TELEGRAM_PAYMENT_TOKEN = 'your-payment-provider-token'
```

### Production Settings
- Configure PostgreSQL database
- Set up static file serving (WhiteNoise or CDN)
- Configure secure settings (SECRET_KEY, DEBUG=False)
- Set up proper logging
- Configure webhook URLs for Telegram

## Sample Data

The project includes sample data with:
- 6 template categories
- 8 realistic bot templates with features and pricing
- Demo users and admin account

Run `python create_sample_data.py` to populate the database.

## Demo Bot Feature

The demo bot generation creates temporary bot instances for users to test templates:
- Mock implementation for demonstration
- Returns bot username, expiry, and commands
- Framework ready for real Telegram API integration

## Admin Interface

Comprehensive admin panel includes:
- Template management with inline features
- Order tracking and status updates
- User management with Telegram usernames
- Payment monitoring and processing
- Category and review moderation

## Security Features

- CSRF protection on all forms
- User authentication required for purchases
- Secure file uploads with validation
- SQL injection protection via ORM
- XSS protection in templates
- Download token system for secure file access

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### Static Files
```bash
python manage.py collectstatic
```

## Deployment

### Production Checklist
- [ ] Set DEBUG=False
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure Telegram webhook URLs
- [ ] Set up SSL certificates
- [ ] Configure payment provider tokens
- [ ] Set up monitoring and logging
- [ ] Configure backup strategy

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For support and questions:
- Check the Django documentation
- Review the API documentation at `/api/v1/`
- Check server logs for debugging

---

**Status**: ✅ Complete and fully functional
**Last Updated**: December 2024

A comprehensive e-commerce platform for selling ready-made Telegram bot templates. Built with Django, this platform provides a complete marketplace experience with user authentication, template catalog, payment processing, and administrative features.

## 🚀 Features

### Core Functionality
- **Multi-page responsive website** with modern design
- **User authentication** (registration, login, logout, profile management)
- **Template catalog** with advanced filtering and search
- **Template detail pages** with demo bot generation
- **Shopping cart and order management**
- **Payment processing** (Telegram Payments API ready)
- **User dashboard** with order history and downloads
- **Admin panel** for template and order management
- **Review system** for templates
- **Demo bot generation** (Telegram API integration ready)

### Technical Features
- **Django 5.2** with modern best practices
- **Bootstrap 5** responsive design
- **RESTful API** architecture ready
- **PostgreSQL/SQLite** database support
- **File upload** handling for templates
- **Session-based authentication**
- **CSRF protection** and security features
- **Pagination** and filtering
- **Real-time demo** bot generation

## 🛠 Technology Stack

- **Backend**: Django 5.2, Django REST Framework
- **Frontend**: Bootstrap 5, JavaScript (ES6), HTML5, CSS3
- **Database**: SQLite (development), PostgreSQL (production ready)
- **APIs**: Telegram Bot API, Telegram Payments API
- **Images**: Pillow for image processing
- **Authentication**: Django's built-in auth system

## 📦 Installation

### Prerequisites
- Python 3.12+
- pip (Python package manager)
- Virtual environment (recommended)

### Setup Instructions

1. **Clone the repository** (if not already in the directory):
   ```bash
   git clone <repository-url>
   cd landing-page
   ```

2. **Create and activate virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install django djangorestframework pillow python-telegram-bot requests
   ```

4. **Run database migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create sample data**:
   ```bash
   python create_sample_data.py
   ```

6. **Create superuser** (admin access):
   ```bash
   python manage.py createsuperuser
   ```
   Or use the existing admin account:
   - Username: `admin`
   - Password: `admin123`

7. **Start development server**:
   ```bash
   python manage.py runserver
   ```

8. **Access the website**:
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## 📁 Project Structure

```
landingpage/
├── telegram_market/          # Project settings
├── core/                      # Core app (home, about, contact)
├── users/                     # User management
├── templates/                 # Template catalog and management
├── orders/                    # Order processing
├── payments/                  # Payment handling
├── static/                    # Static files (CSS, JS, images)
├── templates/                 # HTML templates
├── media/                     # User uploads
├── manage.py                  # Django management script
└── create_sample_data.py      # Sample data creation script
```

## 🔧 Configuration

### Environment Variables
For production deployment, set these environment variables:

```bash
# Django Settings
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

# Database (PostgreSQL)
DATABASE_URL=postgresql://user:password@localhost:5432/dbname

# Telegram API
TELEGRAM_BOT_TOKEN=your-bot-token
TELEGRAM_PAYMENT_TOKEN=your-payment-token
TELEGRAM_WEBHOOK_URL=https://yourdomain.com/payments/telegram/webhook/

# File Storage
MEDIA_ROOT=/path/to/media/files
STATIC_ROOT=/path/to/static/files
```

### Telegram Integration
1. Create a bot via [@BotFather](https://t.me/BotFather)
2. Get your bot token
3. Set up payment provider (for Telegram Payments)
4. Configure webhook URL for payment notifications

## 🎯 Usage

### For Users
1. **Browse Templates**: Visit the homepage and explore available templates
2. **Try Demos**: Generate live demo bots to test functionality
3. **Purchase**: Create account and purchase templates
4. **Download**: Access purchased templates from your dashboard
5. **Review**: Leave reviews for templates you've used

### For Administrators
1. **Access Admin Panel**: Visit `/admin/` with admin credentials
2. **Manage Templates**: Add, edit, or remove templates
3. **Process Orders**: Monitor and manage customer orders
4. **User Management**: Handle user accounts and permissions
5. **Analytics**: View sales and usage statistics

## 📋 Available Pages

### Public Pages
- **Home** (`/`) - Landing page with featured templates
- **Templates** (`/templates/`) - Full catalog with filtering
- **Template Detail** (`/templates/<slug>/`) - Individual template pages
- **About** (`/about/`) - Company information
- **Contact** (`/contact/`) - Contact information and FAQ
- **Login/Register** (`/users/login/`, `/users/register/`) - Authentication

### User Dashboard
- **Dashboard** (`/users/dashboard/`) - User overview
- **Profile** (`/users/profile/`) - Account settings
- **Orders** (`/orders/`) - Order history
- **Downloads** (`/orders/download/<token>/`) - Template downloads

### Admin Features
- **Admin Panel** (`/admin/`) - Complete site administration
- **Template Management** - Add/edit templates
- **Order Processing** - Handle payments and downloads
- **User Management** - Manage accounts

## 🔌 API Endpoints

The platform includes REST API endpoints for future mobile app or third-party integrations:

```
GET  /api/v1/templates/        # List templates
GET  /api/v1/templates/:id/    # Template details
POST /api/v1/templates/:id/demo/ # Generate demo
GET  /api/v1/orders/           # User orders
POST /api/v1/orders/           # Create order
POST /api/v1/payments/process/ # Process payment
```

## 🎨 Design Features

### Responsive Design
- **Mobile-first** approach with Bootstrap 5
- **Adaptive layouts** for all screen sizes
- **Touch-friendly** interface elements
- **Fast loading** with optimized assets

### User Experience
- **Intuitive navigation** with breadcrumbs
- **Search and filtering** for easy template discovery
- **Live demos** to test before purchasing
- **Clear pricing** and feature information
- **Streamlined checkout** process

### Visual Design
- **Modern UI** with clean typography
- **Consistent color scheme** and branding
- **Card-based layouts** for better content organization
- **Interactive elements** with hover effects
- **Loading states** and feedback messages

## 🚀 Deployment

### Production Checklist
1. Set `DEBUG = False`
2. Configure production database (PostgreSQL)
3. Set up static file serving (nginx/Apache)
4. Configure HTTPS/SSL
5. Set up backup strategy
6. Configure monitoring and logging
7. Set up Telegram webhook for payments

### Recommended Hosting
- **VPS**: DigitalOcean, Linode, AWS EC2
- **Platform**: Heroku, Railway, PythonAnywhere
- **Database**: PostgreSQL (managed or self-hosted)
- **CDN**: CloudFlare, AWS CloudFront

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is created for educational and demonstration purposes. Please ensure you have appropriate licenses for any production use.

## 🆘 Support

For questions or issues:
1. Check the FAQ in the contact page
2. Review the code documentation
3. Create an issue in the repository
4. Contact the development team

## 🔮 Future Enhancements

- **Real Telegram API integration** for live demo bots
- **Advanced analytics** dashboard
- **Multi-language support**
- **Advanced payment methods** (Stripe, PayPal)
- **Template versioning** system
- **Bulk operations** for admin
- **API rate limiting** and caching
- **Email notifications** system
- **Social media integration**
- **Advanced search** with Elasticsearch

---

**Built with ❤️ for the Telegram bot development community**