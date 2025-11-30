# Projet de Séparation Voix/Mélodie et Analyse Audio

## **Contexte**
Ce projet vise à **séparer automatiquement la voix et la mélodie** dans des fichiers audio, ainsi qu'à **analyser les caractéristiques acoustiques** des pistes séparées (vocals, drums, bass, other). Il utilise des outils de traitement du signal et d'apprentissage automatique pour atteindre ces objectifs.

---

## **Objectifs**
1. **Séparer** les composantes audio (voix, batterie, basse, autres) à partir de fichiers musicaux complets.
2. **Analyser** les fichiers audio séparés pour extraire des caractéristiques comme :
   - Spectrogrammes (STFT).
   - Fréquences dominantes.
   - Enveloppes temporelles.
3. **Évaluer** la qualité de la séparation et des analyses.

---

## **Outils et Bibliothèques Utilisés**
- **Demucs** : Séparation des pistes audio (vocals, drums, bass, other).
- **Librosa** : Extraction des caractéristiques audio (spectrogrammes, fréquences dominantes, enveloppes temporelles).
- **NumPy, SciPy, Matplotlib** : Traitement numérique et visualisation.
- **PyTorch/TensorFlow** : Support pour les modèles de séparation (Demucs).

---

## **Étapes Clés du Projet**

### **1. Séparation des Pistes Audio**
- Utilisation de **Demucs** pour séparer les fichiers audio en 4 composantes :
  - **Vocals** (voix).
  - **Drums** (batterie).
  - **Bass** (basse).
  - **Other** (autres instruments).
- Script : `run_demucs_on_folder.py`.

### **2. Analyse des Caractéristiques Audio**
- Extraction des **spectrogrammes** (STFT) pour visualiser les fréquences au fil du temps.
- Identification des **fréquences dominantes** pour chaque piste.
- Extraction des **enveloppes temporelles** pour analyser les variations d'amplitude.
- Script : `analyse_wav.py`.

### **3. Séparation Voix/Mélodie**
- Utilisation des **fréquences dominantes** pour distinguer la voix de la mélodie.
- Script : `separation.py`.

---

## **Résultats Attendus**
- Un **jeu de données** de pistes audio séparées et analysées.
- Des **visualisations** (spectrogrammes, enveloppes temporelles) pour chaque piste.
- Un **rapport** détaillant :
  - La méthodologie utilisée.
  - Les résultats des séparations et analyses.
  - Notre façon d'aborder chaque point des attendus du TP dans le cadre de ce projet.
    
