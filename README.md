# ⛏️ Script de Minage Automatique pour Minecraft 1.7.10 - Tunnel 2x2

Script Python d'automatisation de minage pour **Minecraft 1.7.10 moddé**, conçu pour creuser des tunnels de 2x2 blocs en ligne droite avec un **algorithme de temps de minage dynamique** et des mesures d'anti-détection avancées.

## 📋 Fonctionnalités

- ✅ **Minage automatique** de 4 blocs (2 en haut, 2 en bas) puis avance
- ✅ **Algorithme de minage modulaire** pour Minecraft 1.7.10 (calcul dynamique du temps de clic)
- ✅ **Base de données de blocs** : Vanilla + Modded (Thermal Foundation, IC2, BuildCraft, Tinkers' Construct, etc.)
- ✅ **Base de données d'outils** : 35+ pioches supportées (Vanilla, Tinkers', Thermal Series, IC2)
- ✅ **Détection de blocs incassables** (Bedrock, blocs de protection) avec arrêt immédiat
- ✅ **Failsafe** : Blocs/outils inconnus avec valeurs de sécurité par défaut
- ✅ **Randomisation des mouvements de souris** pour éviter la détection
- ✅ **Délais aléatoires** entre chaque action (anti-robot)
- ✅ **Arrêt d'urgence** avec les touches `Q`, `F9` ou pause avec `F8`
- ✅ **Code commenté** et facilement personnalisable

## 🧱 Ajout de nouveaux blocs et pioches

L'algorithme est conçu pour être **extrêmement modulaire**. Ajouter un nouveau minerai ou pioche se fait en une seule ligne !

### Ajouter un bloc (minerais, pierres, etc.)

Ouvrez `mining_algorithm.py` et ajoutez une ligne dans `BLOCKS_HARDNESS` :

```python
"mymod:my_ore": 3.0,  # Format: "block_id": durete
```

### Ajouter une pioche modée

Ajoutez une ligne dans `TOOLS_SPEED` :

```python
"mymod:my_pickaxe": 10.0,  # Format: "tool_id": multiplicateur_de_vitesse
```

### Exemples concrets

```python
# Vanilla
"minecraft:stone": 1.5,
"minecraft:diamond_ore": 6.0,
"minecraft:deepslate": 3.0,

# Thermal Foundation (Thermal Series)
"thermalfoundation:ore:4": 3.0,   # Cuivre
"thermalfoundation:ore:1": 3.0,   # Argent
"thermalfoundation:ore:3": 3.0,   # Etain

# Tinkers' Construct
"tinkers:rose_gold_pickaxe": 14.0,
"tinkers:flux_pickaxe": 12.0,

# IC2
"ic2:oreCopper": 3.0,
"ic2:oreSilver": 3.0,
```

## 🛠️ Installation

### Prérequis

- **Python 3.9+** installé sur votre système
- **Minecraft 1.7.10** moddé lancé et connecté à un serveur (ou mode solo)

### ⚠️ Problème courant : "Python was not found"

Si vous voyez le message `Python was not found; run without arguments to install from the Microsoft Store`, c'est que Python n'est pas réellement installé.

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

1. **Lancez Minecraft 1.7.10 moddé** et connectez-vous à un serveur (ou mode solo)
2. **Équipez-vous de la pioche configurée** dans `autominer.py` (voir `PIOCHE_ACTUELLE_ID`)
3. **Placez-vous face à un mur** de blocs à miner (sol ou paroi)
4. **Lancez le script** avec la commande ci-dessus
5. **Appuyez sur `F8`** pour activer/pauser le minage
6. **Appuyez sur `F9`** pour arrêter définitivement le script
7. **Appuyez sur `Q`** pour l'arrêt d'urgence (relâche le clic)

### Configuration dans `autominer.py`

```python
# Changez selon votre pioche actuelle (voir mining_algorithm.py TOOLS_SPEED)
PIOCHE_ACTUELLE_ID = "minecraft:diamond_pickaxe"

# Niveau d'Enchantement Efficiency (0, I, II, ou III)
NIVEAU_EFFECTIVITE = 0

# Niveau de Potion de Haste (0, I, ou II)
NIVEAU_HASTE = 0

# Changez ces IDs selon les blocs que vous minez
block_id_haut = "minecraft:stone"  # <-- Bloc du haut
block_id_bas = "minecraft:stone"   # <-- Bloc du bas
```

### Configuration de `mining_algorithm.py`

| Paramètre | Description | Valeur par défaut |
|-----------|-------------|-------------------|
| `BLOCKS_HARDNESS` | Dureté des blocs (plus = plus long à miner) | Voir fichier |
| `TOOLS_SPEED` | Vitesse des pioches (plus = plus rapide) | Voir fichier |
| `UNBREAKABLE_BLOCKS` | Liste des blocs incassables (arrêt immédiat) | Bedrock, etc. |
| `DEFAULT_UNKNOWN_BLOCK_HARDNESS` | Dureté par défaut pour bloc inconnu | 5.0 |
| `UNKNOWN_BLOCK_SAFETY_MULTIPLIER` | Multiplicateur de sécurité pour bloc inconnu | 1.5 |

