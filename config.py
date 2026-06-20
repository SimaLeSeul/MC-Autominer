"""
================================================================================
MC-Autominer - Centralized Configuration Module (Minecraft 1.7.10)
================================================================================

This module centralizes ALL configuration from the MC-Autominer project.
All scripts (autominer.py, mining_algorithm.py, block_detector.py) import
from this single file for consistent settings.

Author: MC-Autominer Team
Version: 1.0.0
Minecraft Version: 1.7.10 (Modded with WAILA)
================================================================================

USAGE:
    from config import (
        # Mining configuration
        PIOCHE_ACTUELLE_ID,
        NIVEAU_EFFECTIVITE,
        NIVEAU_HASTE,
        BLOCKS_HARDNESS,
        TOOLS_SPEED,
        
        # Block detection configuration
        WAILA_ROI,
        SCREEN_RESOLUTION,
        
        # Automation configuration
        DIST,
        ACTIVER_RANDOMISATION_SOURIS,
        # ... etc
    )

================================================================================
"""

# =============================================================================
# SECTION 1: AUTOMATION CONFIGURATION (autominer.py settings)
# =============================================================================

# --- CALIBRAGE MOUVEMENTS DE SOURIS ---
# Ajuste cette valeur (en pixels) selon ta sensibilité en jeu.
# Le but est qu'un déplacement de "DIST" déplace ton curseur d'exactement 1 bloc.
DIST = 225

# --- RANDOMISATION MOUVEMENTS SOURIS (ANTI-DETECTION) ---
# Ajoute un léger mouvement aléatoire aux déplacements pour éviter la détection
ACTIVER_RANDOMISATION_SOURIS = True
DEPLACEMENT_RANDOMISATION_MIN = -5   # Déplacement minimum en X (pixels)
DEPLACEMENT_RANDOMISATION_MAX = 5    # Déplacement maximum en X (pixels)

# --- RANDOMISATION DELAIS (ANTI-DETECTION) ---
# Ajoute un facteur aléatoire aux temps de minage pour simuler un comportement humain
ACTIVER_RANDOMISATION_DELAI = True
DELAI_RANDOMISATION_MIN = 0.8   # Facteur minimal (ex: 0.8 = 20% plus rapide)
DELAI_RANDOMISATION_MAX = 1.2   # Facteur maximal (ex: 1.2 = 20% plus lent)

# --- PIOCHE ACTUELLE ---
# Changez cet ID pour correspondre à votre pioche actuelle.
# Voir TOOLS_SPEED ci-dessous pour la liste complète des pioches supportées.
PIOCHE_ACTUELLE_ID = "minecraft:stone_pickaxe"

# --- NIVEAU ENCHANTMENT EFFICIENCY ---
# Niveaux possibles: 0, I, II, ou III
NIVEAU_EFFECTIVITE = 0

# --- NIVEAU POTION HASTE ---
# Niveaux possibles: 0, I, ou II
NIVEAU_HASTE = 0

# --- DETECTION OCR ACTIVEE ---
# Activer la détection de blocs par OCR (WAILA)
# Si False, utilise les block_id hardcodés dans autominer.py
ACTIVER_DETECTION_OCR = True

# =============================================================================
# SECTION 2: BLOC HARDNESS CONFIGURATION (mining_algorithm.py)
# =============================================================================
# Format: "block_id": hardness_value
#
# To add a new block:
#   1. Find the block's registry name using F3 in-game (look for "Name:" or block ID)
#   2. Look up its hardness value on the Minecraft Wiki
#   3. Add it in the format below (modded blocks use mod-specific prefixes)
#
# NOTES:
#   - Vanilla blocks use "minecraft:" prefix (e.g., "minecraft:stone")
#   - Modded blocks use their mod's prefix (e.g., "thermalfoundation:ore:1")
#   - Some blocks have metadata suffixes (:1, :2, etc.) - include them if needed
#   - Hardness values are floats (use decimals, e.g., 3.0, 1.5)

