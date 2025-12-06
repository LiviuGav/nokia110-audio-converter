from pydub import AudioSegment
import os

def convert_for_nokia110(input_file, output_file):
    """
    Converteste un fisier M4A in MP3 optimizat pentru Nokia 110
    Setari recomandate:
    - Format: MP3
    - Bitrate: 96 kbps
    - Sample rate: 44100 Hz
    - Canale: Mono
    - Normalizare volum
    """
    audio = AudioSegment.from_file(input_file, format="m4a")

    # Convertire în MONO
    audio = audio.set_channels(1)

    # Setare sample rate
    audio = audio.set_frame_rate(44100)

    # Normalizare volum (~ -14 LUFS)
    loudness_target = -14.0
    loudness_current = audio.dBFS
    audio = audio.apply_gain(loudness_target - loudness_current)

    # Export MP3
    audio.export(output_file, format="mp3", bitrate="96k")
    print(f"Convertit: {output_file}")


def convert_folder(folder_path):
    """
    Convertește toate fișierele .m4a din folder_path
    și le salvează într-un subfolder *_nokia110.
    """
    # Creează folderul de ieșire
    output_folder = folder_path.rstrip("\\/") + "_nokia110"
    os.makedirs(output_folder, exist_ok=True)

    print(f"Convertesc fișierele din: {folder_path}")
    print(f"Fișierele convertite vor fi în: {output_folder}\n")

    files = os.listdir(folder_path)
    converted_count = 0

    for f in files:
        if f.lower().endswith(".m4a"):
            input_path = os.path.join(folder_path, f)
            base_name = os.path.splitext(f)[0]
            output_path = os.path.join(output_folder, base_name + "_nokia110.mp3")
            convert_for_nokia110(input_path, output_path)
            converted_count += 1

    if converted_count == 0:
        print("Nu s-au găsit fișiere M4A în folderul dat.")
    else:
        print(f"\n{converted_count} fișiere M4A au fost convertite.")


if __name__ == "__main__":
    folder = input("Introduceti calea catre folderul cu fisiere M4A: ").strip()
    if os.path.isdir(folder):
        convert_folder(folder)
    else:
        print("Calea introdusa nu este un folder valid.")