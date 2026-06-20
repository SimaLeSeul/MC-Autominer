import time
import pydirectinput
import keyboard
import random

# =============================================================================
# CONFIGURATION DU CALIBRAGE
# =============================================================================

# Ajuste cette valeur (en pixels) selon ta sensibilité en jeu.
# Le but est qu'un déplacement de "DIST" déplace ton curseur d'exactement 1 bloc.
DIST = 225

# Temps (en secondes) pour casser un bloc.
# Augmente cette valeur si tu mines de la pierre profonde (Deepslate) ou si ta pioche est lente.
TEMPS_MINAGE = 0.7

# =============================================================================
# CONFIGURATION DE LA RANDOMISATION (ANTI-DETECTION)
# =============================================================================

# Randomisation des mouvements de souris (anti-détection)
# Ajoute un léger mouvement aléatoire aux déplacements pour éviter la détection
ACTIVER_RANDOMISATION_SOURIS = True
DEPLACEMENT_RANDOMISATION_MIN = -5  # Déplacement minimum en X (pixels)
DEPLACEMENT_RANDOMISATION_MAX = 5   # Déplacement maximum en X (pixels)

# Randomisation des délais (anti-détection)
# Ajoute un facteur aléatoire aux temps de minage pour simuler un comportement humain
ACTIVER_RANDOMISATION_DELAI = True
DELAI_RANDOMISATION_MIN = 0.8  # Facteur minimal (ex: 0.8 = 20% plus rapide)
DELAI_RANDOMISATION_MAX = 1.2  # Facteur maximal (ex: 1.2 = 20% plus lent)

# =============================================================================
# TOUCHES DE CONTRÔLE
# =============================================================================
# F8 : ACTIVER / PAUSER le minage
# F9 : ARRÊTER définitivement le script
# Q  : ARRÊT D'URGENCE (relâche le clic et arrête)

print("==================================================")
print("-> Script de minage 2x2 (tout droit) prêt !")
print("-> Minage : 1 bloc au-dessus + 1 bloc en dessous")
print("-> Randomisation activée (mouvements + délais)")
print("-> IMPORTANT : Aligne-toi bien (Pitch: 0, Yaw: fixe) via F3.")
print("-> Appuie sur 'F8' pour ACTIVER / PAUSER le minage.")
print("-> Appuie sur 'F9' pour ARRÊTER définitivement le script.")
print("-> Appuie sur 'Q' pour ARRÊT D'URGENCE.")
print("==================================================")

active = False

while True:
    # Gestion des touches de contrôle
    if keyboard.is_pressed('f8'):
        active = not active
        print("Statut :", "En cours..." if active else "En pause.")
        time.sleep(0.5) # Anti-rebond
    
    if keyboard.is_pressed('f9'):
        print("Arrêt total du script.")
        pydirectinput.mouseUp()
        break
    
    # Arrêt d'urgence : relâche le clic et arrête
    if keyboard.is_pressed('q') and active:
        print("Arrêt d'urgence activé !")
        pydirectinput.mouseUp()
        time.sleep(0.5)

    if active:
        # =============================================================================
        # MINAGE 2x2 : 1 bloc au-dessus + 1 bloc en dessous (tout droit)
        # =============================================================================
        
        # On commence à miner (maintien du clic gauche)
        pydirectinput.mouseDown()
        
        # --- BLOC DU HAUT (au-dessus du crosshair) ---
        # Déplacement vers le haut avec randomisation
        y_haut = -DIST
        
        if ACTIVER_RANDOMISATION_SOURIS:
            # Applique une randomisation sur X, puis son inverse sur Y pour compenser
            random_x = random.randint(DEPLACEMENT_RANDOMISATION_MIN, DEPLACEMENT_RANDOMISATION_MAX)
            random_y_compense = -random_x  # L'inverse de random_x annule l'effet
            pydirectinput.move(random_x, y_haut + random_y_compense)
        else:
            pydirectinput.move(0, y_haut)
        
        # Position : Haut-Centre (au-dessus du crosshair)
        
        # Temps de minage avec randomisation
        temps_reel = TEMPS_MINAGE * random.uniform(DELAI_RANDOMISATION_MIN, DELAI_RANDOMISATION_MAX)
        time.sleep(temps_reel)
        
        # --- BLOC DU BAS (en dessous du crosshair) ---
        # Déplacement vers le bas avec randomisation
        y_bas = DIST
        
        if ACTIVER_RANDOMISATION_SOURIS:
            # Applique une randomisation sur X, puis son inverse sur Y pour compenser
            random_x = random.randint(DEPLACEMENT_RANDOMISATION_MIN, DEPLACEMENT_RANDOMISATION_MAX)
            random_y_compense = -random_x  # L'inverse de random_x annule l'effet
            pydirectinput.move(random_x, y_bas + random_y_compense)
        else:
            pydirectinput.move(0, y_bas)
        
        # Position : Bas-Centre (en dessous du crosshair)
        
        # Temps de minage avec randomisation
        temps_reel = TEMPS_MINAGE * random.uniform(DELAI_RANDOMISATION_MIN, DELAI_RANDOMISATION_MAX)
        time.sleep(temps_reel)
        
        # =============================================================================
        # RECENTRAGE ET AVANCÉE
        # =============================================================================
        
        # Retour au centre avec randomisation compensée
        if ACTIVER_RANDOMISATION_SOURIS:
            # Applique une randomisation sur X, puis son inverse sur Y pour compenser
            random_x = random.randint(DEPLACEMENT_RANDOMISATION_MIN, DEPLACEMENT_RANDOMISATION_MAX)
            random_y_compense = -random_x  # L'inverse de random_x annule l'effet
            pydirectinput.move(random_x, random_y_compense)
        else:
            pydirectinput.move(0, 0)  # Déjà au centre
        
        pydirectinput.mouseUp()  # On relâche le clic
        time.sleep(0.1)
        
        # Avancer d'un bloc (maintien court de la touche W)
        # Délai aléatoire avant l'avance
        delai_avance = random.uniform(0.2, 0.5)
        time.sleep(delai_avance)
        
        pydirectinput.keyDown('w')
        time.sleep(0.25)
        pydirectinput.keyUp('w')
        
        # Petite pause de sécurité pour stabiliser la position
        time.sleep(0.4)
        
    time.sleep(0.05)