BLOCKS_HARDNESS: dict = {
    # --- VANILLA BLOCKS ---
    "minecraft:stone": 1.6,
    "minecraft:cobblestone": 1.5,
    "minecraft:deepslate": 3.0,
    "minecraft:obsidian": 50.0,
    "minecraft:iron_ore": 3.0,
    "minecraft:gold_ore": 3.0,
    "minecraft:diamond_ore": 6.0,
    "minecraft:emerald_ore": 6.0,
    "minecraft:redstone_ore": 3.0,
    "minecraft:lapis_ore": 3.0,
    "minecraft:coal_ore": 3.0,
    "minecraft:glass": 0.3,
    "minecraft:sand": 0.5,
    "minecraft:gravel": 0.6,
    "minecraft:iron_block": 6.0,
    "minecraft:gold_block": 6.0,
    "minecraft:diamond_block": 6.0,
    "minecraft:coal_block": 5.0,
    "minecraft:copper_block": 6.0,
    "minecraft:tnt": 0.0,   # Special case: explodes immediately
    "minecraft:lava": -1,   # Special value: unbreakable (liquid)
    "minecraft:water": -1,  # Special value: unbreakable (liquid)
    
    # --- BEDROCK (UNBREAKABLE) ---
    "minecraft:bedrock": -2,  # Special value: absolutely unbreakable
    
    # --- THERMAL FOUNDATION ORES (Thermal Series Mod) ---
    # Format: thermalfoundation:ore:<metadata>
    # "thermalfoundation:ore:0": 3.0,   # Nickel Ore
    # "thermalfoundation:ore:1": 3.0,   # Silver Ore
    # "thermalfoundation:ore:2": 3.0,   # Tin Ore
    # "thermalfoundation:ore:3": 3.0,   # Lead Ore
    # "thermalfoundation:ore:4": 3.0,   # Copper Ore
    # "thermalfoundation:ore:5": 3.0,   # Coal Canker
    
    # --- DEFAULT FALLBACK ---
    # If a block is not found, this default hardness is used (safe fallback)
}

# =============================================================================
# SECTION 3: TOOL SPEED MULTIPLIER CONFIGURATION (mining_algorithm.py)
# =============================================================================
# Format: "tool_id": speed_multiplier
#
# To add a new pickaxe:
#   1. Find the tool's registry name using F3 in-game or your mod's catalog
#   2. Look up its pickaxe speed on the Minecraft Wiki or mod documentation
#   3. Add it in the format below
#
# NOTES:
#   - Vanilla pickaxe speeds (base):
#     - Wooden: 2.0
#     - Stone: 4.0
#     - Iron: 6.0
#     - Diamond: 8.0
#     - Netherite: 9.0 (added in later versions, may not apply to 1.7.10)
#   - Modded pickaxes have custom speeds based on their material

