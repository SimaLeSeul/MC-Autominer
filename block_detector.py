"""
================================================================================
MC-Autominer - Block Detection Module (Minecraft 1.7.10)
================================================================================

This module provides real-time block detection using computer vision and OCR.
It captures the WAILA (What Am I Looking At) info box, processes the image,
and extracts the block name using Tesseract OCR.

Works with:
  - autominer.py (handles mining actions)
  - mining_algorithm.py (calculates mining times)
  - config.py (centralized configuration)

Author: MC-Autominer Team
Version: 1.0.0
Minecraft Version: 1.7.10 (Modded with WAILA)
================================================================================

REQUIREMENTS:
    pip install mss opencv-python pytesseract numpy

INSTALLATION:
    1. Install Python dependencies: pip install mss opencv-python pytesseract numpy
    2. Install Tesseract OCR: https://github.com/UB-Mannheim/tesseract/wiki
    3. Add WAILA mod to your Minecraft 1.7.10 client
    4. Configure WAILA to display block name (top-center popup)
    5. Adjust ROI coordinates in config.py

USAGE:
    from block_detector import BlockDetector
    from config import WAILA_ROI
    
    detector = BlockDetector()
    block_id = detector.detect_block()
    
    if block_id:
        print(f"Detected: {block_id}")
    else:
        print("Unknown block or detection failed")

================================================================================
"""

import mss
import mss.tools
import cv2
import numpy as np
import pytesseract
import time
import re
import os
import subprocess
from typing import Optional, Dict, Tuple

# =============================================================================
# TESSERACT OCR CONFIGURATION
# =============================================================================
# Chemins possibles pour tesseract.exe sur Windows
# Le premier trouvé sera utilisé automatiquement
_TESSERACT_PATHS = [
    r'C:\Program Files\Tesseract-OCR\tesseract.exe',
    r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe',
    r'C:\Users\Michael\AppData\Local\Programs\Tesseract-OCR\tesseract.exe',
]

# Trouver automatiquement Tesseract ou définir un chemin par défaut
_TESSERACT_CMD = None
for _path in _TESSERACT_PATHS:
    if os.path.exists(_path):
        _TESSERACT_CMD = _path
        break

# Si Tesseract n'est pas trouvé, on définit None et on gère l'erreur dans extract_text()
if _TESSERACT_CMD:
    pytesseract.pytesseract.tesseract_cmd = _TESSERACT_CMD
    print(f"[BlockDetector] Tesseract trouvé: {_TESSERACT_CMD}")
else:
    print("[BlockDetector] ATTENTION: Tesseract n'est pas installé ou n'a pas été trouvé.")
    print("[BlockDetector] Le bot fonctionnera en mode dégradé (bloc par défaut: minecraft:stone).")
    print("[BlockDetector] Pour activer la détection OCR, installe Tesseract :")
    print("[BlockDetector]   1. Télécharge: https://github.com/UB-Mannheim/tesseract/wiki")
    print("[BlockDetector]   2. Installe dans C:\\Program Files\\Tesseract-OCR\\")
    print("[BlockDetector]   3. Redémarre le script")

# Import centralized configuration from config.py
from config import (
    # Block mapping
    WAILA_TO_MINECRAFT_BLOCK_MAPPING,
    # ROI configuration
    WAILA_ROI,
    SCREEN_RESOLUTION,
    # OCR settings
    ENABLE_PREPROCESSING,
    THRESHOLD_METHOD,
    BINARY_THRESHOLD_VALUE,
    MORPH_KERNEL_SIZE,
    DILATE_KERNEL_SIZE,
    OCR_LANGUAGE,
    TEXT_SEGMENTATION_MODE,
    CHARACTER_WHITELIST,
    # Failsafe settings
    DEFAULT_UNKNOWN_BLOCK_MINING_TIME,
    CONSECUTIVE_FAILURE_THRESHOLD,
    OCR_FAILURE_LOG_INTERVAL,
    # Evasion settings
    ENABLE_EVASION,
    EVASION_DURATION,
    EVASION_KEY,
    # Mining algorithm
)
from mining_algorithm import get_mining_time, is_block_breakable


