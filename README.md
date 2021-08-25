# PROFIL Project Overview

## 🚙 Démarrage rapide pour la création du logiciel

1. Confirmez que les fichiers dans la liste de fichiers se trouvent dans un certain répertoire, tel que : *C:/Users/Cerema/* 
2. Ouvrez Anaconda Prompt et utilisez la commande bash pour entrer dans le répertoire
> cd nom_du_répertoire
3. Exécutez le code suivant pour générer le fichier exe, cela prendra un certain temps
> pyinstaller -F Logiciel_Profil_v1.py
4. (Facultatif) Entrez Enigma Virtual Box pour compresser à nouveau le fichier exe, ce qui accélérera l'exécution du fichier.
5. Avant d'exécuter le logiciel, mettez les images et le modèle (yolo-tiny.weights) dans le dossier ‘dist’ généré (où Logiciel_Profil_v1.exe est généré)
6. Exécutez le logiciel et suivez les instructions dans l'écran AIDE

---

## 📑 Liste de fichiers

### Codes

- **Logiciel_Profil_v1.py**

    L'interface du logiciel et les fonctions principales pour création des courbes

- **utils.py**

    Les outils pour la prédition de Yolo (génération de bounding box, chargement des paramètres, etc.)

- **detect.py**

    La structure du modèle Yolo

- **treatData.py**

    Pré-traitement des données de csvs pour calculer les vitesse, distance, ...(l'alignement, le remplissage des blancs, ...)

- **video2.py**

    Traitement des données de CI, CAN, Lidar (l'alignement, le remplissage des blancs, ...)

### Modèle

- **yolo-tiny.weights**

    Paramètres du modèle YOLO finetuné

### Images

- **CONT1.png**

    Fond pour afficher les données 

- **logo-3.png**

    Logo de Céréma

- **fenetre0.png**

    Fond de page d'accueil

- **doc_0610.png**

    Tutorial dans l'écran 'AIDE'
