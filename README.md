# DentalCom - Dental Practice Management System

A comprehensive dental practice management system built with Django REST Framework and modern frontend technologies. This system provides a complete solution for dental practices including appointment booking, product management, service catalog, and blog functionality.

## 🚀 Features

### Core Functionality
- **Appointment Management**: Complete appointment booking system with patient information tracking
- **Product Catalog**: E-commerce functionality for dental products with categories, pricing, and inventory management
- **Service Management**: Comprehensive service catalog with detailed descriptions and images
- **Blog System**: SEO-optimized blog with categories, tags, and content management
- **Admin Dashboard**: Full Django admin interface for content management

### Technical Features
- **RESTful API**: Complete REST API built with Django REST Framework
- **Responsive Design**: Modern, mobile-friendly frontend interface
- **Image Management**: Support for product and service images with optimization
- **SEO Optimization**: Built-in SEO features for blog posts and content
- **Database Management**: SQLite database with proper migrations
- **Media Handling**: Proper static and media file management

## 🛠️ Technology Stack

### Backend
- **Django 5.2.6**: Web framework
- **Django REST Framework 3.15.2**: API development
- **Pillow 10.4.0**: Image processing
- **Django Filter 24.2**: API filtering
- **SQLite**: Database (development)

### Frontend
- **HTML5/CSS3**: Modern web standards
- **Bootstrap**: Responsive framework
- **JavaScript/jQuery**: Interactive functionality
- **Font Awesome**: Icons and UI elements

## 📁 Project Structure

```
DentalCom/
├── Backend/                    # Django backend application
│   ├── Backend/               # Main Django project settings
│   ├── Product/               # Product management app
│   ├── Service/               # Service management app
│   ├── Blog/                  # Blog system app
│   ├── frontendCore/          # Core frontend functionality
│   └── manage.py              # Django management script
├── Frontend/                   # Frontend templates and assets
│   ├── assets/                # CSS, JS, and image files
│   ├── media/                 # User-uploaded media files
│   └── *.html                 # HTML templates
├── requirements.txt            # Python dependencies
└── README.md                  # Project documentation
```

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/DentalCom.git
   cd DentalCom
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   cd Backend
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Frontend: http://127.0.0.1:8000/
   - Admin Panel: http://127.0.0.1:8000/admin/
   - API: http://127.0.0.1:8000/api/

## 📚 API Endpoints

### Products
- `GET /api/products/` - List all products
- `GET /api/products/{id}/` - Get product details
- `POST /api/products/` - Create new product (admin)
- `PUT /api/products/{id}/` - Update product (admin)
- `DELETE /api/products/{id}/` - Delete product (admin)

### Services
- `GET /api/services/` - List all services
- `GET /api/services/{id}/` - Get service details
- `POST /api/services/` - Create new service (admin)
- `PUT /api/services/{id}/` - Update service (admin)
- `DELETE /api/services/{id}/` - Delete service (admin)

### Blog
- `GET /api/blog/posts/` - List all blog posts
- `GET /api/blog/posts/{slug}/` - Get blog post details
- `GET /api/blog/categories/` - List blog categories
- `GET /api/blog/tags/` - List blog tags

### Appointments
- `POST /api/appointments/` - Book new appointment
- `GET /api/appointments/` - List appointments (admin)

## 🗄️ Database Models

### Product Model
- Product information with categories (Orthodontics, Cosmetic, Preventive, etc.)
- Pricing with sale functionality
- Image management with primary image support
- SEO-friendly slugs and metadata

### Service Model
- Service descriptions and metadata
- Image galleries for service visualization
- Featured and new service flags

### Blog Model
- Complete blog post system with SEO optimization
- Categories and tags for content organization
- View and like counting
- Draft/published status management

### Appointment Model
- Patient information collection
- Service selection and scheduling
- Status tracking (pending, confirmed, cancelled, completed)

## 🎨 Frontend Features

- **Responsive Design**: Mobile-first approach with Bootstrap
- **Modern UI**: Clean, professional dental practice interface
- **Interactive Elements**: Smooth animations and transitions
- **Image Galleries**: Product and service image showcases
- **Contact Forms**: Appointment booking and contact forms
- **Blog Integration**: SEO-optimized blog with social features

## 🔧 Configuration

### Environment Variables
The project uses Django's built-in settings. For production, consider:
- Setting `DEBUG = False`
- Configuring proper database (PostgreSQL recommended)
- Setting up proper static file serving
- Configuring email settings for appointment notifications

### Media Files
- Product images: `Frontend/media/products/`
- Service images: `Frontend/media/services/`
- Blog images: `Frontend/media/blog/images/`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 📞 Support

For support and questions, please open an issue in the GitHub repository or contact the development team.

## 🔮 Future Enhancements

- [ ] User authentication and patient portal
- [ ] Payment integration for products and services
- [ ] Email notifications for appointments
- [ ] Advanced reporting and analytics
- [ ] Mobile app development
- [ ] Integration with dental practice management software
- [ ] Multi-language support
- [ ] Advanced SEO features

---

**Built with ❤️ for dental professionals**
