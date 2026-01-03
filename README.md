# Système de Détection de Somnolence du Conducteur 🚗💤

Un système de détection de somnolence en temps réel utilisant YOLOv8 et la vision par ordinateur pour améliorer la sécurité routière en surveillant l'état d'alerte du conducteur et en déclenchant des alertes sonores lorsque des signes de fatigue sont détectés. Le système offre une interface graphique moderne (PyQt6) avec suivi de session et historique des alertes.

## 📋 Informations du Projet

- **Auteur**: Yassine Ben Akki
- **Encadrant**: Prof. Kamal AZGHIOU
- **Établissement**: ENSA Oujda
- **Année Universitaire**: 2025-2026


## 📋 Aperçu Général

Ce système utilise un modèle YOLOv8 fine-tuné pour détecter trois états du conducteur :
- **Éveillé (Awake)** - Le conducteur est alerte et concentré
- **Fatigué (Tired)** - Le conducteur montre des signes de fatigue
- **Endormi (Sleep)** - Le conducteur s'endort

Lorsque le système détecte des états de danger continus (fatigué ou endormi) pendant 3 secondes, il déclenche une alarme sonore pour alerter le conducteur.

## ✨ Fonctionnalités

### Interface Graphique (GUI)
- **Interface PyQt6 Moderne** : Interface sombre professionnelle et intuitive
- **Contrôles Complets** : Boutons Start/Pause/Stop pour contrôler la détection
- **Panneau de Statut en Direct** : 
  - État actuel avec code couleur (Vert/Orange/Rouge)
  - Score de confiance en temps réel
  - Timer de danger avec barre de progression
  - Bannières d'alerte visuelles
- **Tableau de Bord de Session** :
  - Durée totale de la session (HH:MM:SS)
  - Nombre total d'alertes déclenchées
  - Historique des alertes avec horodatage
  - Export des logs de session en CSV
- **Paramètres Configurables** : 
  - Ajustement du seuil d'alerte (1-10 secondes)
  - Sélection de la caméra

### Détection et Alertes
- **Détection en Temps Réel** : Traite le flux vidéo de la webcam en temps réel avec YOLOv8
- **Suivi Intelligent des États** : Accumule le temps de danger entre les états fatigué et endormi
- **Alertes Sonores** : Lecture continue de l'alarme jusqu'au retour à l'état éveillé
- **Retour Visuel** : 
  - Boîtes englobantes colorées sur le flux vidéo
  - Bannières d'alerte ("ALERT: SLEEPING!" / "ALERT: TIRED!")
  - Affichage du timer de danger en temps réel

### Architecture et Performances
- **Threading Optimisé** : Traitement vidéo en arrière-plan pour une interface réactive
- **Architecture Modulaire** : Code propre et maintenable séparant GUI et logique métier
- **Gestion de Session** : Suivi automatique des statistiques sans base de données

## 🚀 Fonctionnement

1. **Capture** : OpenCV capture les images vidéo depuis la webcam
2. **Détection** : Le modèle YOLOv8 fine-tuné analyse chaque frame
3. **Suivi** : Le module de logique accumule le temps passé dans les états de danger (fatigué/endormi)
4. **Alerte** : Après 3 secondes en état de danger, déclenche une alarme sonore continue
5. **Réinitialisation** : Retour à la surveillance normale lorsque le conducteur devient éveillé

### Logique des États
- **Fatigué → Endormi** : Le compteur continue (les deux sont des états de danger)
- **Endormi → Fatigué** : Le compteur continue (les deux sont des états de danger)
- **Éveillé détecté** : Le compteur se réinitialise, l'alarme s'arrête

## 🛠️ Installation

### Prérequis
- Python 3.8 ou supérieur
- Webcam

### Configuration

1. **Cloner le dépôt**
```bash
git clone https://github.com/yassin99e/Driver-Safety-System.git
cd Driver-Safety-System
```

2. **Créer un environnement virtuel** (recommandé)
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

## 📦 Structure du Projet

```
driver_safety_system/
│
├── main.py                 # Point d'entrée CLI (ligne de commande)
├── main_gui.py            # Point d'entrée GUI (interface graphique) ⭐
├── requirements.txt        # Dépendances Python
├── README.md              # Documentation
│
├── assets/
│   ├── models/
│   │   └── best-2.pt      # Poids du modèle YOLOv8 fine-tuné
│   ├── sounds/
│   │   ├── sleep.wav      # Audio d'alerte pour endormi
│   │   └── tired.wav      # Audio d'alerte pour fatigué
│   └── logs/              # Logs de session exportés (CSV)
│
└── src/
    ├── __init__.py
    ├── config.py          # Paramètres de configuration
    ├── detector.py        # Module de détection YOLOv8
    ├── logic.py           # Logique de suivi d'état et d'alerte
    ├── alerter.py         # Gestion de la lecture audio
    ├── visualizer.py      # Visualisation OpenCV
    │
    └── gui/               # Modules d'interface graphique ⭐
        ├── __init__.py
        ├── main_window.py      # Fenêtre principale
        ├── video_thread.py     # Thread de traitement vidéo
        ├── session_manager.py  # Gestion de session et statistiques
        └── widgets/
            ├── __init__.py
            ├── video_widget.py    # Affichage vidéo
            ├── control_panel.py   # Panneau de contrôle
            ├── status_panel.py    # Panneau de statut
            └── session_panel.py   # Panneau de session
```

