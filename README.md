# To-Do List API (FastAPI Standard Mini Project)

Proyek ini adalah sebuah web API sederhana untuk mengelola daftar tugas harian (*To-Do List*) yang dibangun menggunakan **FastAPI**. Proyek ini dibuat sebagai media pembelajaran untuk memahami implementasi RESTful API dengan operasi CRUD lengkap menggunakan standar FastAPI modern.

## 🚀 Fitur Utama (CRUD)
* **GET `/todos`** : Mengambil semua daftar tugas.
* **GET `/todos/{id}`** : Mengambil detail satu tugas spesifik berdasarkan ID.
* **POST `/todos`** : Menambahkan tugas baru dengan validasi data (Pydantic).
* **PUT `/todos/{id}`** : Memperbarui seluruh data tugas secara total.
* **PATCH `/todos/{id}`** : Memperbarui sebagian data tugas (misal: mengubah status selesai saja).
* **DELETE `/todos/{id}`** : Menghapus tugas dari daftar berdasarkan ID.

---

## 🛠️ Cara Instalasi dan Menjalankan Proyek

Ikuti langkah-langkah di bawah ini untuk menjalankan proyek ini di komputer lokal Anda:

### 1. Kloning atau Buat Folder Proyek
Pastikan Anda berada di dalam direktori proyek:
```bash
cd todo_list_api

```

### 2. Membuat dan Mengaktifkan Virtual Environment

Gunakan *virtual environment* agar pustaka (*library*) proyek terisolasi dengan aman.

* **Windows:**
```bash
python -m venv venv
.\venv\Scripts\activate

```


* **Linux / macOS:**
```bash
python3 -m venv venv
source venv/bin/activate

```



### 3. Menginstal Dependensi

Instal FastAPI versi terbaru yang sudah mencakup server Uvicorn dan FastAPI CLI:

```bash
pip install fastapi

```

### 4. Menjalankan Server Aplikasi

Jalankan aplikasi menggunakan mode pengembangan (*development mode*):

```bash
fastapi dev main.py

```

Setelah server berhasil menyala, aplikasi Anda akan berjalan di alamat `http://127.0.0.1:8000`.

---

## 📑 Dokumentasi API Interaktif (Swagger UI)

FastAPI secara otomatis menyediakan dokumentasi interaktif yang bisa langsung digunakan untuk menguji seluruh fungsi API tanpa memerlukan aplikasi tambahan seperti Postman.

Setelah server menyala, buka peramban (*browser*) Anda dan akses:
👉 **[http://127.0.0.1:8000/docs](https://www.google.com/search?q=http://127.0.0.1:8000/docs)**

---

## 📂 Struktur Data Proyek (In-Memory)

Untuk mempermudah pembelajaran tanpa konfigurasi basis data yang rumit, proyek ini menggunakan memori sementara (*In-Memory Database*) berbasis *List of Dictionary* di Python dengan struktur data sebagai berikut:

* `id` (Integer, Unik)
* `task` (String)
* `priority` (String: *High/Medium/Low*)
* `is_completed` (Boolean, Default: *False*)