TOOLS_SPEED: dict = {
    # --- VANILLA PICKAXES ---
    "minecraft:wooden_pickaxe": 2.0,
    "minecraft:stone_pickaxe": 3.6,
    "minecraft:iron_pickaxe": 6.0,
    "minecraft:diamond_pickaxe": 8.0,
    "minecraft:golden_pickaxe": 12.0,  # Very fast but fragile
    
    # --- TINKER'S CONSTRUCT PICKAXES ---
    # Format: tinkers:<material>_pickaxe or tinkers:pickaxe
    "tinkers:wooden_pickaxe": 2.0,
    "tinkers:stone_pickaxe": 4.0,
    "tinkers:iron_pickaxe": 6.0,
    "tinkers:obsidian_pickaxe": 10.0,
    "tinkers:onyx_pickaxe": 12.0,
    "tinkers:rose_gold_pickaxe": 14.0,
    "tinkers:pig_iron_pickaxe": 5.0,
    "tinkers:copper_pickaxe": 6.0,
    "tinkers:bronze_pickaxe": 8.0,
    "tinkers:electrum_pickaxe": 10.0,
    "tinkers:flux_pickaxe": 12.0,
    "tinkers:niter_pickaxe": 10.0,
    
    # Tinkers' combined pickaxe (head + handle + binding)
    "tinkers:pickaxe": 8.0,  # Base speed, modified by materials
    
    # --- THERMAL SERIES PICKAXES ---
    # Thermal Expansion / Thermal Foundation
    "thermalfoundation:pickaxe:wood": 2.0,
    "thermalfoundation:pickaxe:stone": 4.0,
    "thermalfoundation:pickaxe:iron": 6.0,
    "thermalfoundation:pickaxe:gold": 12.0,
    "thermalfoundation:pickaxe:diamond": 8.0,
    "thermalfoundation:pickaxe:obsidian": 10.0,
    
    # Thermal Cultivation (newer mod)
    "thermal:pickaxe:wood": 2.0,
    "thermal:pickaxe:stone": 4.0,
    "thermal:pickaxe:iron": 6.0,
    "thermal:pickaxe:gold": 12.0,
    "thermal:pickaxe:diamond": 8.0,
    "thermal:pickaxe:obsidian": 10.0,
    
    # --- BUILDCKT PICKAXES ---
    "buildcraft:minecraft:231": 6.0,   # Refined Iron Pickaxe
    "buildcraft:minecraft:232": 8.0,   # Refined Diamond Pickaxe
    
    # --- IC2 PICKAXES ---
    "ic2:pickIron": 6.0,
    "ic2:pickGold": 12.0,
    "ic2:pickDiamond": 8.0,
    "ic2:pick_Carbon": 10.0,
    "ic2:pick_Netherite": 12.0,  # May not exist in 1.7.10 IC2 version
    
    # --- MODERN PICKAXES (if using compatibility mods) ---
    # Netherite from later version ports
    "minecraft:netherite_pickaxe": 9.0,
}

# =============================================================================
# SECTION 4: UNBREAKABLE BLOCKS LIST (mining_algorithm.py)
# =============================================================================
# Blocks listed here will STOP mining immediately.
# These are blocks that cannot or should not be broken.

UNBREAKABLE_BLOCKS: set = {
    "minecraft:bedrock",
    "minecraft:command_block",
    "minecraft:barrier",
    "minecraft:structure_block",
    "minecraft:jigsaw",
    "minecraft:structure_void",
    "minecraft:end_portal_frame",
    "minecraft:enchanting_table",
    "minecraft:brewing_stand",  # Sometimes protected
    # --- PROTECTED BLOCKS (add based on your server's protection mod) ---
    # "griefprevention:claim_block",
    # "factions:claim_block",
    # "essentials:spawn_protection",
}

# =============================================================================
# SECTION 5: DEFAULT VALUES & FAILSAFE (mining_algorithm.py)
# =============================================================================

# Default hardness for unknown blocks (safe, slow value)
DEFAULT_UNKNOWN_BLOCK_HARDNESS: float = 5.0

# Default tool speed for unknown tools
DEFAULT_UNKNOWN_TOOL_SPEED: float = 2.0  # Bare hands speed

# Safety multiplier: additional slowdown for unknown blocks (0.5 = 50% slower)
UNKNOWN_BLOCK_SAFETY_MULTIPLIER: float = 1.5

# Alert logging interval (seconds) - avoid spamming console for unknown blocks
UNKNOWN_BLOCK_LOG_INTERVAL: float = 30.0