## 📐 Mécanique de fonctionnement

Le script exécute le cycle suivant en boucle :

```
┌─────────────────────────────────────────┐
│  CYCLE DE MINAGE 2x2 (Algorithme 1.7.10)│
├─────────────────────────────────────────┤
│                                         │
│  [1] Miner les 4 blocs devant toi:      │
│     ┌───────┬───────┐                   │
│     │ Bloc1 │ Bloc2 │  ← Haut (2 blocs) │
│     ├───────┼───────┤                   │
│     │ Bloc3 │ Bloc4 │  ← Bas (2 blocs) │
│     └───────┴───────┘                   │
│                                         │
│  [2] Calcul dynamique du temps de minage│
│      (selon bloc + pioche + enchantements)│
│                                         │
│  [3] Avancer d'une case                 │
│                                         │
│  [4] Détecter bloc incassable? → STOP   │
│                                         │
│  [5] Répéter le cycle ∞                │
└─────────────────────────────────────────┘
```

### Formule de calcul (Minecraft 1.7.10)

```
Vitesse de minage = (Vitesse_de_l'Outil / Durete_du_Bloc) * Facteur_Effectivite * Facteur_Haste
Temps_de_clic = 0.05 / Vitesse_de_minage  (en secondes)
```

- **Facteur Effectivité** : `1 + (niveau * 0.3)`
- **Facteur Haste** : `1 + (niveau * 0.2)`

### Mesures de sécurité intégrées

| Mesure | Description |
|--------|-------------|
| 🛡️ Détection bloc incassable | Arrêt immédiat sur Bedrock, blocs de protection, etc. |
| 📦 Failsafe bloc inconnu | Valeur de sécurité par défaut pour les blocs non répertoriés |
| 📦 Failsafe outil inconnu | Vitesse de "mains nus" pour les pioches non répertoriées |
| 🖱️ Micro-déplacements souris | Déplacement aléatoire de ±5 pixels après chaque bloc miné |
| ⏱️ Délais aléatoires | Facteur 0.8x à 1.2x appliqué au temps de minage |
| 🛑 Arrêt d'urgence | Touches `Q`, `F9` ou pause avec `F8` |

## ⚠️ Avertissements

- **Usage responsable** : Ce script est conçu pour un usage personnel en solo ou sur des serveurs autorisant l'automatisation
- **Risque de bannissement** : L'utilisation sur des serveurs publics sans autorisation peut entraîner un bannissement
- **Anti-cheat** : Certains serveurs disposent de systèmes anti-cheat avancés qui peuvent détecter l'automatisation
- **À vos risques** : L'auteur du script n'est pas responsable des conséquences de son utilisation

## 📁 Structure du projet

```
autominer/
├── autominer.py          # Script principal (boucle de minage)
├── mining_algorithm.py   # Algorithme modulaire de calcul du temps de minage
│   ├── BLOCKS_HARDNESS   # Dureté des blocs (50+ blocs vanilla + modded)
│   ├── TOOLS_SPEED       # Vitesse des pioches (35+ pioches vanilla + modded)
│   ├── UNBREAKABLE_BLOCKS# Liste des blocs incassables
│   └── get_mining_time() # Fonction principale de calcul
├── requirements.txt      # Dépendances Python
└── README.md             # Ce fichier
```

## 🔧 Dépannage

| Problème | Solution |
|----------|----------|
| Erreur `ModuleNotFoundError` | Vérifiez que les dépendances sont installées (`pip install -r requirements.txt`) |
| Erreur `ImportError` sur `mining_algorithm` | Vérifiez que `mining_algorithm.py` est dans le même dossier que `autominer.py` |
| Les clics ne fonctionnent pas dans Minecraft | Assurez-vous que le script est exécuté en tant qu'administrateur |
| La souris bouge de trop | Réduisez les valeurs `DEPLACEMENT_RANDOMISATION_MIN` et `DEPLACEMENT_RANDOMISATION_MAX` |
| Le minage est trop rapide/lent | Vérifiez `PIOCHE_ACTUELLE_ID` et assurez-vous qu'il correspond à votre pioche |
| Bloc non reconnu (alerte console) | Ajoutez le bloc dans `BLOCKS_HARDNESS` de `mining_algorithm.py` |

## 📝 Licence

Ce script est fourni à des fins éducatifs et d'usage personnel uniquement.

---

**Version**: 2.0  
**Auteur**: Cline (IA)  
**Minecraft**: 1.7.10 Moddé  
**Python requis**: 3.9+