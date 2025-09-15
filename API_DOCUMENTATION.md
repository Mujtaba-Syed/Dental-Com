# DentalCom API Documentation

## Overview
This API provides endpoints for managing dental products and their images using Django REST Framework with pagination support.

## Base URL
```
http://localhost:8000/api/
```

## Authentication
Currently set to `AllowAny` for development. In production, you should implement proper authentication.

## Endpoints

### Products

#### 1. List All Products
- **URL**: `/api/products/`
- **Method**: `GET`
- **Description**: Get a paginated list of all active products
- **Query Parameters**:
  - `page`: Page number (default: 1)
  - `page_size`: Items per page (default: 10, max: 100)
  - `category`: Filter by category (orthodontics, cosmetic, preventive, restorative, oral_surgery)
  - `search`: Search in name and description
  - `ordering`: Order by field (name, price, created_at)
- **Response**: Paginated list of products with primary image

#### 2. Create Product
- **URL**: `/api/products/`
- **Method**: `POST`
- **Description**: Create a new product
- **Body**:
```json
{
  "name": "Product Name",
  "description": "Product description",
  "price": 100.00,
  "category": "orthodontics",
  "is_active": true,
  "images": [
    {
      "image": "file_upload",
      "alt_text": "Image description",
      "is_primary": true
    }
  ]
}
```

#### 3. Get Product Detail
- **URL**: `/api/products/{id}/`
- **Method**: `GET`
- **Description**: Get detailed information about a specific product including all images

#### 4. Update Product
- **URL**: `/api/products/{id}/`
- **Method**: `PUT` or `PATCH`
- **Description**: Update product information

#### 5. Delete Product
- **URL**: `/api/products/{id}/`
- **Method**: `DELETE`
- **Description**: Delete a product

#### 6. Get Products by Category
- **URL**: `/api/products/category/{category}/`
- **Method**: `GET`
- **Description**: Get products filtered by category
- **Categories**: orthodontics, cosmetic, preventive, restorative, oral_surgery

#### 7. Search Products
- **URL**: `/api/products/search/`
- **Method**: `GET`
- **Description**: Search products by name or description
- **Query Parameters**:
  - `q`: Search query

#### 8. Product Statistics
- **URL**: `/api/products/stats/`
- **Method**: `GET`
- **Description**: Get product statistics

### Product Images

#### 1. List Product Images
- **URL**: `/api/products/{product_id}/images/`
- **Method**: `GET`
- **Description**: Get all images for a specific product

#### 2. Add Product Image
- **URL**: `/api/products/{product_id}/images/`
- **Method**: `POST`
- **Description**: Add a new image to a product
- **Body**:
```json
{
  "image": "file_upload",
  "alt_text": "Image description",
  "is_primary": false
}
```

#### 3. Get Image Detail
- **URL**: `/api/products/{product_id}/images/{image_id}/`
- **Method**: `GET`
- **Description**: Get specific image details

#### 4. Update Image
- **URL**: `/api/products/{product_id}/images/{image_id}/`
- **Method**: `PUT` or `PATCH`
- **Description**: Update image information

#### 5. Delete Image
- **URL**: `/api/products/{product_id}/images/{image_id}/`
- **Method**: `DELETE`
- **Description**: Delete an image

## Response Format

### Product List Response
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "name": "Traditional Braces",
      "slug": "traditional-braces",
      "price": "85.00",
      "category": "orthodontics",
      "is_active": true,
      "created_at": "2025-01-27T10:00:00Z",
      "primary_image": {
        "id": 1,
        "image": "/media/products/braces.jpg",
        "alt_text": "Traditional metal braces"
      }
    }
  ]
}
```

### Product Detail Response
```json
{
  "id": 1,
  "name": "Traditional Braces",
  "slug": "traditional-braces",
  "description": "Traditional metal braces for teeth straightening...",
  "price": "85.00",
  "category": "orthodontics",
  "is_active": true,
  "created_at": "2025-01-27T10:00:00Z",
  "updated_at": "2025-01-27T10:00:00Z",
  "images": [
    {
      "id": 1,
      "image": "/media/products/braces.jpg",
      "alt_text": "Traditional metal braces",
      "is_primary": true,
      "created_at": "2025-01-27T10:00:00Z"
    }
  ],
  "primary_image": {
    "id": 1,
    "image": "/media/products/braces.jpg",
    "alt_text": "Traditional metal braces",
    "is_primary": true,
    "created_at": "2025-01-27T10:00:00Z"
  }
}
```

## Features

### Pagination
- Default page size: 10 items
- Maximum page size: 100 items
- Configurable via `page_size` parameter

### Filtering
- Filter by category
- Filter by active status
- Search by name and description

### Ordering
- Order by name, price, or creation date
- Default ordering: newest first

### Image Management
- Multiple images per product
- Primary image designation
- Automatic primary image management

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run migrations:
```bash
python manage.py makemigrations
python manage.py migrate
```

3. Create sample data:
```bash
python manage.py create_sample_products
```

4. Start the server:
```bash
python manage.py runserver
```

5. Access the API:
- API Root: http://localhost:8000/api/
- Admin Interface: http://localhost:8000/admin/
- Browsable API: http://localhost:8000/api/products/

## Models

### Product
- `name`: Product name
- `slug`: URL-friendly identifier
- `description`: Detailed description
- `price`: Decimal price
- `category`: Choice field with dental categories
- `is_active`: Boolean for product status
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### ProductImage
- `product`: Foreign key to Product
- `image`: Image file
- `alt_text`: Alternative text for accessibility
- `is_primary`: Boolean for primary image
- `created_at`: Creation timestamp
