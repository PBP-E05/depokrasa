# Nama Proyek: DepokRasa

## Anggota Kelompok
- Muhammad Wendy Fyfo Anggara (2306223906)
- Laurentius Farel Arlana Mahardika (2306244892)
- Farrel Athalla Muljawan (2306223925)
- Joe Mathew Rusli (2306152310)
- Philip Halomoan Sampenta Manurung (2306240130)

## Deskripsi Aplikasi
Dengan nama "DepokRasa", aplikasi kami bertujuan untuk memberikan informasi tentang berbagai jenis makanan yang ditemukan di Kota Depok. Tujuan aplikasi ini adalah untuk membantu penduduk lokal dan turis yang datang ke Depok menemukan toko makanan tertentu yang mereka cari. Aplikasi ini dibuat karena banyak sekali orang di depok dan ingin mencari tempat makan yang bukan itu itu saja dan membuat orang ingin tahu tentang produk apa yang ada di sana. Dengan menggunakan aplikasi ini, pengguna dapat dengan mudah menemukan toko atau restoran di Depok yang menjual barang yang mereka butuhkan, membuatnya lebih mudah untuk melihat makanan.

## Modul yang Akan Diimplementasikan
1. [Authentication](#1-authentication-auth)
2. [User Dashboard](#2-user-dashboard)
3. [Menu Management](#3-menu-management)
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
- Food ratings and reviews

**Models:**
- Food
- Shop (one-to-many relationship with Food)

### 7. Admin Panel
- Utilizes Django Admin for backend management

### 8. Information on Promotions and Discounts
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