# =============================================================================
# SECTION 5.1: MINING TIME ADJUSTMENT (IMPORTANT!)
# =============================================================================
# Le calcul théorique du temps de minage donne des valeurs trop rapides.
# Ce multiplicateur permet d'ajuster les temps réels pour qu'ils correspondent
# au comportement réel du jeu Minecraft 1.7.10.
#
# Formule: temps_reel = temps_theorique * MINING_TIME_MULTIPLIER
#
# Valeurs recommandées:
#   - 1.0 = Calcul théorique pur (souvent trop rapide)
#   - 3.0 = 3x plus lent (recommandé pour la stone)
#   - 5.0 = 5x plus lent (pour les mods avec débuff de vitesse)

# Multiplicateur de temps de minage (ajuste selon tes besoins)
# Augmente cette valeur si le bot casse les blocs trop vite
MINING_TIME_MULTIPLIER: float = 5

# Multiplicateur minimum par bloc (en secondes) - empêche les temps trop courts
# Utile pour les blocs très rapides (verre, sable, etc.)
MIN_BLOCK_BREAK_TIME: float = 0.15  # 150ms minimum par bloc

# =============================================================================
# SECTION 6: SCREEN CAPTURE & OCR CONFIGURATION (block_detector.py)
# =============================================================================

# --- SCREEN RESOLUTION ---
# Adjust to your actual screen resolution
SCREEN_RESOLUTION: dict = {
    "width": 2560,
    "height": 1440
}

# --- WAILA ROI (Region of Interest) COORDINATES ---
# These should enclose ONLY the text area of the WAILA popup
# Format: (x_offset, y_offset, width, height)
WAILA_ROI: dict = {
    "x": 1073,       # X offset from left edge of screen
    "y": 72,         # Y offset from top edge of screen (very top)
    "width": 418,   # Width of the capture area
    "height": 101    # Height of the capture area
}

# --- OCR PROCESSING SETTINGS ---
ENABLE_PREPROCESSING: bool = True
THRESHOLD_METHOD: str = "binary"  # Options: "binary", "adaptive"
BINARY_THRESHOLD_VALUE: int = 128
MORPH_KERNEL_SIZE: tuple = (3, 3)
DILATE_KERNEL_SIZE: tuple = (2, 2)

# --- TEXT PROCESSING SETTINGS ---
OCR_LANGUAGE: str = "eng"
TEXT_SEGMENTATION_MODE: str = "7"  # PSM 7 = single text line
CHARACTER_WHITELIST: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789- "

# --- BLOCK NAME MAPPING (WAILA names -> Minecraft IDs) ---
# Maps WAILA display names to Minecraft 1.7.10 block IDs
# Format: "WAILA_NAME": "minecraft:block_id"

