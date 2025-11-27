# src/run_demucs_on_folder.py

import subprocess
from pathlib import Path
import argparse

def run_demucs_on_file(audio_path: Path, model: str = "htdemucs", out_dir: Path | None = None):
    """
    Lance Demucs sur un seul fichier audio.
    """
    if not audio_path.exists():
        print(f"[WARN] Fichier introuvable : {audio_path}")
        return

    cmd = ["demucs", "-n", model]

    if out_dir is not None:
        out_dir.mkdir(parents=True, exist_ok=True)
        cmd += ["--out", str(out_dir)]

    cmd.append(str(audio_path))

    print("\n" + "=" * 80)
    print(f"[INFO] Séparation du fichier : {audio_path}")
    print("[INFO] Commande :", " ".join(cmd))
    print("=" * 80 + "\n")

    subprocess.run(cmd, check=True)


def run_demucs_on_folder(
    input_dir: Path,
    pattern: str = "*.wav",
    model: str = "htdemucs",
    out_dir: Path | None = None,
    recursive: bool = False,
):
    """
    Parcourt un dossier et lance Demucs sur tous les fichiers qui matchent `pattern`.
    """
    if not input_dir.exists():
        print(f"[ERREUR] Dossier introuvable : {input_dir}")
        return

    glob_method = input_dir.rglob if recursive else input_dir.glob
    files = sorted(list(glob_method(pattern)))

    if not files:
        print(f"[INFO] Aucun fichier trouvé dans {input_dir} avec le pattern {pattern}")
        return

    print(f"[INFO] {len(files)} fichier(s) trouvé(s) dans {input_dir} (pattern = {pattern})")

    for f in files:
        run_demucs_on_file(f, model=model, out_dir=out_dir)


def main():
    parser = argparse.ArgumentParser(description="Lancer Demucs sur tous les fichiers d'un dossier.")
    parser.add_argument(
        "--input-dir",
        type=str,
        default="Data/wav_mixes",
        help="Dossier contenant les fichiers audio (par défaut : Data/wav_mixes).",
    )
    parser.add_argument(
        "--pattern",
        type=str,
        default="*.wav",
        help="Pattern de fichiers à traiter (ex : *.wav, *.stem.wav, *.mp3).",
    )
    parser.add_argument(
        "--model",
        type=str,
        default="htdemucs",
        help="Nom du modèle Demucs (par ex : htdemucs, mdx_extra_q).",
    )
    parser.add_argument(
        "--out-dir",
        type=str,
        default="",
        help="Dossier de sortie pour les pistes séparées (par défaut : celui de Demucs).",
    )
    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Parcourir récursivement les sous-dossiers.",
    )

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    out_dir = Path(args.out_dir) if args.out_dir else None

    run_demucs_on_folder(
        input_dir=input_dir,
        pattern=args.pattern,
        model=args.model,
        out_dir=out_dir,
        recursive=args.recursive,
    )


if __name__ == "__main__":
    main()
