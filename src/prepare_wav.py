# src/prepare_wav.py
from pathlib import Path
import subprocess

# Vos chemins (basés sur votre capture d'écran)
DATA_DIR = Path(r"H:\Documents\Trait_Signal\TP\Separation_voix_instru\Separation_Voix_Intru\Data")
MUSDB_DIR = DATA_DIR 
OUTPUT_DIR = DATA_DIR / "wav_mixes"

def extract_mix_and_vocals_from_mp4(input_path: Path, output_dir: Path):
    """
    Extrait le Mix complet (pour l'entrée) ET la piste Vocals (pour la vérification/note).
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Noms des fichiers de sortie
    out_mix = output_dir / (input_path.stem + ".wav")         # Le Mix
    out_vocals = output_dir / (input_path.stem + "_vocals.wav") # La Vraie Voix (Vérité Terrain)

    # Commande 1 : Extraire le MIX (Stereo)
    # ffmpeg prend tout l'audio par défaut
    cmd_mix = [
        "./src/ffmpeg.exe", "-y",
        "-i", str(input_path),
        "-ac", "2", 
        "-vn", # Pas de vidéo
        str(out_mix)
    ]

    # Commande 2 : Extraire les VOCALS 
    # Dans les fichiers Stem MP4 (Native Instruments), les pistes sont souvent dans cet ordre :
    # 0:Mix, 1:Drums, 2:Bass, 3:Other, 4:Vocals.
    # On utilise "-map 0:4" pour cibler la 5ème piste (les voix).
    cmd_vocals = [
        "./src/ffmpeg.exe", "-y",
        "-i", str(input_path),
        "-map", "0:4", 
        "-ac", "1", # On convertit en mono pour simplifier la comparaison SNR
        "-vn",
        str(out_vocals)
    ]

    print(f"Traitement de : {input_path.name}")
    
    # Exécution extraction MIX
    subprocess.run(cmd_mix, check=True)
    print(f" -> Mix extrait : {out_mix.name}")
    
    # Exécution extraction VOCALS
    try:
        subprocess.run(cmd_vocals, check=True)
        print(f" -> Vocals extraits : {out_vocals.name}")
    except subprocess.CalledProcessError:
        print(f"⚠️ ERREUR : Impossible d'extraire la voix sur ce fichier (vérifier le map ffmpeg).")

def main():
    # On ne traite que le dossier 'test' comme dans votre exemple
    test_dir = MUSDB_DIR / "test"
    
    if not test_dir.exists():
        print(f"Erreur : Le dossier {test_dir} n'existe pas !")
        return

    # On cherche les fichiers .mp4 (ou .stem.mp4)
    files = list(test_dir.glob("*.mp4"))
    print(f"Fichiers trouvés : {len(files)}")

    for stem_file in files:
        extract_mix_and_vocals_from_mp4(stem_file, OUTPUT_DIR)

if __name__ == "__main__":
    main()