## 💻 Utilisation

### Interface Graphique (Recommandé) 🌟

Lancer l'application avec l'interface moderne :
```bash
python main_gui.py
```

**Contrôles GUI :**
- **▶ START DETECTION** : Démarrer la surveillance
- **⏸ PAUSE** : Mettre en pause la détection
- **⏹ STOP** : Arrêter la session
- **⚙ SETTINGS** : Configurer le seuil d'alerte et la caméra
- **💾 EXPORT SESSION LOG** : Exporter l'historique des alertes en CSV

**Ce que vous verrez :**
- Flux vidéo en direct avec détections visuelles
- Panneau de statut montrant l'état actuel et le timer de danger
- Tableau de bord avec durée de session et nombre d'alertes
- Historique détaillé des alertes avec horodatage
- Alertes sonores en continu lors de détection de danger

### Interface Ligne de Commande (CLI)

Version simplifiée en ligne de commande :
```bash
python main.py
```

**Contrôles CLI :**
- Appuyer sur `q` pour quitter l'application

**Ce que vous verrez :**
- Flux vidéo en direct avec boîtes englobantes de détection
- Labels d'état actuel avec scores de confiance
- Timer de danger (lorsqu'en état fatigué/endormi)
- Bannières d'alerte lorsque le seuil est dépassé
- Alarmes sonores jouant en continu jusqu'à l'état éveillé

## ⚙️ Configuration

### Configuration via l'Interface Graphique
Utilisez le bouton **⚙ SETTINGS** dans l'application pour ajuster :
- **Seuil d'alerte** : 1-10 secondes (par défaut : 3 secondes)
- **Index de caméra** : 0-5 (par défaut : 0)

Les modifications prennent effet lors de la prochaine session de détection.

### Configuration Manuelle

Modifier `src/config.py` pour personnaliser davantage :

```python
# Seuil d'alerte (secondes)
ALERT_THRESHOLD_SECONDS = 3.0

# Paramètres de la caméra
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Seuil de confiance de détection
CONFIDENCE_THRESHOLD = 0.5

# Couleurs de l'interface
GUI_COLOR_AWAKE = "#00FF00"      # Vert
GUI_COLOR_TIRED = "#FFA500"      # Orange
GUI_COLOR_SLEEP = "#FF0000"      # Rouge

# Paramètres de session
SESSION_LOG_DIRECTORY = ROOT_DIR / "logs"
```

## 📊 Détails du Modèle

- **Framework** : YOLOv8 (Ultralytics)
- **Entraînement** : Fine-tuné sur un dataset personnalisé de détection de somnolence
- **Classes** : 3 (éveillé, endormi, fatigué)
- **Fichier du Modèle** : `assets/models/best-2.pt`

## 📋 Dépendances

### Dépendances Principales
- **ultralytics>=8.0.0** - Framework YOLOv8 pour la détection
- **opencv-python>=4.8.0** - Traitement d'images et capture vidéo
- **torch>=2.0.0** - Backend PyTorch pour le deep learning
- **torchvision>=0.15.0** - Utilitaires vision par ordinateur
- **pygame>=2.5.0** - Lecture des alertes audio
- **PyQt6>=6.4.0** - Interface graphique moderne ⭐
- **numpy>=1.24.0** - Calculs numériques
- **Pillow>=10.0.0** - Traitement d'images

### Installation Complète
```bash
pip install -r requirements.txt
```

### Note pour Windows
En cas d'erreur DLL avec PyTorch, réinstaller avec :
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

## 🎯 Cas d'Usage

- **Véhicules Personnels** : Surveillance du conducteur pour la sécurité routière
- **Gestion de Flotte** : Monitoring des chauffeurs professionnels avec logs de session
- **Recherche Académique** : Étude de l'attention et de la fatigue du conducteur
- **Démonstrations Éducatives** : Application pratique de vision par ordinateur et deep learning
- **Prototypage IoT** : Base pour systèmes embarqués de sécurité automobile
- **Analyse de Données** : Export CSV pour analyse statistique des sessions de conduite

## ⚠️ Limitations

- Nécessite de bonnes conditions d'éclairage
- La caméra doit avoir une vue dégagée du visage du conducteur
- Les performances dépendent de la précision du modèle
- Ne remplace pas un repos approprié

## 🤝 Contribution

Les contributions sont les bienvenues ! N'hésitez pas à :
- Signaler des bugs
- Suggérer des fonctionnalités
- Soumettre des pull requests

## 📝 Licence

Ce projet est open source et disponible à des fins éducatives et de recherche.

## 📧 Contact

- **GitHub** : [@yassin99e](https://github.com/yassin99e)
- **Auteur** : Yassine Ben Akki
- **Email** : [yassine.benakki@ump.ac.ma](mailto:yassine.benakki@ump.ac.ma)
- **Établissement** : ENSA Oujda
- **Année Universitaire** : 2025–2026

## 🙏 Remerciements

- **YOLOv8** par Ultralytics pour le framework de détection
- **Communauté OpenCV** pour les outils de vision par ordinateur
- **PyQt6** pour le framework d'interface graphique
- **PyTorch** pour le backend de deep learning
- **Prof. Kamal AZGHIOU** pour l'encadrement du projet
- **ENSA Oujda** pour le soutien académique
- **Contributeurs du dataset** de détection de somnolence

---

**⚡ Restez Vigilant, Restez en Sécurité !** 


