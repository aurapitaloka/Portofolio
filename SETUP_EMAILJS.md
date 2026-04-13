# Setup EmailJS untuk Form Kontak

## Cara Setup EmailJS (Gratis)

### 1. Daftar di EmailJS
- Kunjungi: https://www.emailjs.com
- Klik "Sign Up" dan buat akun gratis
- Verifikasi email Anda

### 2. Buat Email Service
- Setelah login, klik "Add New Service"
- Pilih provider email Anda (Gmail, Outlook, dll)
- Ikuti instruksi untuk menghubungkan email Anda
- Catat **Service ID** yang diberikan

### 3. Buat Email Template
- Klik "Email Templates" → "Create New Template"
- Buat template dengan variabel:
  ```
  From: {{from_name}} ({{from_email}})
  Subject: Pesan dari Portfolio Website
  
  Pesan:
  {{message}}
  ```
- Catat **Template ID** yang diberikan

### 4. Dapatkan Public Key
- Klik "Account" → "General"
- Salin **Public Key** Anda

### 5. Install EmailJS SDK
Jalankan di terminal:
```bash
npm install @emailjs/browser
```

### 6. Update main.js
Buka `src/main.js` dan uncomment bagian EmailJS, lalu isi dengan:
- `YOUR_SERVICE_ID` → Service ID Anda
- `YOUR_TEMPLATE_ID` → Template ID Anda  
- `YOUR_PUBLIC_KEY` → Public Key Anda

### 7. Import EmailJS di main.js
Tambahkan di bagian atas file:
```javascript
import emailjs from '@emailjs/browser';

// Initialize EmailJS
emailjs.init('YOUR_PUBLIC_KEY');
```

## Alternatif: Formspree (Lebih Mudah)

Jika EmailJS terlalu rumit, gunakan Formspree:

1. Kunjungi: https://formspree.io
2. Daftar gratis
3. Buat form baru
4. Dapatkan endpoint URL (contoh: `https://formspree.io/f/xxxxx`)
5. Update form di `index.html`:
   ```html
   <form action="https://formspree.io/f/xxxxx" method="POST">
   ```

## Catatan
- Data form saat ini disimpan di **localStorage** browser (untuk testing)
- Untuk melihat pesan yang masuk, buka Developer Tools → Application → Local Storage
- Setelah setup EmailJS, pesan akan langsung masuk ke email Anda