WAILA_TO_MINECRAFT_BLOCK_MAPPING: dict = {
    # --- VANILLA BLOCKS ---
    "GRASS BLOCK": "minecraft:grass_block",
    "DIRT": "minecraft:dirt",
    "COBBLESTONE": "minecraft:cobblestone",
    "STONE": "minecraft:stone",
    "SAND": "minecraft:sand",
    "GRAVEL": "minecraft:gravel",
    "GLASS": "minecraft:glass",
    "LOG": "minecraft:oak_log",
    "LEAVES": "minecraft:leaves",
    "BEDROCK": "minecraft:bedrock",
    "COAL ORE": "minecraft:coal_ore",
    "IRON ORE": "minecraft:iron_ore",
    "GOLD ORE": "minecraft:gold_ore",
    "DIAMOND ORE": "minecraft:diamond_ore",
    "EMERALD ORE": "minecraft:emerald_ore",
    "REDSTONE ORE": "minecraft:redstone_ore",
    "LAPIS ORE": "minecraft:lapis_ore",
    "IRON BLOCK": "minecraft:iron_block",
    "GOLD BLOCK": "minecraft:gold_block",
    "DIAMOND BLOCK": "minecraft:diamond_block",
    "COAL BLOCK": "minecraft:coal_block",
    "COPPER BLOCK": "minecraft:copper_block",
    "TNT": "minecraft:tnt",
    "WATER": "minecraft:water",
    "LAVA": "minecraft:lava",
    "STONE BRICK": "minecraft:stone_bricks",
    "BRICK": "minecraft:brick_block",
    "MOSSY COBBLESTONE": "minecraft:mossy_cobblestone",
    "OBSIDIAN": "minecraft:obsidian",
    "ANVIL": "minecraft:anvil",
    "SPONGE": "minecraft:sponge",
    "GLOWSTONE": "minecraft:glowstone",
    "PORTAL": "minecraft:obsidian",  # Nether portal frame
    "ENCHANTING TABLE": "minecraft:enchanting_table",
    "BREWING STAND": "minecraft:brewing_stand",
    "CAULDRON": "minecraft:cauldron",
    "FLOWER POT": "minecraft:flower_pot",
    "BOOKSHELF": "minecraft:bookshelf",
    "CHEST": "minecraft:chest",
    "TRAPPED CHEST": "minecraft:trapped_chest",
    "DROPPER": "minecraft:dropper",
    "DISPENSER": "minecraft:dispenser",
    "FURNACE": "minecraft:furnace",
    "LANTERN": "minecraft:lantern",
    "SANDSTONE": "minecraft:sandstone",
    "SMOOTH SANDSTONE": "minecraft:smooth_sandstone",
    "SMOOTH STONE": "minecraft:smooth_stone",
    "STONE SLAB": "minecraft:stone_slab",
    "BRICK STAIRS": "minecraft:brick_stairs",
    "STONE BRICK STAIRS": "minecraft:stone_brick_stairs",
    "SANDSTONE STAIRS": "minecraft:sandstone_stairs",
    "COBBLESTONE STAIRS": "minecraft:cobblestone_stairs",
    "WOODEN STAIRS": "minecraft:oak_stairs",
    "WOODEN SLAB": "minecraft:wooden_slab",
    "IRON DOOR": "minecraft:iron_door",
    "WOODEN DOOR": "minecraft:wooden_door",
    "TRAPDOOR": "minecraft:trapdoor",
    "IRON BARS": "minecraft:iron_bars",
    "GLASS PANE": "minecraft:glass_pane",
    "FENCE": "minecraft:fence",
    "NETHER BRICK FENCE": "minecraft:nether_brick_fence",
    "REDSTONE WIRE": "minecraft:redstone_wire",
    "REDSTONE TORCH": "minecraft:redstone_torch",
    "RAIL": "minecraft:rail",
    "POWERED RAIL": "minecraft:powered_rail",
    "DETECTOR RAIL": "minecraft:detector_rail",
    "ACTIVATOR RAIL": "minecraft:activator_rail",
    "LEVER": "minecraft:lever",
    "STONE BUTTON": "minecraft:stone_button",
    "PRESSURE PLATE": "minecraft:stone_pressure_plate",
    "TRIPWIRE": "minecraft:tripwire",
    "CHEST MINECART": "minecraft:chest_minecart",
    "TNT MINECART": "minecraft:tnt_minecart",
    "COMMAND BLOCK": "minecraft:command_block",
    "END PORTAL FRAME": "minecraft:end_portal_frame",
    "END STONE": "minecraft:end_stone",
    "PURPUR BLOCK": "minecraft:purpur_block",
    "PURPUR PILLAR": "minecraft:purpur_pillar",
    "END ROD": "minecraft:end_rod",
    "SHULKER BOX": "minecraft:shulker_box",
    "BLACK SHULKER BOX": "minecraft:black_shulker_box",
    "BONE BLOCK": "minecraft:bone_block",
    "DIRT PATH": "minecraft:dirt_path",
    "SNOW": "minecraft:snow",
    "ICE": "minecraft:ice",
    "PACKED ICE": "minecraft:packed_ice",
    "BLUE ICE": "minecraft:blue_ice",
    "CLAY": "minecraft:clay",
    "PRISMARINE": "minecraft:prismarine",
    "PRISMARINE BRICKS": "minecraft:prismarine_bricks",
    "DARK PRISMARINE": "minecraft:dark_prismarine",
    "SEA LANTERN": "minecraft:sea_lantern",
    "DAYLIGHT DETECTOR": "minecraft:daylight_detection_sensor",
    "HOPPER": "minecraft:hopper",
    "NOTE BLOCK": "minecraft:noteblock",
    "JUKEBOX": "minecraft:jukebox",
    "PISTON": "minecraft:piston",
    "RABBIT FOOT": "minecraft:rabbit_foot",
    "MUSHROOM": "minecraft:brown_mushroom_block",
    "CACTUS": "minecraft:cactus",
    "SUGAR CANE": "minecraft:reeds",
    "REEDS": "minecraft:reeds",
    "BAMBOO": "minecraft:bamboo",
    "PUMPKIN": "minecraft:pumpkin",
    "CARVED PUMPKIN": "minecraft:jack_o_lantern",
    "MELON": "minecraft:melon_block",
    "MELON SLICE": "minecraft:melon",
    "VINE": "minecraft:vine",
    "WEB": "minecraft:cobweb",
    "PAINTING": "minecraft:painting",
    "EYE OF ENDER": "minecraft:eye_of_ender",
    "ENDER CHEST": "minecraft:ender_chest",
    "BEACON": "minecraft:beacon",
    "BARRIER": "minecraft:barrier",
    "STRUCTURE BLOCK": "minecraft:structure_block",
    "JIGSAW BLOCK": "minecraft:jigsaw",
    "STRUCTURE VOID": "minecraft:structure_void",
    "GOLDEN RAIL": "minecraft:powered_rail",
    
    # Fallbacks for modded ores
    "RUBY ORE": "minecraft:coal_ore",
    "SAPPHIRE ORE": "minecraft:coal_ore",
    "LUMBER": "minecraft:coal_ore",
    
    # --- THERMAL FOUNDATION ORES (Thermal Series Mod) ---
    "TIN ORE": "thermalfoundation:ore:2",
    "LEAD ORE": "thermalfoundation:ore:3",
    "COPPER ORE": "thermalfoundation:ore:4",
    "SILVER ORE": "thermalfoundation:ore:1",
    "NICKEL ORE": "thermalfoundation:ore:0",
    "IRONSTONE": "thermalfoundation:ore:0",
    "COAL CANKER": "thermalfoundation:ore:5",
    "BRASS BLOCK": "thermalfoundation:material:4",
    
    # --- IC2 ORES ---
    "BRONZE ORE": "ic2:oreBronze",
    "LEAD ORE IC2": "ic2:oreLead",
    "NICKEL IC2": "ic2:oreNickel",
    "SILVER IC2": "ic2:oreSilver",
    "TIN IC2": "ic2:oreTin",
    
    # --- TINKER'S CONSTRUCT MATERIALS ---
    "CRAFTING BLOCK": "tinkers:crafting",
    "SMELTER": "tinkers:smelter",
    "MELTER": "tinkers:melter",
    "ROUTER": "tinkers:router",
    "DRAIN": "tinkers:drain",
    "CASTING TABLE": "tinkers:casting_table",
    "CASTING VAULT": "tinkers:casting_vault",
    "BLACKSMITH TABLE": "tinkers:anvil",
    "ANVIL TINKERS": "tinkers:anvil",
}

