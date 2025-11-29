import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from pathlib import Path

# --- CHEMINS (VERIFIEZ CES 3 LIGNES) ---
# 1. La VRAIE voix
path_true = Path(r"H:\Documents\Trait_Signal\TP\Separation_Voix_Instru\Separation_Voix_Intru\Data\wav_mixes\Al James - Schoolboy Facination.stem_vocals.wav")

# 2. Votre séparation FILTRE (le fichier voice.wav généré par separation.py)
path_filter = Path(r"H:\Documents\Trait_Signal\TP\Separation_Voix_Instru\Separation_Voix_Intru\Data\wav_mixes\outputs\voice.wav")

# 3. La séparation DEMUCS (Vérifiez bien ce chemin, il est dans le dossier 'separated' créé par Demucs)
path_demucs = Path(r"H:\Documents\Trait_Signal\TP\Separation_Voix_Instru\Separation_Voix_Intru\separated\htdemucs\Al James - Schoolboy Facination.stem\vocals.wav")

def calculate_snr(target, estimate):
    # Alignement des tailles (on coupe au plus court)
    min_len = min(len(target), len(estimate))
    target = target[:min_len]
    estimate = estimate[:min_len]
    
    noise = target - estimate
    s_power = np.sum(target**2)
    n_power = np.sum(noise**2)
    
    if n_power == 0: return 100
    return 10 * np.log10(s_power / n_power)

def plot_spectrogram(y, sr, title, ax):
    D = librosa.stft(y)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    librosa.display.specshow(S_db, sr=sr, x_axis='time', y_axis='hz', ax=ax, cmap='magma')
    ax.set_title(title)
    ax.set_ylim(0, 8000)

def main():
    print("--- Analyse Comparative ---")
    
    # Chargement
    print(f"Chargement Vérité : {path_true.name}")
    y_true, sr = librosa.load(path_true, sr=None, mono=True)
    
    print(f"Chargement Filtre : {path_filter.name}")
    y_filt, _ = librosa.load(path_filter, sr=None, mono=True)
    
    print(f"Chargement Demucs : {path_demucs.name}")
    y_dem, _  = librosa.load(path_demucs, sr=None, mono=True)

    # Calcul SNR
    snr_filt = calculate_snr(y_true, y_filt)
    snr_dem = calculate_snr(y_true, y_dem)

    print(f"\n>>> RÉSULTATS SNR <<<")
    print(f"1. Votre Filtre Passe-Bande : {snr_filt:.2f} dB")
    print(f"2. IA Demucs                : {snr_dem:.2f} dB")

    # Graphique
    fig, ax = plt.subplots(3, 1, figsize=(10, 12), sharex=True)
    plot_spectrogram(y_true, sr, "Vérité Terrain (Vraie Voix)", ax[0])
    plot_spectrogram(y_filt, sr, f"Approche 1: Filtre (SNR={snr_filt:.1f}dB)", ax[1])
    plot_spectrogram(y_dem, sr, f"Approche 2: Demucs (SNR={snr_dem:.1f}dB)", ax[2])
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()