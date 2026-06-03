# CodingCamp Jobs Recommendation

Proyek ini adalah sistem rekomendasi pekerjaan. Repositori ini mencakup model *machine learning* (Jupyter Notebook) dan *backend* yang dibangun menggunakan Django.

## Prasyarat

Pastikan kamu sudah menginstal perangkat lunak berikut di sistemmu:
* [Python](https://www.python.org/downloads/) (Disarankan versi 3.8 atau lebih baru)
* [Miniconda](https://docs.conda.io/en/latest/miniconda.html) atau [Anaconda](https://www.anaconda.com/) (Opsional, jika ingin menggunakan Conda)

---

## 1. Instalasi dan Persiapan Lingkungan (Environment Setup)

Sangat disarankan untuk menggunakan *virtual environment* guna menghindari konflik versi library antar proyek. Kamu bisa memilih salah satu cara di bawah ini: menggunakan `venv` atau `Conda`.

### Opsi A: Menggunakan `venv` (Python Bawaan)

1. Buka terminal dan arahkan ke direktori proyek ini.
2. Buat virtual environment bernama `env`:
   ```bash
   python -m venv env
   Aktifkan virtual environment:

Windows:

```bash
env\Scripts\activate
```

macOS / Linux:

```bash
source env/bin/activate
```  

Instal semua dependensi yang dibutuhkan (pastikan kamu memiliki file requirements.txt):

```bash
pip install -r requirements.txt
```

### Opsi B: Menggunakan Conda
Buka terminal/Anaconda Prompt.

Buat environment baru bernama codingcamp_env (bisa disesuaikan):

```bash
conda create -n codingcamp_env python=3.10
``` 

Aktifkan environment tersebut:

```bash
conda activate codingcamp_env
``` 

Instal dependensi:

```bash
pip install -r requirements.txt
```

## 2. Menjalankan Jupyter Notebook (Modeling)
File permodelan machine learning berada di file modeling_case_3.ipynb. Untuk membukanya dan mencoba menjalankannya:

Pastikan virtual environment kamu masih aktif.

Instal Jupyter Notebook (jika belum terinstal di dalam environment):

```bash
pip install jupyter
```

Jalankan server Jupyter:

```bash
jupyter notebook
```

Browser akan otomatis terbuka. Navigasikan ke file modeling_case_3.ipynb dan klik untuk membukanya.

Kamu bisa menjalankan setiap baris kode (Cell) dengan menekan Shift + Enter.

## 3. Menjalankan Backend Django
Proyek ini menggunakan framework Django untuk API/Backend yang berada di dalam folder ./backend_django.

Ikuti langkah berikut untuk menjalankan server secara lokal:

Pastikan virtual environment (venv/conda) dalam keadaan aktif.

Masuk ke direktori backend:

```bash
cd backend_django
```

(Opsional, tapi disarankan) Jalankan migrasi database terlebih dahulu jika ada perubahan model:

```bash
python manage.py makemigrations
python manage.py migrate
``` 

Jalankan development server:

```bash
python manage.py runserver
```

Server backend akan berjalan secara default di http://127.0.0.1:8000/. Kamu bisa mengakses endpoint API melalui alamat tersebut.

Struktur Direktori (Singkat)
Plaintext
.
├── backend_django/        # Kode sumber (Source code) untuk backend Django
├── modeling_case_3.ipynb  # Jupyter notebook untuk eksplorasi dan pemodelan data
├── requirements.txt       # Daftar library dan dependensi proyek (Opsional)
└── README.md              # Dokumentasi proyek ini
