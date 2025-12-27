# Système de Détection de Somnolence du Conducteur 🚗💤

Un système de détection de somnolence en temps réel utilisant YOLOv8 et la vision par ordinateur pour améliorer la sécurité routière en surveillant l'état d'alerte du conducteur et en déclenchant des alertes sonores lorsque des signes de fatigue sont détectés.

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

- **Détection en Temps Réel** : Traite le flux vidéo de la webcam en temps réel avec YOLOv8
- **Suivi Intelligent des États** : Accumule le temps de danger entre les états fatigué et endormi
- **Alertes Sonores** : Lecture continue de l'alarme jusqu'au retour à l'état éveillé
- **Retour Visuel** : 
  - Boîtes englobantes colorées (Vert/Orange/Rouge)
  - Bannières d'alerte ("ALERT: SLEEPING!" / "ALERT: TIRED!")
  - Affichage du timer de danger en temps réel
- **Architecture Modulaire** : Structure de code propre et maintenable

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
├── main.py                 # Point d'entrée de l'application
├── requirements.txt        # Dépendances Python
├── README.md              # Documentation
│
├── assets/
│   ├── models/
│   │   └── best-2.pt      # Poids du modèle YOLOv8 fine-tuné
│   └── sounds/
│       ├── sleep.wav      # Audio d'alerte pour endormi
│       └── tired.wav      # Audio d'alerte pour fatigué
│
└── src/
    ├── __init__.py
    ├── config.py          # Paramètres de configuration
    ├── detector.py        # Module de détection YOLOv8
    ├── logic.py           # Logique de suivi d'état et d'alerte
    ├── alerter.py         # Gestion de la lecture audio
    └── visualizer.py      # Visualisation OpenCV
```

## 💻 Utilisation

Exécuter l'application :
```bash
python main.py
```

**Contrôles :**
- Appuyer sur `q` pour quitter l'application

**Ce que vous verrez :**
- Flux vidéo en direct avec boîtes englobantes de détection
- Labels d'état actuel avec scores de confiance
- Timer de danger (lorsqu'en état fatigué/endormi)
- Bannières d'alerte lorsque le seuil est dépassé
- Alarmes sonores jouant en continu jusqu'à l'état éveillé

## ⚙️ Configuration

Modifier `src/config.py` pour personnaliser :

```python
# Seuil d'alerte (secondes)
ALERT_THRESHOLD_SECONDS = 3.0

# Paramètres de la caméra
CAMERA_INDEX = 0
FRAME_WIDTH = 640
FRAME_HEIGHT = 480

# Seuil de confiance de détection
CONFIDENCE_THRESHOLD = 0.5

# Couleurs et visualisation
BOX_COLOR_AWAKE = (0, 255, 0)      # Vert
BOX_COLOR_TIRED = (0, 165, 255)    # Orange
BOX_COLOR_SLEEP = (0, 0, 255)      # Rouge
```

## 📊 Détails du Modèle

- **Framework** : YOLOv8 (Ultralytics)
- **Entraînement** : Fine-tuné sur un dataset personnalisé de détection de somnolence
- **Classes** : 3 (éveillé, endormi, fatigué)
- **Fichier du Modèle** : `assets/models/best-2.pt`

## 📋 Dépendances

- ultralytics>=8.0.0
- opencv-python>=4.8.0
- torch>=2.0.0
- torchvision>=0.15.0
- pygame>=2.5.0
- numpy>=1.24.0
- Pillow>=10.0.0

## 🎯 Cas d'Usage

- Systèmes de surveillance du conducteur dans les véhicules
- Sécurité de gestion de flotte
- Recherche sur l'attention et la fatigue du conducteur
- Démonstrations éducatives d'applications de vision par ordinateur

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

- YOLOv8 par Ultralytics
- Communauté OpenCV
- Contributeurs du dataset

---

**⚡ Restez Vigilant, Restez en Sécurité !** 