# =============================================================================
# SECTION 7: BLOCK DETECTOR FAILSAFE SETTINGS (block_detector.py)
# =============================================================================

# Default mining time when block is unknown (seconds)
DEFAULT_UNKNOWN_BLOCK_MINING_TIME: float = 2.0

# Number of consecutive failed OCR attempts before giving up
CONSECUTIVE_FAILURE_THRESHOLD: int = 3

# Interval for logging OCR failures (to avoid spam)
OCR_FAILURE_LOG_INTERVAL: float = 30.0

# --- EVASIVE ACTION CONFIGURATION ---
ENABLE_EVASION: bool = True
EVASION_DURATION: float = 0.3  # seconds
EVASION_KEY: str = "D"  # Options: "A", "D", or "BOTH"

# =============================================================================
# SECTION 8: UTILITY FUNCTIONS FOR DYNAMIC CONFIG UPDATES
# =============================================================================

def add_block_hardness(block_id: str, hardness: float) -> None:
    """Dynamically add a block to BLOCKS_HARDNESS at runtime."""
    BLOCKS_HARDNESS[block_id] = hardness


def add_tool_speed(tool_id: str, speed: float) -> None:
    """Dynamically add a pickaxe to TOOLS_SPEED at runtime."""
    TOOLS_SPEED[tool_id] = speed


