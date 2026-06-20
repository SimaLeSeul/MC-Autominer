# ⛏️ Script de Minage Automatique pour Minecraft - Tunnel 2x2

Script Python d'automatisation de minage pour Minecraft, conçu pour creuser des tunnels de 2x2 blocs en ligne droite avec des mesures d'anti-détection avancées.

## 📋 Fonctionnalités

- ✅ **Minage automatique** de 4 blocs (2 en haut, 2 en bas) puis avance
- ✅ **Randomisation des mouvements de souris** pour éviter la détection
- ✅ **Délais aléatoires** entre chaque action (anti-robot)
- ✅ **Arrêt d'urgence** avec les touches `Q` ou `Escape`
- ✅ **Statistiques en temps réel** (cycles, vitesse, temps écoulé)
- ✅ **Code commenté** et facilement personnalisable

## 🛠️ Installation

### Prérequis

- **Python 3.9+** installé sur votre système
- **Minecraft** lancé et connecté à un serveur (ou en mode solo)

### ⚠️ Problème courant : "Python was not found"

Si vous voyez le message `Python was not found; run without arguments to install from the Microsoft Store`, c'est que Python n'est pas réellement installé. Le message "Python was not found" doit être ignoré.

**Solution :**

1. **Téléchargez Python** depuis [python.org](https://www.python.org/downloads/)
2. **Lancez l'installateur**
3. **COCHEZ la case** `"Add Python to PATH"` lors de l'installation (très important!)
4. Cliquez sur "Install Now"

5. **Vérifiez l'installation** en ouvrant un NVEAU terminal PowerShell et en tapant :

   ```powershell
   python --version
   ```

   Vous devriez voir : `Python 3.x.x`

### Étapes d'installation des dépendances

1. **Ouvrez un terminal** dans le dossier du projet (où se trouve `requirements.txt`)

2. **Installez les dépendances Python** avec la commande suivante :

   ```bash
   pip install -r requirements.txt
   ```

   Ou installez les paquets individuellement :

   ```bash
   pip install pyautogui pydirectinput keyboard
   ```

### Dépendances

| Paquet | Version | Description |
|--------|---------|-------------|
| `pyautogui` | 0.9.54 | Simulation des mouvements de souris |
| `pydirectinput` | 1.0.4 | Entrées clavier directes (optimisé pour Minecraft) |
| `keyboard` | 0.13.5 | Surveillance des touches d'arrêt d'urgence |

## 🚀 Utilisation

### Démarrage rapide

```bash
python autominer.py
```

### Étapes d'utilisation

1. **Lancez Minecraft** et connectez-vous à un serveur (ou mode solo)
2. **Assurez-vous d'avoir une pioche** dans votre inventaire
3. **Placez-vous face à un mur** de blocs à miner (sol ou paroi)
4. **Lancez le script** avec la commande ci-dessus
5. **Appuyez sur `Entrée`** pour démarrer le minage automatique
6. **Appuyez sur `Q` ou `Escape`** à tout moment pour arrêter le script

### Configuration

Éditez le fichier `autominer.py` et modifiez le dictionnaire `CONFIG` en haut du fichier :

```python
CONFIG = {
    # Nombre de clics par bloc (ajuste selon ta pioche)
    "couples_de_tirs_par_bloc": 4,
    
    # Amplitude des micro-déplacements de souris (pixels)
    "deplacement_min_x": -3,
    "deplacement_max_x": 3,
    "deplacement_min_y": -3,
    "deplacement_max_y": 3,
    
    # Délais aléatoires (en millisecondes)
    "delai_clic_min_ms": 150,
    "delai_clic_max_ms": 350,
    "delai_avance_min_ms": 400,
    "delai_avance_max_ms": 800,
    
    # Touche d'arrêt d'urgence
    "touche_arret": "q",
}
```

## 📐 Mécanique de fonctionnement

Le script exécute le cycle suivant en boucle :

```
┌─────────────────────────────────────────┐
│  CYCLE DE MINAGE 2x2                    │
├─────────────────────────────────────────┤
│                                         │
│  [1] Miner les 4 blocs devant toi:      │
│     ┌───────┬───────┐                   │
│     │ Bloc1 │ Bloc2 │  ← Haut (2 blocs) │
│     ├───────┼───────┤                   │
│     │ Bloc3 │ Bloc4 │  ← Bas (2 blocs) │
│     └───────┴───────┘                   │
│                                         │
│  [2] Avancer d'une case                 │
│                                         │
│  [3] Répéter le cycle ∞                │
└─────────────────────────────────────────┘
```

### Mesures de sécurité intégrées

| Mesure | Description |
|--------|-------------|
| 🖱️ Micro-déplacements souris | Déplacement aléatoire de ±3 pixels après chaque bloc miné |
| ⏱️ Délais aléatoires | 150-350ms entre les clics, 400-800ms pour l'avance |
| 🛑 Arrêt d'urgence | Touches `Q` ou `Escape` pour arrêter instantanément |

## ⚠️ Avertissements

- **Usage responsable** : Ce script est conçu pour un usage personnel en solo ou sur des serveurs autorisant l'automatisation
- **Risque de bannissement** : L'utilisation sur des serveurs publics sans autorisation peut entraîner un bannissement
- **Anti-cheat** : Certains serveurs disposent de systèmes anti-cheat avancés qui peuvent détecter l'automatisation
- **À vos risques** : L'auteur du script n'est pas responsable des conséquences de son utilisation

## 📁 Structure du projet

```
autominer/
├── autominer.py        # Script principal
├── requirements.txt    # Dépendances Python
└── README.md          # Ce fichier
```

## 🔧 Dépannage

| Problème | Solution |
|----------|----------|
| Erreur `ModuleNotFoundError` | Vérifie que les dépendances sont installées (`pip install -r requirements.txt`) |
| Les clics ne fonctionnent pas dans Minecraft | Assure-toi que le script est exécuté en tant qu'administrateur |
| La souris bouge de trop | Réduis les valeurs `deplacement_min_x` et `deplacement_max_x` |
| Le minage est trop rapide/lent | Ajuste les valeurs `delai_clic_min_ms` et `delai_clic_max_ms` |

## 📝 Licence

Ce script est fourni à des fins éducatifs et d'usage personnel uniquement.

---

**Version**: 1.0  
**Auteur**: Cline (IA)  
**Python requis**: 3.9+