# E-commerce API

A production-grade RESTful API for a simple e-commerce platform built with Django REST Framework.

## Features

- Product management (CRUD operations)
- Order placement with stock validation
- Comprehensive test coverage
- Docker support
- PostgreSQL database

## Prerequisites

- Docker
- Docker Compose

## Installation

1. Clone the repository: 

```bash
git clone https://github.com/yourusername/ecommerce-api.git
cd ecommerce-api
```

2. Build and run the Docker container:

```bash
docker compose up --build
```


The API will be available at `http://localhost:8000/api/`

## API Endpoints

### Products

- `GET /api/products/` - List all products
- `POST /api/products/` - Create a new product
- `GET /api/products/{id}/` - Retrieve a product
- `PUT /api/products/{id}/` - Update a product
- `DELETE /api/products/{id}/` - Delete a product

### Orders

- `GET /api/orders/` - List all orders
- `POST /api/orders/` - Create a new order
- `GET /api/orders/{id}/` - Retrieve an order

## Testing

Run tests using pytest:

```bash
docker compose run web pytest
```