# Panduan Penggunaan Portofolio Dinamis (Flask + MySQL)

Aplikasi portofolio Anda kini telah berhasil dirombak menjadi web dinamis dengan sistem manajemen konten (**CMS Admin**) berbasis **Flask** dan database **MySQL** (`porto`).

---

## 🚀 Cara Menjalankan Aplikasi

1. **Pastikan MySQL XAMPP Aktif:**
   - Buka XAMPP Control Panel dan pastikan modul **MySQL** & **Apache** dalam status **Running**.
   - Database yang digunakan adalah `porto` (Port 3306, user `root`, password kosong).

2. **Jalankan Server Flask:**
   Buka terminal di folder project ini:
   ```bash
   python app.py
   ```
   Server akan berjalan di:
   - **Website Publik:** `http://127.0.0.1:5000`
   - **Panel Admin CMS:** `http://127.0.0.1:5000/admin/login`

---

## 🔐 Kredensial Administrator Default

- **URL Login:** `http://127.0.0.1:5000/admin/login`
- **Username:** `admin`
- **Password:** `admin123`
*(Anda dapat mengubah username dan password kapan saja di menu **Pengaturan Akun** pada panel admin)*.

---

## 🛠️ Fitur & Kontrol Penuh dari Admin Dashboard

Semua teks, foto, berkas, dan kartu yang tampil di frontend kini 100% dapat diubah dari backend tanpa menyentuh kode HTML:

1. **Profil & Identitas Diri (`/admin/profile`):**
   - Inisial brand logo navbar (`AP`)
   - Badge sambutan (`👋 Halo, Saya`) & Status ketersediaan (`Open to Work & Internship`)
   - Nama lengkap, profesi utama, dan spesialisasi/sub-judul
   - Paragraf narasi bio di Hero Section
   - **Upload Foto Profil Baru** (otomatis update ke website)
   - **Upload Berkas CV PDF Baru** (tombol download CV di frontend otomatis mengambil file terbaru)
   - Teks bagian *Tentang Saya* (Judul, Subjudul, Paragraf 1 & 2)
   - Informasi Kontak (Email, WhatsApp/No. HP, Domisili, URL GitHub, LinkedIn, Instagram, dan Teks Hak Cipta Footer)
   - **Kartu Kelebihan Diri (Highlights):** Tambah/hapus kartu seperti Komunikasi, Teamwork, Adaptif, dll.

2. **Skills & Teknologi (`/admin/skills`):**
   - Tambah, edit, dan hapus keahlian/tools.
   - Kategori skill (Frontend, Backend, Testing & QA, Database, Mobile, UI/UX, dll.).
   - Pengaturan persentase kemahiran (slider 1-100%) dan icon FontAwesome / Devicon SVG.

3. **Projek Portofolio (`/admin/projects`):**
   - Tambah, edit, dan hapus projek portofolio.
   - Unggah gambar cover projek (rasio 16:9).
   - Fitur **Projek Unggulan (Featured)** untuk menampilkan kartu projek berukuran besar.
   - Tag tech stack (dipisahkan koma).
   - Tautan repositori GitHub dan link Live Website.
   - **Lampiran Dokumen QA (PDF):** Khusus projek pengujian seperti Senja App, Anda dapat mengunggah berkas PRD, Test Plan, Test Design, dan Laporan QA (ISO/IEC 25010).

4. **Pengalaman & Organisasi (`/admin/experiences`):**
   - Kelola riwayat Magang, Kepengurusan Organisasi, atau Pekerjaan.
   - Nama instansi/perusahaan, role/posisi, periode waktu, deskripsi tanggung jawab, dan tag keterampilan.

5. **Sertifikasi & Prestasi (`/admin/certificates`):**
   - Unggah sertifikat (Magang, Juara Lomba, Pelatihan/Course).
   - Pratinjau gambar sertifikat tajam dengan fitur **Popup Lightbox** (pengunjung dapat mengklik untuk melihat sertifikat ukuran penuh tanpa pindah halaman).
   - Tautan verifikasi kredensial online.

6. **Pesan Masuk / Inbox (`/admin/messages`):**
   - Pesan yang dikirimkan oleh pengunjung melalui formulir kontak publik akan otomatis tersimpan ke database MySQL.
   - Admin dapat membaca isi pesan, menandai sudah/belum dibaca, membalas langsung ke email pengirim, atau menghapus pesan.

7. **Pengaturan Akun (`/admin/account`):**
   - Mengubah username dan memperbarui kata sandi admin dengan aman (password di-hash menggunakan standar industri).
