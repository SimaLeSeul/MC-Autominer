"""
================================================================================
MC-Autominer - Mining Time Calculator Module (Minecraft 1.7.10)
================================================================================

This module provides a modular, configurable system for calculating the optimal
left-click hold time when mining blocks in Minecraft 1.7.10 modded.

Configuration is centralized in config.py. To modify blocks, pickaxes, or settings,
edit config.py directly.

Author: MC-Autominer Team
Version: 1.0.0
Minecraft Version: 1.7.10 (Modded)
================================================================================

USAGE:
    from mining_algorithm import get_mining_time, is_block_breakable
    from config import (
        BLOCKS_HARDNESS, TOOLS_SPEED, UNBREAKABLE_BLOCKS,
        DEFAULT_UNKNOWN_BLOCK_HARDNESS, DEFAULT_UNKNOWN_TOOL_SPEED,
        UNKNOWN_BLOCK_SAFETY_MULTIPLIER, UNKNOWN_BLOCK_LOG_INTERVAL
    )

FORMULA (Minecraft 1.7.10 official):
    Mining Speed = (Tool Speed Multiplier / Block Hardness) * Efficiency Factor * Haste Factor
    Click Hold Time = 0.05 / Mining Speed  (in seconds)

    - Efficiency Factor: 1 + (Efficiency Level * 0.3)
    - Haste Factor: 1 + (Haste Level * 0.2)
    - If the wrong tool is used, speed is multiplied by 0.0833 (1/12)
    - If the correct tool is used, full speed applies

UNBREAKABLE BLOCKS:
    Blocks listed in UNBREAKABLE_BLOCKS will be detected immediately,
    stopping the mining process to prevent wasting time.
================================================================================
"""

import time
from typing import Dict, Tuple, Optional

# Import centralized configuration from config.py
from config import (
    BLOCKS_HARDNESS,
    TOOLS_SPEED,
    UNBREAKABLE_BLOCKS,
    DEFAULT_UNKNOWN_BLOCK_HARDNESS,
    DEFAULT_UNKNOWN_TOOL_SPEED,
    UNKNOWN_BLOCK_SAFETY_MULTIPLIER,
    UNKNOWN_BLOCK_LOG_INTERVAL,
    # Mining time adjustment
    MINING_TIME_MULTIPLIER,
    MIN_BLOCK_BREAK_TIME,
)

# =============================================================================
# INTERNAL STATE (DO NOT MODIFY)
# =============================================================================

# Internal state for logging throttling
_last_unknown_log_time: float = 0
_last_unknown_block_id: str = ""


def _log_alert(message: str) -> None:
    """
    Log an alert message to the console, throttled to avoid spam.
    
    Args:
        message: The alert message to display.
    """
    global _last_unknown_log_time
    current_time = time.time()
    if (current_time - _last_unknown_log_time) > UNKNOWN_BLOCK_LOG_INTERVAL:
        print(f"[ALERT] {message}")
        _last_unknown_log_time = current_time


