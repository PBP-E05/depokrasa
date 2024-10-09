# Nama Proyek: DepokRasa

## Anggota Kelompok
- Muhammad Wendy Fyfo Anggara (2306223906)
- Laurentius Farel Arlana Mahardika (2306244892)
- Farrel Athalla Muljawan (2306223925)
- Joe Mathew Rusli (2306152310)
- Philip Halomoan Sampenta Manurung (2306240130)

## Deskripsi Aplikasi
Sebagai mahasiswa di Universitas Indonesia, kami semua memiliki satu masalah yang sama, yaitu menu makanan yang itu-itu saja. Di kota Depok yang besar ini kami kebingunngan dalam memilih makanan yang akan kami makan dan tempat untuk mendapatkannya. Sehingga, kami muncul dengan ide untuk menciptakan DepokRasa. 

DepokRasa adalah aplikasi yang bertujuan untuk memberikan informasi tentang berbagai jenis makanan atau minuman yang ditemukan di Kota Depok. Tujuan aplikasi ini adalah untuk membantu penduduk lokal dan turis yang datang ke Depok menemukan toko makanan atau minuman tertentu yang mereka cari. Dengan menggunakan aplikasi ini, pengguna dapat dengan mudah menemukan toko atau restoran di Depok yang menjual makanan atau minuman yang beragam, sehingga pengguna dapat menyicipi keberagaman rasa yang ada di Depok.

## Modul yang Akan Diimplementasikan
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

## Sumber Dataset Awal

## Peran Pengguna
1. **Pengguna Umum**: Pengguna yang dapat menelusuri produk makanan, menambahkan makanan ke keranjang, menandai favorit, dan memberikan ulasan serta peringkat.
   - **Fitur Utama**: Registrasi, login/logout, melihat menu, membuat wishlist, mengelola keranjang belanja, melakukan checkout, dan melihat riwayat pesanan.
   - **Views**: Halaman dashboard pengguna, halaman profil, halaman riwayat pesanan, halaman wishlist.

2. **Penjual**: Pengguna yang dapat menambahkan produk makanan ke platform, mengelola daftar produk, dan mengelola pesanan yang diterima.
   - **Fitur Utama**: Menambah, mengedit, dan menghapus makanan; mengelola kategori makanan; memproses pesanan yang diterima.
   - **Views**: Halaman manajemen menu, halaman pesanan penjual.

3. **Admin**: Administrator yang dapat mengelola pengguna, memoderasi daftar produk, dan memastikan kelancaran operasi platform.
   - **Fitur Utama**: Mengelola pengguna, melihat dan mengelola pesanan, memoderasi konten.
   - **Views**: Admin Panel (menggunakan Django Admin).

4. **Kurir**: Pengguna yang dapat melihat detail pengiriman dan mengelola status pengiriman pesanan.
   - **Fitur Utama**: Melacak status pengiriman, mengelola opsi pengiriman.
   - **Views**: Halaman pelacakan pengiriman, halaman status pengiriman.

## Tautan Deployment
Aplikasi ini dapat diakses di: 
