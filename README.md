# Portfolio Website dengan Tailwind CSS

## 📋 Penjelasan Singkat

Proyek ini menggunakan:
- **Vite** - Build tool yang cepat untuk development
- **Tailwind CSS** - Framework CSS utility-first untuk styling
- **PostCSS** - Tool untuk memproses CSS

## 🚀 Cara Menjalankan Website

### 1. Install Dependencies (jika belum)
```bash
npm install
```

### 2. Jalankan Development Server
```bash
npm run dev
```

Setelah menjalankan perintah di atas, Vite akan memberikan URL seperti:
```
➜  Local:   http://localhost:5173/
```

**Buka URL tersebut di browser Anda!** 

### 3. Build untuk Production
```bash
npm run build
```

### 4. Preview Build Production
```bash
npm run preview
```

## 📝 Catatan Penting

### ❌ JANGAN langsung buka `index.html` di browser!

**Kenapa?**
- Website ini menggunakan **Vite** sebagai development server
- Tailwind CSS perlu diproses terlebih dahulu oleh Vite
- Jika langsung buka `index.html`, Tailwind CSS tidak akan berfungsi dengan baik

### ✅ Cara yang Benar:
1. Jalankan `npm run dev` di terminal
2. Buka URL yang diberikan (biasanya `http://localhost:5173/`)
3. Website akan otomatis reload ketika Anda mengubah file

## 🎨 Cara Menggunakan Tailwind CSS

Tailwind CSS sudah dikonfigurasi! Anda bisa langsung menggunakan class Tailwind di HTML:

```html
<div class="bg-primary text-white p-4 rounded-lg">
  Hello World
</div>
```

### Contoh Class Tailwind:
- `bg-primary` - Background warna primary (teal)
- `text-white` - Warna text putih
- `p-4` - Padding 4
- `rounded-lg` - Border radius besar
- `flex` - Display flex
- `container` - Container dengan max-width

## 📁 Struktur Folder

```
portofolio-saya/
├── index.html          # File HTML utama
├── src/
│   ├── input.css       # File CSS input untuk Tailwind
│   └── main.js         # JavaScript utama
├── dist/               # Folder output (hasil build)
│   └── output.css      # CSS yang sudah diproses
├── tailwind.config.js  # Konfigurasi Tailwind
└── package.json        # Dependencies dan scripts
```

## 🔧 Scripts yang Tersedia

- `npm run dev` - Jalankan development server
- `npm run build` - Build untuk production
- `npm run preview` - Preview hasil build

## 💡 Tips

1. **Development**: Selalu gunakan `npm run dev` saat development
2. **Hot Reload**: Perubahan file akan otomatis terlihat di browser
3. **Tailwind**: Gunakan class Tailwind langsung di HTML, tidak perlu menulis CSS manual
4. **Custom Color**: Warna primary sudah dikonfigurasi di `tailwind.config.js`