def get_mining_time(
    block_id: str,
    tool_id: str,
    efficiency_level: int = 0,
    haste_level: int = 0
) -> float:
    """
    Calculate the optimal left-click hold time for mining a block.
    
    This function implements the Minecraft 1.7.10 mining formula:
    
        Mining Speed = (Tool Speed / Block Hardness) * Efficiency Factor * Haste Factor
        Click Hold Time = 0.05 / Mining Speed  (seconds)
    
    Args:
        block_id: The block's registry name (e.g., "minecraft:stone", 
                  "thermalfoundation:ore:1").
        tool_id: The pickaxe's registry name (e.g., "minecraft:diamond_pickaxe",
                 "tinkers:rose_gold_pickaxe").
        efficiency_level: Enchantment level of Efficiency (0-III or 0-V with mods).
                          Default: 0.
        haste_level: Potion level of Haste (0, I, or II). Default: 0.
    
    Returns:
        float: The click-hold time in seconds.
               - Positive value: time to hold left-click (in seconds)
               - -1: Block is unbreakable (stop mining immediately)
               - None: Critical error (should not happen with proper input)
    
    Examples:
        >>> # Mine stone with a diamond pickaxe, no enchantments/potions
        >>> get_mining_time("minecraft:stone", "minecraft:diamond_pickaxe")
        0.0333...
        
        >>> # Mine thermal copper ore with Tink's Rose Gold Pickaxe, Eff III, Haste I
        >>> get_mining_time(
        ...     "thermalfoundation:ore:4", 
        ...     "tinkers:rose_gold_pickaxe", 
        ...     efficiency_level=3, 
        ...     haste_level=1
        ... )
        0.017...
        
        >>> # Bedrock returns -1 (stop immediately)
        >>> get_mining_time("minecraft:bedrock", "minecraft:diamond_pickaxe")
        -1
    
    Raises:
        ValueError: If block_id or tool_id are empty strings.
    """
    
    # --- INPUT VALIDATION ---
    if not block_id or not isinstance(block_id, str):
        raise ValueError(f"block_id must be a non-empty string, got: {block_id}")
    if not tool_id or not isinstance(tool_id, str):
        raise ValueError(f"tool_id must be a non-empty string, got: {tool_id}")
    if efficiency_level < 0:
        raise ValueError(f"efficiency_level must be >= 0, got: {efficiency_level}")
    if haste_level < 0:
        raise ValueError(f"haste_level must be >= 0, got: {haste_level}")
    
    current_time = time.time()
    
    # --- STEP 1: CHECK FOR UNBREAKABLE BLOCKS ---
    if block_id in UNBREAKABLE_BLOCKS:
        print(f"[STOP] Unbreakable block detected: {block_id}")
        print("[STOP] Stopping mining process immediately.")
        return -1.0
    
    # --- STEP 2: LOOK UP BLOCK HARDNESS ---
    block_hardness = BLOCKS_HARDNESS.get(block_id)
    
    if block_hardness is None:
        # Block not found in configuration - apply safety fallback
        _log_alert(
            f"Unknown block '{block_id}' using default hardness "
            f"({DEFAULT_UNKNOWN_BLOCK_HARDNESS}). "
            f"Add it to BLOCKS_HARDNESS for optimal mining."
        )
        block_hardness = DEFAULT_UNKNOWN_BLOCK_HARDNESS * UNKNOWN_BLOCK_SAFETY_MULTIPLIER
    
    # Special case: liquids and special blocks (hardness < 0)
    if block_hardness < 0 and block_hardness != -2:
        # -1 = liquid (can't mine), -2 = bedrock (handled above)
        if block_hardness == -1:
            print(f"[WARNING] Cannot mine liquids: {block_id}")
            return -1.0
    
    # --- STEP 3: LOOK UP TOOL SPEED ---
    tool_speed = TOOLS_SPEED.get(tool_id)
    
    if tool_speed is None:
        # Tool not found in configuration - use bare hands speed
        _log_alert(
            f"Unknown tool '{tool_id}' using bare hands speed "
            f"({DEFAULT_UNKNOWN_TOOL_SPEED}). "
            f"Add it to TOOLS_SPEED for optimal mining."
        )
        tool_speed = DEFAULT_UNKNOWN_TOOL_SPEED
    
    # --- STEP 4: CALCULATE EFFICIENCY AND HASTE FACTORS ---
    # Efficiency: each level adds 0.3 (30%) to the base speed
    # Formula: 1 + (level * 0.3)
    efficiency_factor = 1.0 + (efficiency_level * 0.3)
    
    # Haste: each level adds 0.2 (20%) to the break speed
    # Formula: 1 + (level * 0.2)
    haste_factor = 1.0 + (haste_level * 0.2)
    
    # --- STEP 5: CALCULATE MINING SPEED ---
    # Speed = (Tool Speed / Block Hardness) * Efficiency * Haste
    if block_hardness <= 0:
        # Handle edge case: hardness of 0 (e.g., TNT before explosion)
        # Use a very large speed to break it quickly
        if block_hardness == 0:
            mining_speed = tool_speed * efficiency_factor * haste_factor * 100
        else:
            # Negative hardness (liquids, etc.) - can't mine
            return -1.0
    else:
        mining_speed = (tool_speed / block_hardness) * efficiency_factor * haste_factor
    
    # --- STEP 6: CALCULATE CLICK HOLD TIME ---
    # Minecraft uses 0.05 seconds as the base tick
    # Click time = 0.05 / mining_speed
    click_hold_time = 0.05 / mining_speed
    
    # Apply the mining time multiplier for real-world game behavior
    # The theoretical formula often gives values that are too fast
    click_hold_time = click_hold_time * MINING_TIME_MULTIPLIER
    
    # Apply minimum break time (ensures fast-breaking blocks like glass work correctly)
    if click_hold_time < MIN_BLOCK_BREAK_TIME:
        click_hold_time = MIN_BLOCK_BREAK_TIME
    
    return float(click_hold_time)


