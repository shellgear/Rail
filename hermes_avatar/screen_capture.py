"""
Screen capture module - captures screenshots and sends them directly to Hermes via API.

No disk storage - screenshots are captured in memory and transmitted as base64.
"""

import base64
import io
import time
from typing import Optional, Callable
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPixmap
from PIL import Image
import requests
import yaml
import os
from pathlib import Path


class ScreenCapture:
    """Captures screen and sends to Hermes API without saving to disk."""
    
    def __init__(self, config_path: str = None):
        """
        Initialize screen capture with configuration.
        
        Args:
            config_path: Path to config.yaml (default: same dir as this file)
        """
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yaml"
        
        self.config = self._load_config(config_path)
        self.interval = self.config.get("screen_capture", {}).get("interval_seconds", 30)
        self.api_config = self.config.get("api", {})
        self.is_running = False
        self.capture_callback: Optional[Callable] = None
        
    def _load_config(self, config_path: str) -> dict:
        """Load configuration from YAML file."""
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def capture_screenshot(self) -> bytes:
        """
        Capture current screen and return as JPEG bytes.
        
        Returns:
            JPEG-encoded screenshot bytes (no file saved)
        """
        # Use PIL to capture screen via X11 (Linux)
        # Alternative: use PyQt6's QScreen.grabWindow()
        try:
            from PyQt6.QtWidgets import QApplication
            from PyQt6.QtGui import QGuiApplication
            
            app = QApplication.instance()
            if app is None:
                app = QApplication([])
            
            screen = QGuiApplication.primaryScreen()
            pixmap = screen.grabWindow(0)  # Grab entire screen
            
            # Convert to PIL Image
            image = QPixmap.toImage(pixmap)
            buffer = io.BytesIO()
            
            # Save as JPEG in memory
            # Note: PyQt6 doesn't directly export to PIL, so we use a workaround
            # For production, consider using mss or pyscreenshot
            pixmap.save(buffer, "JPEG")
            buffer.seek(0)
            
            return buffer.getvalue()
            
        except Exception as e:
            print(f"Screen capture error: {e}")
            # Fallback: try PIL's ImageGrab if available
            try:
                from PIL import ImageGrab
                img = ImageGrab.grab()
                buffer = io.BytesIO()
                img.save(buffer, format="JPEG")
                buffer.seek(0)
                return buffer.getvalue()
            except ImportError:
                raise ImportError("PIL ImageGrab not available. Install: pip install pillow")
    
    def send_to_hermes(self, screenshot_bytes: bytes) -> dict:
        """
        Send screenshot to Hermes API for analysis.
        
        Args:
            screenshot_bytes: JPEG image bytes
            
        Returns:
            API response dict with Hermes' analysis
        """
        api_endpoint = self.api_config.get("endpoint", "http://localhost:8000/v1/chat/completions")
        model = self.api_config.get("model", "qwen3.5-122b")
        timeout = self.api_config.get("timeout", 10)
        
        # Convert to base64
        base64_image = base64.b64encode(screenshot_bytes).decode('utf-8')
        
        # Prepare payload for vision analysis
        payload = {
            "model": model,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": "Analizza questo screenshot e fornisci suggerimenti utili per l'utente su ciò che sta facendo a schermo. Sii conciso e pratico."
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            "max_tokens": 500
        }
        
        try:
            response = requests.post(
                api_endpoint,
                json=payload,
                timeout=timeout,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            
            result = response.json()
            return {
                "success": True,
                "analysis": result.get("choices", [{}])[0].get("message", {}).get("content", "Nessuna analisi disponibile"),
                "timestamp": time.time()
            }
            
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"API request failed: {str(e)}",
                "analysis": None
            }
    
    def capture_and_send(self) -> dict:
        """
        Full workflow: capture screenshot and send to Hermes.
        
        Returns:
            Dict with success status and analysis/result
        """
        if not self.config.get("screen_capture", {}).get("enabled", True):
            return {"success": False, "error": "Screen capture disabled in config"}
        
        try:
            # Capture screenshot in memory
            screenshot_bytes = self.capture_screenshot()
            
            # Send to Hermes
            result = self.send_to_hermes(screenshot_bytes)
            
            # Trigger callback if registered
            if self.capture_callback and result.get("success"):
                self.capture_callback(result.get("analysis"))
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Capture failed: {str(e)}",
                "analysis": None
            }
    
    def start_periodic_capture(self, callback: Callable = None):
        """
        Start periodic screen capture in background.
        
        Args:
            callback: Function to call with Hermes' analysis after each capture
        """
        import threading
        
        self.capture_callback = callback
        self.is_running = True
        
        def capture_loop():
            while self.is_running:
                time.sleep(self.interval)
                if self.is_running:
                    result = self.capture_and_send()
                    if result.get("success") and callback:
                        callback(result.get("analysis"))
        
        thread = threading.Thread(target=capture_loop, daemon=True)
        thread.start()
        return thread
    
    def stop_periodic_capture(self):
        """Stop periodic capture."""
        self.is_running = False
