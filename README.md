# Web-Cam-Meme
## Features

- **Real-Time Gesture Recognition**: Deteksi gesture tangan dan wajah presisi menggunakan MediaPipe.
- **Dynamic Meme Overlay**: Menampilkan stiker meme secara otomatis di layar sesuai gesture yang terdeteksi.
- **Virtual Camera Output**: Terintegrasi langsung dengan OBS Virtual Camera untuk digunakan di Zoom, Google Meet, MS Teams, dll.
- **Local Live Preview**: Jendela preview interaktif menggunakan OpenCV.

## Supported Gestures & Memes

1. **Call Sign + Tongue Out** (`🤙` + melet) -> Meme Plenger Cat
2. **Heart Hands** (Dua tangan membentuk hati) -> Meme Love Sign
3. **Index Near Head** (Telunjuk di samping kepala) -> Meme Nerd Pose
4. **Shh Pose** (Telunjuk di depan bibir) -> Meme Kaget
5. **Hold Head** (Dua tangan memegang kepala) -> Meme Sigma Amba
6. **OK Sign** (Jari membentuk huruf O) -> Meme Indian Men

## Prerequisites

- **Python 3.11.x**
- **OBS Studio** (Diperlukan untuk driver OBS Virtual Camera)

## Installation

1. **Clone Repositori**
   ```bash
   git clone https://github.com/porvyyn/Web-Cam-Meme.git
   cd webcam-zoom
   
## Buat & Aktifkan Virtual Environment

1. **Windows (PowerShell):**
    ```PowerShell
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    Windows (CMD):
    ```
    ```
    DOS
    python -m venv .venv
    .\.venv\Scripts\activate.bat
    Install Dependencies
    ```
    ```
    Bash
    pip install "opencv-python<4.10.0" "mediapipe==0.10.14" "numpy<2.0.0" pyvirtualcam
    Persiapan OBS Virtual Camera
    ```
- ***Unduh dan pasang OBS Studio.***

- ***Buka OBS Studio sekali, ikuti Auto-Configuration Wizard dan pilih opsi I will only be using the virtual camera.***

- ***Tutup OBS Studio.***

## Folder Structure

```Plaintext
webcam-zoom/
├── assets/
│   ├── plenger-cat.jpg
│   ├── love-sign.jpg
│   ├── nerd-pose.jpg
│   ├── kaget.jpg
│   ├── sigma-amba.jpg
│   └── indian-men.jpg
├── app.py
├── README.md
└── .gitignore
```


## How to Run
1. ***Pastikan webcam tidak sedang digunakan oleh aplikasi lain.***

2. ***Jalankan skrip utama:***

```Bash
python app.py
```
3. ***Buka Zoom atau Google Meet.***

4. ***Masuk ke pengaturan Video dan ganti input kamera ke OBS Virtual Camera.***

5. ***Tekan tombol q pada jendela preview OpenCV untuk menghentikan program.***

## Troubleshooting
- ***Error NormalizedLandmarkList: Pastikan akses data landmark menggunakan properti .landmark.***

- ***OBS Virtual Camera device not found: Pastikan OBS Studio sudah pernah dibuka sekali agar driver terdaftar di Windows.***