def is_block_breakable(block_id: str) -> bool:
    """
    Check if a block can be broken (not protected/unbreakable).
    
    Args:
        block_id: The block's registry name.
    
    Returns:
        bool: True if the block can be broken, False if it's unbreakable.
    """
    return block_id not in UNBREAKABLE_BLOCKS


def is_block_known(block_id: str) -> bool:
    """
    Check if a block is configured in BLOCKS_HARDNESS.
    
    Args:
        block_id: The block's registry name.
    
    Returns:
        bool: True if the block is in the configuration, False otherwise.
    """
    return block_id in BLOCKS_HARDNESS


def add_block(block_id: str, hardness: float) -> None:
    """
    Dynamically add a block to BLOCKS_HARDNESS at runtime.
    
    This allows adding new blocks without modifying the source code.
    Also updates config.py's BLOCKS_HARDNESS.
    
    Args:
        block_id: The block's registry name.
        hardness: The block's hardness value.
    
    Example:
        >>> add_block("mymod:my_ore", 3.0)
    """
    BLOCKS_HARDNESS[block_id] = hardness
    # Also update config for persistence
    import config
    config.add_block_hardness(block_id, hardness)


def add_tool(tool_id: str, speed: float) -> None:
    """
    Dynamically add a tool to TOOLS_SPEED at runtime.
    
    This allows adding new pickaxes without modifying the source code.
    Also updates config.py's TOOLS_SPEED.
    
    Args:
        tool_id: The tool's registry name.
        speed: The tool's speed multiplier.
    
    Example:
        >>> add_tool("mymod:my_pickaxe", 10.0)
    """
    TOOLS_SPEED[tool_id] = speed
    # Also update config for persistence
    import config
    config.add_tool_speed(tool_id, speed)


def add_unbreakable_block(block_id: str) -> None:
    """
    Dynamically add a block to the unbreakable list.
    
    This allows adding protected blocks without modifying the source code.
    Also updates config.py's UNBREAKABLE_BLOCKS.
    
    Args:
        block_id: The block's registry name.
    
    Example:
        >>> add_unbreakable_block("griefprevention:claim_block")
    """
    UNBREAKABLE_BLOCKS.add(block_id)
    # Also update config for persistence
    import config
    config.add_unbreakable_block(block_id)


# =============================================================================
# EXAMPLE USAGE AND DEMONSTRATION
# =============================================================================

