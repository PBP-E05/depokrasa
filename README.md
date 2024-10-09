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

### Manfaat
- Temukan kuliner baru
   - DepokRasa memudahkan pengguna untuk menemukan berbagai macam kuliner baru dan unik di Depok.
- Cari makanan berdasarkan kategori
   - Pengguna dapat mencari kuliner berdasarkan kategori yang disediakan. Memudahkan pengguna mencari makanan yang mereka mau.
- Temukan rekomendasi kuliner
   - Pengguna dapat menemukan kuliner favorit di Depok dengan menggunakan review dan artikel dalam DepokRasa.


## Modul yang Akan Diimplementasikan
1. [Authentication (auth) and User Management](#1-authentication-auth-and-user-management)
2. [Menu Management](#3-menu-management)
3. [Information on Promotions and Discounts](#5-information-on-promotions-and-discounts)
4. [Blog/Articles](#6-blogarticles)
5. [Feedback and Support](#7-feedback-and-support)

### 1. Authentication (auth) and User Management
**Features:**
- Food wishlist
- User registration (sign up)
- Login and logout functionality

**Views:**
- Dashboard page
- Order details page

### 2. Menu Management
**Features:**
- Food item listing (CRUD operations)
- Food ratings and reviews

**Models:**
- Food
- Shop (one-to-many relationship with Food)

### 3. Information on Promotions and Discounts
**Features:**
- Promo codes
- Category-specific discounts

**Models:**
- Promotion
- Discount

### 4. Blog/Articles
**Features:**
- Articles about Depok's culinary scene
- Food tips and recommendations

**Model:**
- Article

### 5. Feedback and Support
**Features:**
- Feedback form
- FAQ section

**Model:**
- Feedback

## Sumber Dataset Awal
1. [Link Google Spreadsheet](https://docs.google.com/spreadsheets/d/1kX3j5mdDwOSw6WzYEg5S7Ls4GGcUpeF5ypGo_OaXc88/edit?hl=id&gid=0#gid=0)
2. [Gofood Daerah Depok](https://gofood.co.id/jakarta/depok-restaurants)
3. [PergiKuliner.com Daerah Depok](https://pergikuliner.com/restoran/depok/)

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
Aplikasi ini dapat diakses di: [DepokRasa](http://muhammad-wendy-depokrasa.pbp.cs.ui.ac.id/)