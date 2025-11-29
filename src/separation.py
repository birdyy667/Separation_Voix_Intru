import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt
import soundfile as sf
from pathlib import Path

# -------------------------------------------------
#                PARAMÈTRES GÉNÉRAUX
# -------------------------------------------------

wav_path = Path(
    r"H:\Documents\Trait_Signal\TP\Separation_Voix_Instru\Separation_Voix_Intru\Data\wav_mixes\Al James - Schoolboy Facination.stem.wav"
)

# Dossier de sortie : Data/wav_mixes/outputs
OUTPUT_DIR = wav_path.parent / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)


# -------------------------------------------------
#                 FONCTIONS UTILITAIRES
# -------------------------------------------------
def butter_bandpass(lowcut, highcut, fs, order=4):
    """Filtre passe-bande Butterworth (ordre raisonnable)."""
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype="band")
    return b, a


def apply_voice_filter(y, fs):
    """
    Filtre passe-bande pour la voix.
    Bande assez large pour ne pas tout détruire.
    """
    lowcut = 200.0      # Hz
    highcut = 5000.0    # Hz
    b, a = butter_bandpass(lowcut, highcut, fs, order=4)
    voice = filtfilt(b, a, y)
    return voice


def normalize(sig):
    """Normalise le signal dans [-1, 1] si possible."""
    m = np.max(np.abs(sig))
    if m > 0:
        return sig / m
    return sig


def show_spectrogram(sig, sr, title):
    D = librosa.stft(sig, n_fft=2048, hop_length=512)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    plt.figure(figsize=(12, 4))
    librosa.display.specshow(
        S_db,
        sr=sr,
        hop_length=512,
        x_axis='time',
        y_axis='hz',
        cmap='magma'
    )
    plt.colorbar(format='%+2.0f dB')
    plt.ylim(0, 4000)  # zone voix
    plt.title(title)
    plt.tight_layout()
    plt.show()


# -------------------------------------------------
#              PROGRAMME PRINCIPAL
# -------------------------------------------------

def main():
    # 1) Charger le fichier .wav (mix)
    y, sr = librosa.load(wav_path, sr=None)
    print("Fréquence d'échantillonnage :", sr)
    print("Durée du signal (s) :", len(y) / sr)
    print("Amplitude max mix (y) :", float(np.max(np.abs(y))))

    # 2) Waveform du mix
    plt.figure(figsize=(12, 4))
    plt.plot(y)
    plt.title("Waveform audio (mix)")
    plt.xlabel("Échantillons")
    plt.ylabel("Amplitude")
    plt.show()

    # 3) Spectrogramme du mix
    D = librosa.stft(y, n_fft=2048, hop_length=512)
    S_db = librosa.amplitude_to_db(np.abs(D), ref=np.max)

    plt.figure(figsize=(12, 6))
    librosa.display.specshow(
        S_db,
        sr=sr,
        hop_length=512,
        x_axis='time',
        y_axis='hz',
        cmap='magma'
    )
    plt.colorbar(format='%+2.0f dB')
    plt.title("Spectrogramme STFT (mix, 0–4 kHz)")
    plt.ylim(0, 4000)
    plt.show()

    # 4) Extraction de la voix par filtrage
    voice = apply_voice_filter(y, sr)
    instrumental = y - voice

    print("Amplitude max voice (avant norm) :", float(np.max(np.abs(voice))))
    print("Amplitude max instrumental (avant norm) :", float(np.max(np.abs(instrumental))))

    # 5) Normalisation pour être sûr d'entendre quelque chose
    voice = normalize(voice)
    instrumental = normalize(instrumental)

    print("Amplitude max voice (après norm) :", float(np.max(np.abs(voice))))
    print("Amplitude max instrumental (après norm) :", float(np.max(np.abs(instrumental))))

    # 6) Spectrogrammes filtrés (facultatif mais utile)
    show_spectrogram(voice, sr, "Spectrogramme – Voix filtrée (0–4 kHz)")
    show_spectrogram(instrumental, sr, "Spectrogramme – Résidu instrumental (0–4 kHz)")

    # 7) Sauvegarde des signaux
    voice_path = OUTPUT_DIR / "voice.wav"
    instru_path = OUTPUT_DIR / "instrumental.wav"

    sf.write(voice_path, voice, sr)
    sf.write(instru_path, instrumental, sr)

    print("\nFichiers générés :")
    print("-", voice_path)
    print("-", instru_path)


# -------------------------------------------------
#              POINT D’ENTRÉE DU SCRIPT
# -------------------------------------------------

if __name__ == "__main__":
    main()
