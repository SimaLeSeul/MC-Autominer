"""
================================================================================
MC-Autominer - Automated Mining Script (Minecraft 1.7.10)
================================================================================

This script handles the mining automation for Minecraft 1.7.10 modded.
It uses dynamic mining times based on block detection (OCR via WAILA)
and calculates optimal click-hold durations.

All configuration is centralized in config.py. To modify settings,
edit config.py directly.

Author: MC-Autominer Team
Version: 1.0.0
Minecraft Version: 1.7.10 (Modded with WAILA)
================================================================================

USAGE:
    python autominer.py
    
CONTROLS:
    F8  : Toggle mining on/off
    F9  : Stop script completely
    Q   : Emergency stop (release click and stop)

DEPENDENCIES:
    from config.py: All configuration (pickaxes, blocks, ROI, etc.)
    from mining_algorithm.py: get_mining_time(), is_block_breakable()
    from block_detector.py: BlockDetector (optional, for OCR detection)

================================================================================
"""

import time
import pydirectinput
import keyboard
import random

# Import centralized configuration from config.py
from config import (
    # Mining settings
    PIOCHE_ACTUELLE_ID,
    NIVEAU_EFFECTIVITE,
    NIVEAU_HASTE,
    # Automation settings
    DIST,
    ACTIVER_RANDOMISATION_SOURIS,
    DEPLACEMENT_RANDOMISATION_MIN,
    DEPLACEMENT_RANDOMISATION_MAX,
    ACTIVER_RANDOMISATION_DELAI,
    DELAI_RANDOMISATION_MIN,
    DELAI_RANDOMISATION_MAX,
    # Block detection settings
    ACTIVER_DETECTION_OCR,
    # Mining time adjustment
    MINING_TIME_MULTIPLIER,
    MIN_BLOCK_BREAK_TIME,
)
from mining_algorithm import get_mining_time, is_block_breakable
from block_detector import BlockDetector


# =============================================================================
# INITIALIZE BLOCK DETECTOR (if OCR detection is enabled)
# =============================================================================

detector: BlockDetector = None
if ACTIVER_DETECTION_OCR:
    print("[Autominer] Block detection (OCR) enabled. Initializing...")
    detector = BlockDetector()

print("\n==================================================")
print("  MC-Autominer - Script de minage 2x2 (tout droit) prêt !")
print("==================================================")
print(f"  Pioche: {PIOCHE_ACTUELLE_ID}")
print(f"  Effectivité: {NIVEAU_EFFECTIVITE} | Haste: {NIVEAU_HASTE}")
print(f"  Détection OCR: {'OUI' if ACTIVER_DETECTION_OCR else 'NON'}")
print(f"  Randomisation souris: {'OUI' if ACTIVER_RANDOMISATION_SOURIS else 'NON'}")
print(f"  Randomisation délai: {'OUI' if ACTIVER_RANDOMISATION_DELAI else 'NON'}")
print("  IMPORTANT : Aligne-toi bien (Pitch: 0, Yaw: fixe) via F3.")
print("  Appuie sur 'F8' pour ACTIVER / PAUSER le minage.")
print("  Appuie sur 'F9' pour ARRÊTER définitivement le script.")
print("  Appuie sur 'Q' pour ARRÊT D'URGENCE.")
print("==================================================\n")

active = False
arret_total = False