def add_unbreakable_block(block_id: str) -> None:
    """Dynamically add a block to UNBREAKABLE_BLOCKS."""
    UNBREAKABLE_BLOCKS.add(block_id)


def add_block_mapping(waila_name: str, minecraft_id: str) -> None:
    """Dynamically add a block mapping to WAILA_TO_MINECRAFT_BLOCK_MAPPING."""
    WAILA_TO_MINECRAFT_BLOCK_MAPPING[waila_name.upper()] = minecraft_id


# =============================================================================
# VALIDATION ON IMPORT (DO NOT MODIFY)
# =============================================================================

def _validate_config() -> None:
    """Validate configuration integrity on import."""
    errors = []
    
    # Validate ROI coordinates
    roi = WAILA_ROI
    if not all(k in roi for k in ["x", "y", "width", "height"]):
        errors.append("WAILA_ROI must contain 'x', 'y', 'width', 'height' keys.")
    else:
        if roi["x"] < 0 or roi["y"] < 0:
            errors.append("WAILA_ROI coordinates must be non-negative.")
        if roi["width"] <= 0 or roi["height"] <= 0:
            errors.append("WAILA_ROI dimensions must be positive.")
    
    # Validate screen resolution
    res = SCREEN_RESOLUTION
    if not all(k in res for k in ["width", "height"]):
        errors.append("SCREEN_RESOLUTION must contain 'width' and 'height' keys.")
    else:
        if res["width"] <= 0 or res["height"] <= 0:
            errors.append("Screen resolution dimensions must be positive.")
    
    # Validate thresholds
    if not 0 <= BINARY_THRESHOLD_VALUE <= 255:
        errors.append("BINARY_THRESHOLD_VALUE must be between 0 and 255.")
    
    # Validate threshold method
    if THRESHOLD_METHOD not in ["binary", "adaptive"]:
        errors.append(f"THRESHOLD_METHOD must be 'binary' or 'adaptive', got: {THRESHOLD_METHOD}")
    
    # Validate PSM mode
    if TEXT_SEGMENTATION_MODE not in ["3", "7", "13"]:
        errors.append(f"TEXT_SEGMENTATION_MODE must be '3', '7', or '13', got: {TEXT_SEGMENTATION_MODE}")
    
    # Validate evasion key
    if EVASION_KEY not in ["A", "D", "BOTH"]:
        errors.append(f"EVASION_KEY must be 'A', 'D', or 'BOTH', got: {EVASION_KEY}")
    
    # Validate efficiency and haste levels
    if NIVEAU_EFFECTIVITE not in [0, 1, 2, 3]:
        errors.append(f"NIVEAU_EFFECTIVITE must be 0, 1, 2, or 3, got: {NIVEAU_EFFECTIVITE}")
    if NIVEAU_HASTE not in [0, 1, 2]:
        errors.append(f"NIVEAU_HASTE must be 0, 1, or 2, got: {NIVEAU_HASTE}")
    
    if errors:
        print("=" * 60)
        print("  [ERROR] Configuration Validation Failed!")
        print("=" * 60)
        for error in errors:
            print(f"  - {error}")
        print("=" * 60)
        print("Please fix your config in config.py or the main config section.")
        print("Applying safe defaults for invalid values.")
        print()
        
        # Apply safe defaults for invalid values using module-level reassignment
        # Note: We cannot use 'global' here because these variables were already
        # referenced earlier in the function. Instead, we use exec() to modify
        # the module-level variables.
        import sys
        _current_module = sys.modules[__name__]
        
        # Set safe defaults using setattr on the module
        if not (0 <= getattr(_current_module, 'BINARY_THRESHOLD_VALUE', 0) <= 255):
            _current_module.BINARY_THRESHOLD_VALUE = 128
        if getattr(_current_module, 'THRESHOLD_METHOD', '') not in ["binary", "adaptive"]:
            _current_module.THRESHOLD_METHOD = "binary"
        if getattr(_current_module, 'TEXT_SEGMENTATION_MODE', '') not in ["3", "7", "13"]:
            _current_module.TEXT_SEGMENTATION_MODE = "7"
        if not (getattr(_current_module, 'NIVEAU_EFFECTIVITE', -1) in [0, 1, 2, 3]):
            _current_module.NIVEAU_EFFECTIVITE = 0
        if not (getattr(_current_module, 'NIVEAU_HASTE', -1) in [0, 1, 2]):
            _current_module.NIVEAU_HASTE = 0
        if getattr(_current_module, 'EVASION_KEY', '') not in ["A", "D", "BOTH"]:
            _current_module.EVASION_KEY = "D"


