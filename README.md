# 🎧 EchoHide - Audio Steganography using FFT

**EchoHide** adalah aplikasi berbasis web yang memungkinkan Anda menyembunyikan dan mengekstrak pesan teks dari/ke file audio `.wav` menggunakan teknik steganografi berbasis **Fast Fourier Transform (FFT)**. Aplikasi ini dibangun dengan **Streamlit**, dan cocok untuk eksperimen atau proyek edukasi terkait audio processing dan keamanan data.

---

## 📌 Fitur Utama

- 🔒 Menyisipkan pesan ke dalam file audio `.wav`
- 🧠 Mengekstrak pesan dari audio steganografi
- 📊 Visualisasi bentuk gelombang (waveform) & spektrum frekuensi
- 🎛️ Pengaturan kekuatan embed (alpha)
- 🎧 Pemutar audio langsung di aplikasi
- 💾 Fitur unduh audio hasil embed

---

### 1. 📥 Clone Repositori

```bash
git clone https://github.com/rhenaald/Steganography.git
cd echohide
```

### 2. 📦 Instalasi Dependensi

Pastikan Python sudah terpasang, lalu:

```bash
pip install -r requirements.txt
```

Atau secara manual:

```bash
pip install streamlit numpy scipy matplotlib
```

### 3. 🚀 Jalankan Aplikasi

```bash
streamlit run app.py
```

---

## 🛠️ Penjelasan Fungsionalitas

### 🔸 Penyisipan Pesan (Steganografi)
- Audio diubah menjadi mono jika stereo.
- Pesan dikonversi ke biner (8 bit per karakter).
- Transformasi Fourier dilakukan (FFT).
- Magnitude spektrum diubah sedikit berdasarkan bit pesan (`+alpha` untuk bit 1, `-alpha` untuk bit 0).
- Data audio dikembalikan ke domain waktu dengan iFFT.

### 🔸 Ekstraksi Pesan
- FFT dilakukan pada audio stego & original.
- Selisih magnitude dianalisis untuk menebak bit.
- Bit dikumpulkan dan dikonversi ke karakter ASCII.

---

## 🎨 Tampilan Visualisasi
- **Waveform** menampilkan bentuk gelombang waktu.
- **Spektrum** menunjukkan distribusi frekuensi (log scale).

---

## ⚠️ Batasan & Catatan

- Tidak disarankan untuk menyembunyikan informasi sensitif.
- Disarankan hanya untuk eksperimen dan edukasi.
- Kompatibel dengan file `.wav` saja.

---

## 🙋 Kontribusi

Pull request terbuka! Jika kamu punya ide peningkatan fitur atau perbaikan bug, langsung saja fork dan kembangkan. Jangan lupa ⭐ repo ini kalau kamu suka ya!

---