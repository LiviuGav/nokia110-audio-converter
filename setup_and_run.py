import os
import subprocess
import sys
import urllib.request
import zipfile

FFMPEG_URL = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
FFMPEG_FOLDER = "ffmpeg"
FFMPEG_CHECKSUM_FILE = os.path.join(FFMPEG_FOLDER, ".ffmpeg_ok")

def show_download_progress(block_num, block_size, total_size):
    """Afișează progresul descărcării"""
    if total_size == -1:
        print(f"Descărcat: {block_num * block_size} bytes", end='\r')
    else:
        downloaded = block_num * block_size
        if downloaded >= total_size:
            downloaded = total_size
        percent = (downloaded / total_size) * 100
        bar_length = 40
        filled = int(bar_length * downloaded // total_size)
        bar = '#' * filled + '-' * (bar_length - filled)
        print(f"Progres: [{bar}] {percent:.1f}% ({downloaded / (1024**2):.1f} MB / {total_size / (1024**2):.1f} MB)", end='\r')

def get_ffmpeg_path():
    """Găsește calea completă la ffmpeg.exe din folderul local"""
    for root, dirs, files in os.walk(FFMPEG_FOLDER):
        if "ffmpeg.exe" in files:
            return os.path.join(root, "ffmpeg.exe")
    return None

def is_ffmpeg_valid():
    """Verifică dacă ffmpeg există local și este valid"""
    if not os.path.exists(FFMPEG_CHECKSUM_FILE):
        return False
    
    return get_ffmpeg_path() is not None

def is_ffmpeg_installed():
    """Verifică dacă ffmpeg este instalat în sistem"""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except FileNotFoundError:
        return False

def download_ffmpeg():
    
    # Creează folderul dacă nu există
    os.makedirs(FFMPEG_FOLDER, exist_ok=True)
    
    zip_path = "ffmpeg.zip"
    try:
        urllib.request.urlretrieve(FFMPEG_URL, zip_path, show_download_progress)
        print("\n\nFișierul a fost descărcat. Se dezarhivează...")
        
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(FFMPEG_FOLDER)
        
        os.remove(zip_path)
        
        # Creează marker file pentru a indica că ffmpeg este valid
        with open(FFMPEG_CHECKSUM_FILE, 'w') as f:
            f.write("ffmpeg verificat")
        
        print(f"ffmpeg a fost dezarhivat în folderul {FFMPEG_FOLDER}")
        return True
    except Exception as e:
        print(f"Eroare la descărcarea ffmpeg: {e}")
        return False

def setup_ffmpeg_env():
    """Salvează calea ffmpeg pentru folosire în converter"""
    ffmpeg_path = get_ffmpeg_path()
    if ffmpeg_path:
        os.environ["FFMPEG_PATH"] = ffmpeg_path
        ffmpeg_dir = os.path.dirname(ffmpeg_path)
        os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
        print(f"ffmpeg găsit la: {ffmpeg_path}")

def install_dependencies():
    print("\nInstalare dependențe Python...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

def run_converter():
    subprocess.run([sys.executable, "convert_m4a_mp3.py"])

if __name__ == "__main__":
    # Verifică dacă ffmpeg este în sistem
    if is_ffmpeg_installed():
        print("ffmpeg a fost găsit în PATH-ul sistemului")
    else:
        # Dacă nu e în sistem, verifică local
        if is_ffmpeg_valid():
            print("ffmpeg a fost găsit în local și este valid")
            setup_ffmpeg_env()
        else:
            # Dacă nu e nici local, descarcă
            print("ffmpeg nu a fost găsit. Se inițiază descărcarea...")
            if not download_ffmpeg():
                print("Eroare: nu s-a putut descărca ffmpeg")
                sys.exit(1)
            setup_ffmpeg_env()

    # Adaugă ffmpeg la PATH înainte de a instala dependențe (pentru pydub)
    if "FFMPEG_PATH" in os.environ:
        ffmpeg_dir = os.path.dirname(os.environ["FFMPEG_PATH"])
        if ffmpeg_dir not in os.environ.get("PATH", ""):
            os.environ["PATH"] = ffmpeg_dir + os.pathsep + os.environ.get("PATH", "")
    
    install_dependencies()
    run_converter()
