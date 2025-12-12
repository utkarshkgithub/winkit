# Winkit E-Commerce API

A comprehensive Django REST Framework-based e-commerce backend API with JWT authentication, product management, shopping cart, and order processing capabilities.

## Features

- 🔐 **JWT Authentication** - Secure user authentication using Simple JWT
- 👥 **User Management** - Custom user model with registration and profile management
- 📦 **Product Management** - Full CRUD operations for products and categories
- 🛒 **Shopping Cart** - Add, update, and manage cart items
- 📋 **Order Processing** - Place orders, track status, and manage deliveries
- 🔍 **Advanced Filtering** - Search and filter products by category
- 👨‍💼 **Admin Panel** - Django admin interface for managing the entire platform
- 📊 **RESTful API** - Clean, well-documented API endpoints

## Tech Stack

- **Django 4.2+** - High-level Python web framework
- **Django REST Framework** - Powerful toolkit for building Web APIs
- **Simple JWT** - JSON Web Token authentication
- **SQLite/PostgreSQL** - Database (SQLite for development, PostgreSQL for production)
- **Django CORS Headers** - Handle Cross-Origin Resource Sharing

## Project Structure

```
winkit/
├── authentication/          # User authentication and management
│   ├── models.py           # Custom User model
│   ├── serializers.py      # User serializers
│   ├── views.py            # Auth views (signup, login, me)
│   └── urls.py             # Auth endpoints
├── products/               # Product and category management
│   ├── models.py           # Product and Category models
│   ├── serializers.py      # Product serializers
│   ├── views.py            # Product ViewSets
│   └── urls.py             # Product endpoints
├── cart/                   # Shopping cart functionality
│   ├── models.py           # Cart and CartItem models
│   ├── serializers.py      # Cart serializers
│   ├── views.py            # Cart API views
│   └── urls.py             # Cart endpoints
├── orders/                 # Order management
│   ├── models.py           # Order and OrderItem models
│   ├── serializers.py      # Order serializers
│   ├── views.py            # Order API views
│   └── urls.py             # Order endpoints
└── winkit/                 # Project configuration
    ├── settings.py         # Django settings
    ├── urls.py             # Main URL configuration
    └── wsgi.py             # WSGI configuration
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment (recommended)

### Step 1: Clone the Repository

```bash
cd /home/variable/django-mdn/winkit
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration

Create a `.env` file in the root directory:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# For PostgreSQL (optional)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=winkit_db
# DB_USER=your_db_user
# DB_PASSWORD=your_db_password
# DB_HOST=localhost
# DB_PORT=5432
```

### Step 5: Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser

```bash
python manage.py createsuperuser
```

Follow the prompts to create an admin account.

### Step 7: Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

## API Documentation

### Authentication Endpoints

#### Sign Up
- **URL:** `POST /auth/signup`
- **Body:**
```json
{
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890",
    "address": "123 Main St, City, Country"
}
```
- **Response:**
```json
{
    "user": {
        "id": 1,
        "username": "johndoe",
        "email": "john@example.com",
        "first_name": "John",
        "last_name": "Doe"
    },
    "tokens": {
        "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc...",
        "access": "eyJ0eXAiOiJKV1QiLCJhbGc..."
    }
}
```

#### Login
- **URL:** `POST /auth/login`
- **Body:**
```json
{
    "username": "johndoe",
    "password": "securepassword123"
}
```
- **Response:** Same as signup

#### Get Current User
- **URL:** `GET /auth/me`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
```json
{
    "id": 1,
    "username": "johndoe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone_number": "1234567890",
    "address": "123 Main St, City, Country",
    "created_at": "2025-12-11T10:00:00Z"
}
```

### Product Endpoints

#### List All Products
- **URL:** `GET /products/`
- **Query Parameters:**
  - `category=<category_name>` - Filter by category
  - `search=<keyword>` - Search in name/description
  - `ordering=price` - Order by price, -price, name, -created_at
- **Response:**
```json
{
    "count": 10,
    "next": null,
    "previous": null,
    "results": [
        {
            "id": 1,
            "name": "Product Name",
            "description": "Product description",
            "category": 1,
            "category_name": "Electronics",
            "price": "99.99",
            "discounted_price": "89.99",
            "image_url": "https://example.com/image.jpg",
            "stock": 50,
            "discount": "10.00",
            "is_in_stock": true,
            "created_at": "2025-12-11T10:00:00Z"
        }
    ]
}
```

#### Get Product by ID
- **URL:** `GET /products/<id>/`
- **Response:** Single product object

#### Create Product (Admin Only)
- **URL:** `POST /products/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
```json
{
    "name": "New Product",
    "description": "Product description",
    "category": 1,
    "price": "99.99",
    "stock": 100,
    "discount": "10.00",
    "image_url": "https://example.com/image.jpg"
}
```

