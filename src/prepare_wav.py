# src/prepare_wav.py
from pathlib import Path
import subprocess

DATA_DIR = Path(r"H:\Documents\2025-2026\ing2\S11\Tratement du signal\Separation_voix_instru\Data")
MUSDB_DIR = DATA_DIR  # ton musdb18 est directement dans Data
OUTPUT_DIR = DATA_DIR / "wav_mixes"

def extract_mix_from_mp4(input_path: Path, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cmd = [
        "ffmpeg",
        "-y",              # overwrite
        "-i", str(input_path),
        "-ac", "2",        # stéréo
        "-vn",             # pas de vidéo
        str(output_path)
    ]
    print(" ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    # Exemple : on ne traite que quelques fichiers du dossier test pour commencer
    test_dir = MUSDB_DIR / "test"
    for stem_file in test_dir.glob("*.stem.mp4"):
        out_wav = OUTPUT_DIR / (stem_file.stem + ".wav")
        print(f"Conversion : {stem_file.name} -> {out_wav.name}")
        extract_mix_from_mp4(stem_file, out_wav)

if __name__ == "__main__":
    main()
