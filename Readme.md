# OCR Auto Typer

OCR Auto Typer adalah aplikasi desktop yang menggunakan OCR untuk membaca teks dari area layar yang dipilih dan mengetikkannya secara otomatis menggunakan PyAutoGUI.

## Fitur Utama

- Select Area
- Start
- Stop
- OCR Text Detection
- Auto Typing
- OCR Monitoring
- Anti Double Typing

## Alur Sistem

Select Area
↓
Start
↓
OCR membaca teks
↓
Pilih area tempat mengetik
↓
Auto Typing
↓
OCR terus memantau perubahan teks
↓
Stop

## Cara Penggunaan

1. Jalankan aplikasi.
2. Klik **Select Area**.
3. Pilih area layar yang ingin dibaca oleh OCR.
4. Klik **Start**.
5. Saat jeda setelah Start, klik area tempat teks akan diketik.
6. Hasil OCR akan otomatis diketik.
7. Jika teks berubah, teks baru akan otomatis diketik.
8. Jika teks tidak berubah, teks tidak akan diketik ulang.
9. Klik **Stop** untuk menghentikan proses.

## Teknologi

- Python
- PySide6
- OCR
- PyAutoGUI
- QTimer

## Status Project

Step 5.5 — Selesai ✅

Project masih dalam tahap pengembangan.

## Catatan

Versi saat ini ditujukan untuk penggunaan pribadi dan pengujian.