while True:
    # =============================================================================
    # GESTION DES TOUCHES DE CONTRÔLE
    # =============================================================================
    if keyboard.is_pressed('f8'):
        active = not active
        print("Statut :", "En cours..." if active else "En pause.")
        time.sleep(0.5)  # Anti-rebond
    
    if keyboard.is_pressed('f9'):
        print("Arrêt total du script.")
        pydirectinput.mouseUp()
        arret_total = True
        break
    
    # Arrêt d'urgence : relâche le clic et arrête
    if keyboard.is_pressed('q') and active:
        print("Arrêt d'urgence activé !")
        pydirectinput.mouseUp()
        time.sleep(0.5)
        arret_total = True

    if active and not arret_total:
        # =============================================================================
        # MINAGE 2x2 : 1 bloc au-dessus + 1 bloc en dessous (tout droit)
        # =============================================================================
        
        # On commence à miner (maintien du clic gauche)
        pydirectinput.mouseDown()
        
        # =============================================================================
        # BLOC DU HAUT - CALCUL DU TEMPS DE MINAGE AVANT MOUVEMENT
        # =============================================================================
        # On calcule d'abord le temps de minage nécessaire, puis on effectue
        # le mouvement de la caméra en tenant compte de ce temps.
        
        # Détection du bloc (si OCR activé)
        if detector and ACTIVER_DETECTION_OCR:
            block_id_haut = detector.detect_block()
            if block_id_haut is None:
                block_id_haut = "minecraft:stone"
                print("[Autominer] Détection incertaine, utilisation du bloc par défaut: minecraft:stone")
        else:
            block_id_haut = "minecraft:stone"
        
        # Calcul du temps de minage AVEC multiplicateur et minimum
        temps_theorique = get_mining_time(
            block_id_haut,
            PIOCHE_ACTUELLE_ID,
            NIVEAU_EFFECTIVITE,
            NIVEAU_HASTE
        )
        
        if temps_theorique == -1.0:
            pydirectinput.mouseUp()
            print(f"\n[STOP] Bloc incassable/protégé détecté: {block_id_haut}")
            print("[STOP] Le script a arrêté le minage immédiatement.")
            arret_total = True
            break
        
        # Appliquer le multiplicateur et le minimum
        temps_minage_haut = temps_theorique * MINING_TIME_MULTIPLIER
        if temps_minage_haut < MIN_BLOCK_BREAK_TIME:
            temps_minage_haut = MIN_BLOCK_BREAK_TIME
        
        # Avec randomisation (anti-détection)
        if ACTIVER_RANDOMISATION_DELAI:
            temps_minage_haut = temps_minage_haut * random.uniform(DELAI_RANDOMISATION_MIN, DELAI_RANDOMISATION_MAX)
        
        # =============================================================================
        # MOUVEMENT VERS LE BLOC DU HAUT + CALCUL DU TEMPS RESTANT
        # =============================================================================
        # Le mouvement de la caméra prend du temps. On mesure ce temps
        # et on soustrait ce temps au temps de minage total.
        
        y_haut = -DIST
        
        # Mesure le temps de début de mouvement
        movement_start = time.time()
        
        if ACTIVER_RANDOMISATION_SOURIS:
            random_x = random.randint(DEPLACEMENT_RANDOMISATION_MIN, DEPLACEMENT_RANDOMISATION_MAX)
            random_y_compense = -random_x
            pydirectinput.move(random_x, y_haut + random_y_compense)
        else:
            pydirectinput.move(0, y_haut)
        
        # Position : Haut-Centre (au-dessus du crosshair)
        # Calcule le temps réel pris par le mouvement
        movement_time_haut = time.time() - movement_start
        
        # Temps de minage restant après le mouvement
        temps_restant_haut = temps_minage_haut - movement_time_haut
        
        # Si le mouvement est plus long que le temps de minage, pas d'attente supplémentaire
        if temps_restant_haut > 0:
            time.sleep(temps_restant_haut)
        
        # =============================================================================
        # BLOC DU BAS - CALCUL DU TEMPS DE MINAGE AVANT MOUVEMENT
        # =============================================================================
        
        # Détection du bloc (si OCR activé)
        if detector and ACTIVER_DETECTION_OCR:
            block_id_bas = detector.detect_block()
            if block_id_bas is None:
                block_id_bas = "minecraft:stone"
                print("[Autominer] Détection incertaine, utilisation du bloc par défaut: minecraft:stone")
        else:
            block_id_bas = "minecraft:stone"
        
        # Calcul du temps de minage AVEC multiplicateur et minimum
        temps_theorique_bas = get_mining_time(
            block_id_bas,
            PIOCHE_ACTUELLE_ID,
            NIVEAU_EFFECTIVITE,
            NIVEAU_HASTE
        )
        
        if temps_theorique_bas == -1.0:
            pydirectinput.mouseUp()
            print(f"\n[STOP] Bloc incassable/protégé détecté: {block_id_bas}")
            print("[STOP] Le script a arrêté le minage immédiatement.")
            arret_total = True
            break
        
        # Appliquer le multiplicateur et le minimum
        temps_minage_bas = temps_theorique_bas * MINING_TIME_MULTIPLIER
        if temps_minage_bas < MIN_BLOCK_BREAK_TIME:
            temps_minage_bas = MIN_BLOCK_BREAK_TIME
        
        # Avec randomisation (anti-détection)
        if ACTIVER_RANDOMISATION_DELAI:
            temps_minage_bas = temps_minage_bas * random.uniform(DELAI_RANDOMISATION_MIN, DELAI_RANDOMISATION_MAX)
        
        # =============================================================================
        # MOUVEMENT VERS LE BLOC DU BAS + CALCUL DU TEMPS RESTANT
        # =============================================================================
        y_bas = DIST
        
        # Mesure le temps de début de mouvement
        movement_start = time.time()
        
        if ACTIVER_RANDOMISATION_SOURIS:
            random_x = random.randint(DEPLACEMENT_RANDOMISATION_MIN, DEPLACEMENT_RANDOMISATION_MAX)
            random_y_compense = -random_x
            pydirectinput.move(random_x, y_bas + random_y_compense)
        else:
            pydirectinput.move(0, y_bas)
        
        # Calcule le temps réel pris par le mouvement
        movement_time_bas = time.time() - movement_start
        
        # Temps de minage restant après le mouvement
        temps_restant_bas = temps_minage_bas - movement_time_bas
        
        # Si le mouvement est plus long que le temps de minage, pas d'attente supplémentaire
        if temps_restant_bas > 0:
            time.sleep(temps_restant_bas)
        
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