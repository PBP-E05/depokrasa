# DepokRasa

DepokRasa is a comprehensive food ordering and delivery platform showcasing the culinary delights of Depok. This README provides an overview of the project's modules and features.

## Table of Contents

## Core Modules
1. [Authentication](#1-authentication-auth)
2. [User Dashboard](#2-user-dashboard)
3. [Menu Management](#3-menu-management)
4. [Shopping Cart](#4-shopping-cart)
5. [Order Management](#5-order-management)
6. [Delivery Management](#6-delivery-management)
7. [Admin Panel](#7-admin-panel)
8. [Optional Features](#optional-features)

### 1. Authentication (auth)
- User registration (sign up)
- Login and logout functionality
- User profile management

### 2. User Dashboard
**Features:**
- Order summary
- Order history
- Profile management (edit profile, change password)
- Food wishlist

**Views:**
- Dashboard page
- Order details page

### 3. Menu Management
**Features:**
- Food item listing (CRUD operations)
- Food categories (e.g., main courses, beverages, desserts)
- Food ratings and reviews

**Models:**
- Food
- Category (one-to-many relationship with Food)

### 4. Shopping Cart
**Features:**
- Add food items to cart
- Update quantity of items in cart
- Remove items from cart

**Views:**
- Shopping cart page
- Checkout process

### 5. Order Management
**Features:**
- Order processing
- Payment handling
- Order confirmation (optional: via email)

**Models:**
- Order
- OrderDetail

### 6. Delivery Management
**Features:**
- Delivery options (e.g., pickup, delivery)
- Order status tracking

### 7. Admin Panel
- Utilizes Django Admin for backend management

## Optional Features

### 8. Promotions and Discounts
**Features:**
- Promo codes
- Category-specific discounts

**Models:**
- Promotion
- Discount

### 9. Blog/Articles
**Features:**
- Articles about Depok's culinary scene
- Food tips and recommendations

**Model:**
- Article

### 10. Feedback and Support
**Features:**
- Feedback form
- FAQ section

**Model:**
- Feedback