# =============================================================================
# CORE BLOCK DETECTION CLASS
# =============================================================================

class BlockDetector:
    """
    High-performance block detection module using screen capture and OCR.
    
    This class captures the WAILA info box area from the screen,
    processes the image using OpenCV, and extracts block names via Tesseract OCR.
    
    Configuration is centralized in config.py. To modify detection settings,
    edit config.py directly.
    
    Usage:
        detector = BlockDetector()
        block_id = detector.detect_block()
        
    Attributes:
        roi: Region of Interest configuration for screen capture
        mapping: Dictionary mapping WAILA names to Minecraft block IDs
    """
    
    def __init__(self, roi: Optional[Dict] = None, mapping: Optional[Dict] = None):
        """
        Initialize the BlockDetector with ROI and block mapping configuration.
        
        Args:
            roi: Region of Interest dictionary. If None, uses config.py WAILA_ROI.
                 Format: {"x": int, "y": int, "width": int, "height": int}
            mapping: Block name mapping dictionary. If None, uses config.py mapping.
        """
        self.roi = roi or WAILA_ROI
        self.mapping = mapping or WAILA_TO_MINECRAFT_BLOCK_MAPPING
        
        # Create screen capture area
        self.sct_monitor = mss.mss()
        self.monitor = {
            "top": self.roi["y"],
            "left": self.roi["x"],
            "width": self.roi["width"],
            "height": self.roi["height"]
        }
        
        # Tesseract configuration
        # Note: --whitelist was removed in Tesseract 5.x+, use oem 1 instead
        self.tesseract_config = f'--psm {TEXT_SEGMENTATION_MODE} --oem 1 -l {OCR_LANGUAGE}'
        
        print("[BlockDetector] Initialized successfully.")
        print(f"  ROI: x={self.roi['x']}, y={self.roi['y']}, "
              f"w={self.roi['width']}, h={self.roi['height']}")
        print(f"  Mapping entries: {len(self.mapping)}")
        print(f"  Threshold method: {THRESHOLD_METHOD}")
    
    def capture_screen(self) -> Optional[np.ndarray]:
        """
        Capture the screen region of interest (WAILA info box area).
        
        This method uses mss for ultra-fast screen capture, targeting
        ONLY the WAILA popup area to minimize CPU usage.
        
        Returns:
            numpy.ndarray: The captured screen region as a numpy array (BGR format),
                          or None if capture fails.
        """
        try:
            # Capture only the WAILA area (not the entire screen!)
            screenshot = self.sct_monitor.grab(self.monitor)
            
            # Convert to OpenCV image (numpy array)
            # mss returns BGRA format, we need BGR for OpenCV
            img = np.array(screenshot)
            
            # Handle different bit depths
            if len(img.shape) == 3 and img.shape[2] == 4:
                # BGRA to BGR (remove alpha channel)
                # Use COLOR_BGRA2BGR for OpenCV 4.10+ compatibility
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
            elif len(img.shape) == 2:
                # Grayscale image (single channel)
                img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
            
            return img
            
        except Exception as e:
            print(f"[BlockDetector] Screen capture failed: {str(e)}")
            return None
    
    def preprocess_image(self, img: np.ndarray) -> np.ndarray:
        """
        Preprocess the captured image for optimal OCR recognition.
        
        Steps:
        1. Convert to grayscale
        2. Apply thresholding (binary or adaptive)
        3. Apply morphological operations to connect text parts
        4. Noise reduction
        
        Configuration is centralized in config.py.
        
        Args:
            img: Raw captured image from capture_screen()
            
        Returns:
            np.ndarray: Preprocessed binary image optimized for OCR
        """
        if not ENABLE_PREPROCESSING:
            return img
        
        # Step 1: Convert to grayscale (always enabled)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Step 2: Apply thresholding
        if THRESHOLD_METHOD == "binary":
            _, processed = cv2.threshold(gray, BINARY_THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
        elif THRESHOLD_METHOD == "adaptive":
            processed = cv2.adaptiveThreshold(
                gray, 255,
                cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY,
                11,  # Block size (odd number)
                2    # Constant subtracted from mean
            )
        else:
            # Fallback to binary if method is invalid
            _, processed = cv2.threshold(gray, BINARY_THRESHOLD_VALUE, 255, cv2.THRESH_BINARY)
        
        # Step 3: Morphological operations to connect broken text
        kernel = cv2.getStructuringElement(
            cv2.MORPH_RECT, 
            MORPH_KERNEL_SIZE
        )
        
        # Dilate to connect nearby pixels
        processed = cv2.dilate(processed, kernel, iterations=1)
        
        # Erode back to original size
        processed = cv2.erode(processed, kernel, iterations=1)
        
        return processed
    
    def extract_text(self, processed_img: np.ndarray) -> str:
        """
        Extract text from the preprocessed image using Tesseract OCR.
        
        This method uses Tesseract with specific configuration for
        single-line text recognition (WAILA displays one line of text).
        
        Configuration is centralized in config.py.
        
        Args:
            processed_img: Preprocessed image from preprocess_image()
            
        Returns:
            str: Extracted text (uppercase, cleaned), or empty string if
                 no text was recognized.
        """
        try:
            # Use Tesseract to extract text
            # custom_config ensures we only look for the block name line
            text = pytesseract.image_to_string(
                processed_img,
                config=self.tesseract_config
            ).strip()
            
            return text
            
        except Exception as e:
            print(f"[BlockDetector] OCR extraction failed: {str(e)}")
            return ""
    
    def clean_text(self, raw_text: str) -> str:
        """
        Clean and normalize the raw OCR output.
        
        Processing steps:
        1. Convert to uppercase (WAILA displays names in uppercase)
        2. Remove special characters (except spaces and hyphens)
        3. Strip extra whitespace
        4. Remove common WAILA noise (like "@MINECRAFT" footer)
        
        Args:
            raw_text: Raw text output from Tesseract OCR
            
        Returns:
            str: Cleaned and normalized block name
        """
        if not raw_text:
            return ""
        
        # Convert to uppercase (WAILA displays in uppercase)
        cleaned = raw_text.upper()
        
        # Remove the @MINECRAFT footer (common in WAILA)
        if "@MINECRAFT" in cleaned:
            cleaned = cleaned.replace("@MINECRAFT", "").strip()
        if "@waila" in cleaned.lower():
            cleaned = re.sub(r'@\w+', '', cleaned).strip()
        
        # Remove special characters (keep letters, numbers, spaces, hyphens)
        cleaned = re.sub(r'[^A-Z0-9\- ]', '', cleaned)
        
        # Strip extra whitespace
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        
        return cleaned
    
    def map_to_block_id(self, cleaned_name: str) -> Optional[str]:
        """
        Map the cleaned WAILA block name to a Minecraft block ID.
        
        This method uses the WAILA_TO_MINECRAFT_BLOCK_MAPPING dictionary
        (from config.py) to convert human-readable names to game-usable block IDs.
        
        Args:
            cleaned_name: Cleaned block name from clean_text()
            
        Returns:
            str: Minecraft block ID (e.g., "minecraft:stone"), or None if
                 no mapping was found.
        """
        if not cleaned_name:
            return None
        
        # Direct lookup in mapping dictionary
        block_id = self.mapping.get(cleaned_name)
        
        if block_id:
            return block_id
        
        # Try partial matching (for similar names)
        for waila_name, minecraft_id in self.mapping.items():
            if waila_name in cleaned_name or cleaned_name in waila_name:
                return minecraft_id
        
        # Try fuzzy matching: remove spaces and compare
        cleaned_no_spaces = cleaned_name.replace(" ", "").upper()
        for waila_name, minecraft_id in self.mapping.items():
            waila_no_spaces = waila_name.replace(" ", "").upper()
            if waila_no_spaces == cleaned_no_spaces:
                return minecraft_id
        
        return None
    
    def handle_unknown_block(self) -> str:
        """
        Handle the case when a block cannot be detected or mapped.
        
        This is a safety fallback that returns a default Minecraft block ID
        when OCR fails or returns unknown text.
        
        Configuration is centralized in config.py.
        
        Returns:
            str: Default block ID ("minecraft:stone") for safe mining.
        """
        global _consecutive_failures, _last_failure_log_time
        
        _consecutive_failures += 1
        
        # Log failure periodically (throttled to avoid spam)
        current_time = time.time()
        if (current_time - _last_failure_log_time) > OCR_FAILURE_LOG_INTERVAL:
            print(f"[BlockDetector] WARNING: Could not detect block name.")
            print(f"  Consecutive failures: {_consecutive_failures}/{CONSECUTIVE_FAILURE_THRESHOLD}")
            print(f"  Tip: Add the block to WAILA_TO_MINECRAFT_BLOCK_MAPPING in config.py")
            _last_failure_log_time = current_time
        
        # If too many consecutive failures, reset counter
        if _consecutive_failures >= CONSECUTIVE_FAILURE_THRESHOLD:
            print("[BlockDetector] Maximum consecutive failures reached. Resetting counter.")
            _consecutive_failures = 0
        
        # Return default block ID (stone - safe fallback)
        return "minecraft:stone"
    
    def handle_unbreakable_block(self, block_id: str) -> None:
        """
        Handle the case when an unbreakable block is detected.
        
        Actions:
        1. Release the left mouse click immediately
        2. Execute evasion movement (sidestep)
        3. Log the event
        
        Configuration is centralized in config.py.
        
        Args:
            block_id: The detected unbreakable block ID
        """
        import pydirectinput
        import time
        
        print(f"[BlockDetector] UNBREAKABLE BLOCK DETECTED: {block_id}")
        print("[BlockDetector] Releasing mining click...")
        
        # Release the left mouse click
        pydirectinput.mouseUp()
        time.sleep(0.1)
        
        # Execute evasion if enabled
        if ENABLE_EVASION:
            self._execute_evasion(pydirectinput, time)
        
        print("[BlockDetector] Evasion complete. Resuming mining.")
    
    def _execute_evasion(self, pydirectinput, time_module) -> None:
        """
        Execute evasion movement to bypass unbreakable blocks.
        
        Configuration is centralized in config.py (EVASION_KEY, EVASION_DURATION).
        
        Args:
            pydirectinput: The pydirectinput module (passed for compatibility)
            time_module: The time module (passed for compatibility)
        """
        key = EVASION_KEY
        
        if key == "BOTH":
            # Move left then right
            pydirectinput.keyDown('a')
            time_module.sleep(EVASION_DURATION)
            pydirectinput.keyUp('a')
            time_module.sleep(0.1)
            pydirectinput.keyDown('d')
            time_module.sleep(EVASION_DURATION)
            pydirectinput.keyUp('d')
        elif key == "A":
            # Move left
            pydirectinput.keyDown('a')
            time_module.sleep(EVASION_DURATION)
            pydirectinput.keyUp('a')
        elif key == "D":
            # Move right
            pydirectinput.keyDown('d')
            time_module.sleep(EVASION_DURATION)
            pydirectinput.keyUp('d')
        
        print(f"[BlockDetector] Evasion executed: key='{key}', "
              f"duration={EVASION_DURATION}s")
    
    def detect_block(self) -> Optional[str]:
        """
        Main block detection method. Performs the full pipeline:
        capture -> preprocess -> OCR -> clean -> map -> return block ID.
        
        This is the primary method to use for block detection.
        Configuration is centralized in config.py.
        
        Returns:
            str: Minecraft block ID if detected successfully.
                None if detection completely failed (use handle_unknown_block).
                
        Raises:
            No exceptions - all errors are caught and handled internally.
        
        Full Pipeline:
        1. Capture screen ROI (WAILA info box)
        2. Preprocess image (grayscale, threshold, morphological ops)
        3. Extract text via Tesseract OCR
        4. Clean and normalize text
        5. Map WAILA name to Minecraft block ID
        6. Check if block is breakable
        7. Return block ID or handle edge cases
        """
        try:
            # Step 1: Capture screen (ROI - only the WAILA area)
            raw_img = self.capture_screen()
            if raw_img is None:
                return self.handle_unknown_block()
            
            # Step 2: Preprocess image for OCR
            processed_img = self.preprocess_image(raw_img)
            
            # Step 3: Extract text via OCR
            raw_text = self.extract_text(processed_img)
            
            if not raw_text:
                # No text recognized - return unknown block handling
                return self.handle_unknown_block()
            
            # Step 4: Clean and normalize the extracted text
            cleaned_name = self.clean_text(raw_text)
            
            if not cleaned_name:
                # Empty after cleaning - return unknown block handling
                return self.handle_unknown_block()
            
            # Step 5: Map WAILA name to Minecraft block ID
            block_id = self.map_to_block_id(cleaned_name)
            
            if block_id is None:
                # Block not in mapping - handle as unknown
                print(f"[BlockDetector] Unknown block name: '{cleaned_name}'")
                return self.handle_unknown_block()
            
            # Step 6: Check if block is breakable
            if not is_block_breakable(block_id):
                self.handle_unbreakable_block(block_id)
                return None  # Return None to signal unbreakable block
            
            # Reset consecutive failure counter on success
            global _consecutive_failures
            _consecutive_failures = 0
            
            print(f"[BlockDetector] Detected: '{cleaned_name}' -> {block_id}")
            return block_id
            
        except Exception as e:
            print(f"[BlockDetector] Detection pipeline failed: {str(e)}")
            return self.handle_unknown_block()
    
    def detect_and_get_mining_time(
        self,
        tool_id: str,
        efficiency_level: int = 0,
        haste_level: int = 0
    ) -> Optional[float]:
        """
        Convenience method: detect block AND calculate mining time in one call.
        
        This method combines block detection with the mining time calculation
        from mining_algorithm.py, providing a simple interface for the miner.
        Configuration is centralized in config.py.
        
        Args:
            tool_id: The equipped pickaxe's registry name
            efficiency_level: Efficiency enchantment level (0-III)
            haste_level: Haste potion level (0-II)
            
        Returns:
            float: Mining time in seconds, or None if:
                  - Block could not be detected
                  - Block is unbreakable (Bedrock, etc.)
        
        Example:
            detector = BlockDetector()
            mining_time = detector.detect_and_get_mining_time(
                "minecraft:diamond_pickaxe",
                efficiency_level=3,
                haste_level=1
            )
            if mining_time is not None:
                time.sleep(mining_time)
        """
        block_id = self.detect_block()
        
        if block_id is None:
            # Could not detect or unbreakable block
            return None
        
        # Calculate mining time using the algorithm
        mining_time = get_mining_time(
            block_id,
            tool_id,
            efficiency_level,
            haste_level
        )
        
        return mining_time
    
    def add_block_mapping(self, waila_name: str, minecraft_id: str) -> None:
        """
        Dynamically add a new block mapping at runtime.
        
        Useful for adding blocks from your modpack without modifying source code.
        Also updates config.py's WAILA_TO_MINECRAFT_BLOCK_MAPPING.
        
        Args:
            waila_name: The exact name displayed by WAILA (uppercase)
            minecraft_id: The Minecraft block ID (e.g., "minecraft:stone")
        
        Example:
            detector = BlockDetector()
            detector.add_block_mapping("MY_SPECIAL_ORE", "mymod:special_ore")
        """
        self.mapping[waila_name.upper()] = minecraft_id
        print(f"[BlockDetector] Added mapping: '{waila_name}' -> '{minecraft_id}'")
        
        # Also update config for persistence
        import config
        config.add_block_mapping(waila_name, minecraft_id)
    
    def close(self) -> None:
        """
        Clean up resources (close screen capture monitor).
        
        Call this when done with the detector to release resources.
        """
        try:
            if hasattr(self, 'sct_monitor'):
                del self.sct_monitor
            print("[BlockDetector] Resources cleaned up.")
        except Exception as e:
            print(f"[BlockDetector] Cleanup error: {str(e)}")


# =============================================================================
# MODULE-LEVEL CONVENIENCE FUNCTIONS
# =============================================================================

# Global detector instance (lazy initialization)
_detector_instance: Optional[BlockDetector] = None

# Internal state for failure logging (imported from config)
_consecutive_failures: int = 0
_last_failure_log_time: float = 0.0


def get_detector() -> BlockDetector:
    """
    Get (or create) the global BlockDetector instance.
    
    This provides a convenient way to access the detector without
    creating a new instance every time. Configuration is from config.py.
    
    Returns:
        BlockDetector: The global detector instance
    """
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = BlockDetector()
    return _detector_instance


def detect_block() -> Optional[str]:
    """
    Simple function-style block detection.
    
    Convenience function for quick access to block detection.
    Creates a detector instance, detects the block, and returns the result.
    Configuration is centralized in config.py.
    
    Returns:
        str: Minecraft block ID if detected, None if unbreakable or failed.
    
    Example:
        from block_detector import detect_block
        
        block_id = detect_block()
        if block_id:
            print(f"Found: {block_id}")
    """
    detector = get_detector()
    return detector.detect_block()


def detect_and_mine(
    tool_id: str,
    efficiency_level: int = 0,
    haste_level: int = 0
) -> Optional[float]:
    """
    Simple function-style block detection + mining time calculation.
    
    Convenience function that combines detection and mining time calculation.
    Configuration is centralized in config.py.
    
    Args:
        tool_id: The equipped pickaxe's registry name
        efficiency_level: Efficiency enchantment level (0-III)
        haste_level: Haste potion level (0-II)
    
    Returns:
        float: Mining time in seconds, or None if undetectable/unbreakable.
    """
    detector = get_detector()
    return detector.detect_and_get_mining_time(
        tool_id, efficiency_level, haste_level
    )


# =============================================================================
# DEMONSTRATION / TESTING
# =============================================================================

if __name__ == "__main__":
    print("=" * 60)
    print("  MC-Autominer - Block Detector Test Mode")
    print("=" * 60)
    print()
    
    # Create detector instance
    detector = BlockDetector()
    
    try:
        print("Starting block detection (press Ctrl+C to stop)...")
        print()
        
        iteration = 0
        while True:
            iteration += 1
            start_time = time.time()
            
            # Detect block
            block_id = detector.detect_block()
            
            elapsed = time.time() - start_time
            
            print(f"\n--- Detection #{iteration} (took {elapsed*1000:.1f}ms) ---")
            
            if block_id:
                # Calculate mining time for this block
                mining_time = get_mining_time(block_id, "minecraft:diamond_pickaxe", 0, 0)
                
                if mining_time == -1.0:
                    print(f"  Status: UNBREAKABLE - {block_id}")
                else:
                    print(f"  Block ID: {block_id}")
                    print(f"  Mining time: {mining_time*1000:.2f}ms")
            else:
                print("  Status: Could not detect block (using default)")
                print(f"  Default block: minecraft:stone")
                print(f"  Default mining time: {DEFAULT_UNKNOWN_BLOCK_MINING_TIME*1000:.0f}ms")
            
            print()
            time.sleep(0.5)  # Small pause between detections
            
    except KeyboardInterrupt:
        print("\n[BlockDetector] Test mode stopped by user.")
    finally:
        detector.close()
    
    print("\nBlock detection test completed.")