# IyanTools

## Preview

![Preview IyanTools](https://raw.githubusercontent.com/IyanzNotDev/IyanTools-V2.1/main/Screenshot_20260922_130905_ZeroTermux.png)

## Fitur

| No | Fitur | Kegunaan |
|----|-------|----------|
| 1 | Cari Sekolah (Nama) | Cari data sekolah berdasarkan nama |
| 2 | Cari Sekolah (NPSN) | Cari data sekolah berdasarkan NPSN |
| 3 | Cek NIK | Urai struktur NIK (provinsi, tanggal lahir, jenis kelamin) — 100% lokal, tanpa internet |
| 4 | IP Lookup | Cek info geolokasi/ISP dari sebuah IP atau domain |
| 5 | Stalker TikTok | Lihat info publik sebuah akun TikTok |
| 6 | Stalker GitHub | Lihat info publik sebuah akun GitHub |
| 7 | Generate Password | Bikin varian password yang lebih kuat dari password kamu — diproses lokal, tidak dikirim ke internet |
| 8 | Hash Testing | Cocokkan hash dengan wordlist (dictionary attack) — buat testing hash/password milik sendiri |
| 9 | Scrape Website | Ambil info publik dari sebuah halaman web (kontak, link, dugaan API endpoint) |
| 10 | Cek Kebocoran Email | Cek apakah email pernah muncul di data breach publik |
| 11 | Cek Kebocoran Password | Cek apakah password pernah bocor di database publik — aman secara privasi (cuma sebagian hash yang dikirim) |

## Instalasi (Termux)

```bash
# 1. Update paket & install Python
pkg update -y && pkg upgrade -y
pkg install python -y

# 2. Clone repo
git clone https://github.com/IyanzNotDev/IyanTools-V2.1.git
cd IyanTools-V2.1

# 3. (Opsional) install pemutar musik biar musik latar jalan
pkg install mpv -y

# 4. Jalankan
python iyantools.py
```

> Musik latar butuh salah satu dari `termux-media-player` (paket `termux-api` + app Termux:API), `mpv`, `ffplay`, `mpg123`, atau `cvlc`. Kalau tidak ada satupun terpasang, aplikasi tetap jalan normal tanpa musik.

## Catatan

Semua fitur di sini cuma membaca data publik atau memproses sesuatu secara lokal di HP — tidak ada fitur bypass login, serang akun, atau ambil data pribadi dari database ilegal manapun. Dipakai untuk edukasi, testing punya sendiri, dan keperluan OSIN
T yang wajar.