#### Update Product (Admin Only)
- **URL:** `PUT /products/<id>/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:** Same as create

#### Delete Product (Admin Only)
- **URL:** `DELETE /products/<id>/`
- **Headers:** `Authorization: Bearer <access_token>`

### Category Endpoints

#### List All Categories
- **URL:** `GET /categories/`
- **Response:**
```json
{
    "count": 5,
    "results": [
        {
            "id": 1,
            "name": "Electronics",
            "description": "Electronic devices and gadgets",
            "products_count": 25,
            "created_at": "2025-12-11T10:00:00Z"
        }
    ]
}
```

#### Get Category by ID
- **URL:** `GET /categories/<id>/`

#### Create/Update/Delete Category
- Admin only, similar to products

### Cart Endpoints

#### Get Cart
- **URL:** `GET /cart/`
- **Headers:** `Authorization: Bearer <access_token>`
- **Response:**
```json
{
    "id": 1,
    "user": 1,
    "items": [
        {
            "id": 1,
            "product": 1,
            "product_details": { /* Full product object */ },
            "quantity": 2,
            "subtotal": "179.98"
        }
    ],
    "total_items": 2,
    "total_price": "179.98"
}
```

#### Add to Cart
- **URL:** `POST /cart/add`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
```json
{
    "product_id": 1,
    "quantity": 2
}
```

#### Update Cart Item
- **URL:** `POST /cart/update`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
```json
{
    "product_id": 1,
    "quantity": 3
}
```
- **Note:** Set quantity to 0 to remove item

#### Clear Cart
- **URL:** `DELETE /cart/clear`
- **Headers:** `Authorization: Bearer <access_token>`

### Order Endpoints

#### Place Order
- **URL:** `POST /orders`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
```json
{
    "shipping_address": "123 Main St, City, State, ZIP",
    "phone_number": "1234567890"
}
```
- **Response:**
```json
{
    "id": 1,
    "user": 1,
    "user_name": "johndoe",
    "order_status": "pending",
    "total_amount": "179.98",
    "shipping_address": "123 Main St, City, State, ZIP",
    "phone_number": "1234567890",
    "items": [
        {
            "id": 1,
            "product": 1,
            "product_name": "Product Name",
            "quantity": 2,
            "price": "89.99",
            "subtotal": "179.98"
        }
    ],
    "created_at": "2025-12-11T10:00:00Z"
}
```

#### Get Order by ID
- **URL:** `GET /orders/<id>`
- **Headers:** `Authorization: Bearer <access_token>`

#### Get User Orders
- **URL:** `GET /orders/user/<user_id>`
- **Headers:** `Authorization: Bearer <access_token>`

#### Update Order Status (Admin Only)
- **URL:** `PUT /orders/<id>/status`
- **Headers:** `Authorization: Bearer <access_token>`
- **Body:**
```json
{
    "order_status": "packed"
}
```
- **Available statuses:** pending, confirmed, packed, shipped, out_for_delivery, delivered, cancelled

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/`

### Admin Capabilities:
- ✅ Manage users and permissions
- ✅ Create, edit, and delete products
- ✅ Manage product categories
- ✅ View and manage all orders
- ✅ Update order statuses
- ✅ View customer carts
- ✅ Monitor inventory and stock levels

## Testing the API

### Using cURL

```bash
# Sign up
curl -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'

# Login
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "testpass123"
  }'

# Get products (with token)
curl -X GET http://localhost:8000/products/ \
  -H "Authorization: Bearer <your_access_token>"
```

### Using Postman

1. Import the API endpoints into Postman
2. Set up environment variables:
   - `base_url`: http://localhost:8000
   - `access_token`: (obtained from login)
3. Use Bearer Token authentication for protected endpoints

## Database Models

### User Model
- Custom user model extending Django's AbstractUser
- Fields: username, email, password, first_name, last_name, phone_number, address

### Product Model
- name, description, category (FK), price, image_url, stock, discount
- Calculated fields: discounted_price, is_in_stock

### Category Model
- name, description

### Cart & CartItem Models
- Cart: One-to-one with User
- CartItem: Many-to-one with Cart, references Product

### Order & OrderItem Models
- Order: Belongs to User, contains status, total_amount, shipping info
- OrderItem: Snapshot of product at time of purchase

## Security Features

- ✅ JWT-based authentication
- ✅ Password hashing using Django's default PBKDF2
- ✅ CORS configuration for frontend integration
- ✅ Permission-based access control
- ✅ Admin-only endpoints for sensitive operations
- ✅ Input validation and sanitization

## Development Notes

- All API endpoints return JSON responses
- Pagination is enabled by default (10 items per page)
- Timestamps are stored in UTC
- Stock is automatically updated when orders are placed
- Cart is automatically cleared after successful order

## Deployment Considerations

For production deployment:

1. Set `DEBUG=False` in settings
2. Use PostgreSQL instead of SQLite
3. Configure proper SECRET_KEY
4. Set up static files serving (WhiteNoise or CDN)
5. Use environment variables for sensitive data
6. Enable HTTPS
7. Configure ALLOWED_HOSTS properly
8. Set up proper CORS origins

## Troubleshooting

### Common Issues:

**Import errors for rest_framework or simplejwt:**
```bash
pip install -r requirements.txt
```

**Migration errors:**
```bash
python manage.py makemigrations
python manage.py migrate
```

**Permission denied errors:**
- Ensure you're using the correct JWT token
- Check if the endpoint requires admin privileges


## Credits

Built with Django REST Framework for the Winkit E-Commerce platform.

## License

This project is for educational and assessment purposes.

---

**API Base URL:** `http://localhost:8000`
**Admin Panel:** `http://localhost:8000/admin/`

For questions or support, please contact the development team.
# winkit