# Run validation on import
_validate_config()

# Print config summary on import (first time only)
_config_printed = False


def print_config_summary() -> None:
    """Print a summary of all loaded configuration."""
    global _config_printed
    if _config_printed:
        return
    _config_printed = True
    
    print("=" * 60)
    print("  MC-Autominer - Configuration Loaded Successfully")
    print("=" * 60)
    
    print("\n  --- Mining Configuration ---")
    print(f"  Pickaxe: {PIOCHE_ACTUELLE_ID}")
    print(f"  Efficiency: {NIVEAU_EFFECTIVITE}")
    print(f"  Haste: {NIVEAU_HASTE}")
    print(f"  Blocks configured: {len(BLOCKS_HARDNESS)}")
    print(f"  Tools configured: {len(TOOLS_SPEED)}")
    print(f"  Unbreakable blocks: {len(UNBREAKABLE_BLOCKS)}")
    
    print("\n  --- Block Detection (OCR) ---")
    print(f"  Enabled: {ACTIVER_DETECTION_OCR}")
    print(f"  Screen: {SCREEN_RESOLUTION['width']}x{SCREEN_RESOLUTION['height']}")
    print(f"  WAILA ROI: x={WAILA_ROI['x']}, y={WAILA_ROI['y']}, "
          f"w={WAILA_ROI['width']}, h={WAILA_ROI['height']}")
    print(f"  Block mappings: {len(WAILA_TO_MINECRAFT_BLOCK_MAPPING)}")
    print(f"  Threshold method: {THRESHOLD_METHOD}")
    print(f"  OCR Language: {OCR_LANGUAGE}")
    
    print("\n  --- Automation ---")
    print(f"  Mouse calibration distance: {DIST}px")
    print(f"  Mouse randomization: {ACTIVER_RANDOMISATION_SOURIS} "
          f"({DEPLACEMENT_RANDOMISATION_MIN} to {DEPLACEMENT_RANDOMISATION_MAX}px)")
    print(f"  Delay randomization: {ACTIVER_RANDOMISATION_DELAI} "
          f"({DELAI_RANDOMISATION_MIN}x to {DELAI_RANDOMISATION_MAX}x)")
    print(f"  Evasion: {ENABLE_EVASION} (key: {EVASION_KEY}, "
          f"duration: {EVASION_DURATION}s)")
    
    print("=" * 60)
    print()


# Auto-print config summary on first import
print_config_summary()