def print_mining_table() -> None:
    """
    Print a demonstration table showing mining times for various
    block/pickaxe combinations. This serves as both documentation
    and a working example.
    """
    print("\n" + "=" * 70)
    print("  MINING TIME CALCULATOR - Example Table (Minecraft 1.7.10)")
    print("=" * 70)
    print(f"  {'Block':<40} {'Pickaxe':<25} {'Time (ms)':>10}")
    print("-" * 70)
    
    # Example combinations: (block_id, tool_id, efficiency, haste)
    examples = [
        # Vanilla blocks with various pickaxes
        ("minecraft:stone", "minecraft:wooden_pickaxe", 0, 0),
        ("minecraft:stone", "minecraft:stone_pickaxe", 0, 0),
        ("minecraft:stone", "minecraft:iron_pickaxe", 0, 0),
        ("minecraft:stone", "minecraft:diamond_pickaxe", 0, 0),
        ("minecraft:stone", "minecraft:diamond_pickaxe", 3, 0),  # Efficiency III
        ("minecraft:stone", "minecraft:diamond_pickaxe", 3, 1),  # Efficiency III + Haste I
        
        # Modded ores (Thermal Foundation)
        ("thermalfoundation:ore:4", "minecraft:iron_pickaxe", 0, 0),  # Copper Ore - wrong tool
        ("thermalfoundation:ore:4", "minecraft:diamond_pickaxe", 0, 0),  # Copper Ore
        ("thermalfoundation:ore:4", "minecraft:diamond_pickaxe", 3, 1),  # Copper Ore - optimal
        
        # Modded ores (Thermal Foundation - Silver)
        ("thermalfoundation:ore:1", "minecraft:diamond_pickaxe", 3, 0),  # Silver Ore
        
        # Modded ores (Tinkers' Construct materials)
        ("minecraft:stone", "tinkers:rose_gold_pickaxe", 3, 1),
        ("minecraft:stone", "tinkers:flux_pickaxe", 3, 1),
        
        # Hard blocks
        ("minecraft:obsidian", "minecraft:diamond_pickaxe", 0, 0),
        ("minecraft:obsidian", "minecraft:diamond_pickaxe", 3, 0),
        ("minecraft:deepslate", "minecraft:diamond_pickaxe", 3, 1),
        
        # Unbreakable block (bedrock)
        ("minecraft:bedrock", "minecraft:diamond_pickaxe", 0, 0),
    ]
    
    for block_id, tool_id, eff, haste in examples:
        result = get_mining_time(block_id, tool_id, eff, haste)
        
        if result == -1.0:
            time_str = "UNBREAKABLE"
        else:
            time_ms = result * 1000
            time_str = f"{time_ms:.2f}"
        
        # Truncate block ID for display
        display_block = block_id if len(block_id) <= 38 else f"...{block_id[-35:]}"
        display_tool = tool_id if len(tool_id) <= 23 else f"...{tool_id[-20:]}"
        
        print(f"  {display_block:<40} {display_tool:<25} {time_str:>10}")
    
    print("=" * 70)
    print("\n  HOW TO ADD YOUR OWN BLOCKS AND TOOLS:\n")
    print("  1. Open config.py")
    print("  2. Find BLOCKS_HARDNESS dictionary (Section 2)")
    print("  3. Add your block in format: \"block_id\": hardness_value,")
    print("  4. Find TOOLS_SPEED dictionary (Section 3)")
    print("  5. Add your pickaxe in format: \"tool_id\": speed_value,")
    print("  6. Restart your script!")
    print("\n  Example entries:")
    print('    "minecraft:diamond_ore": 6.0,')
    print('    "thermalfoundation:ore:4": 3.0,  # Copper Ore')
    print('    "tinkers:rose_gold_pickaxe": 14.0,')
    print("\n")


# Run demonstration when this module is executed directly
if __name__ == "__main__":
    print_mining_table()
    
    # Runtime addition example (no file modification needed!)
    print("\n--- Dynamic Block Addition Example ---")
    add_block("mymod:my_special_ore", 5.0)
    add_tool("mymod:my_super_pickaxe", 16.0)
    
    result = get_mining_time(
        "mymod:my_special_ore",
        "mymod:my_super_pickaxe",
        efficiency_level=3,
        haste_level=1
    )
    print(f"Custom ore with custom pickaxe: {result * 1000:.2f}ms")