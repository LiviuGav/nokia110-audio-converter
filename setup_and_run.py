import os
import subprocess
import sys
import urllib.request
import zipfile

FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
FFMPEG_FOLDER = "ffmpeg_temp"

def is_ffmpeg_installed():
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def download_ffmpeg():
    print("ffmpeg nu este instalat. Se descarcă acum...")
    zip_path = "ffmpeg.zip"
    urllib.request.urlretrieve(FFMPEG_URL, zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(FFMPEG_FOLDER)
    os.remove(zip_path)
    print(f"ffmpeg descărcat și dezarhivat în {FFMPEG_FOLDER}")

def add_ffmpeg_to_path():
    # Găsește folderul bin
    for root, dirs, files in os.walk(FFMPEG_FOLDER):
        if "bin" in dirs:
            ffmpeg_bin_path = os.path.join(root, "bin")
            os.environ["PATH"] += os.pathsep + ffmpeg_bin_path
            print(f"ffmpeg adăugat temporar în PATH: {ffmpeg_bin_path}")
            break

def install_dependencies():
    print("Instalare dependențe Python...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def run_converter():
    subprocess.run([sys.executable, "convert_m4a_mp3.py"])

if __name__ == "__main__":
    if not is_ffmpeg_installed():
        download_ffmpeg()
        add_ffmpeg_to_path()
    else:
        print("ffmpeg găsit în PATH")

    install_dependencies()
    run_converter()
