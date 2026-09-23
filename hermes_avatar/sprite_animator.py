"""
Sprite animator module - handles pixel art animations for Hermes Girl avatar.

Inspired by 1990s fighting games (Metaslug style) with frame-based animations.
"""

from PyQt6.QtWidgets import QLabel, QApplication
from PyQt6.QtGui import QPixmap, QPainter, QPalette, QColor
from PyQt6.QtCore import QTimer, Qt, QRect
from pathlib import Path
import yaml
import os


class SpriteAnimator:
    """Manages pixel art sprite animations for the avatar."""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yaml"
        
        self.config = self._load_config(config_path)
        self.anim_config = self.config.get("animation", {})
        self.current_state = "idle"
        self.current_frame = 0
        self.frame_timer = None
        
        # Sprite sheet paths
        self.assets_dir = Path(__file__).parent.parent / "assets" / "hermes_girl"
        
        # Animation states
        self.states = {
            "idle": {"frames": self.anim_config.get("idle_frames", 4), "fps": self.anim_config.get("fps", 12)},
            "speak": {"frames": self.anim_config.get("speak_frames", 6), "fps": self.anim_config.get("fps", 12)},
            "think": {"frames": self.anim_config.get("think_frames", 3), "fps": self.anim_config.get("fps", 12)},
            "alert": {"frames": self.anim_config.get("alert_frames", 4), "fps": self.anim_config.get("fps", 15)},
        }
        
    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_sprite_path(self, state: str, frame: int) -> Path:
        """Get path to sprite frame image."""
        # Expected structure: assets/hermes_girl/{state}/{frame}.png
        sprite_path = self.assets_dir / state / f"{frame}.png"
        return sprite_path if sprite_path.exists() else None
    
    def load_sprite_sheet(self, state: str) -> list:
        """Load all frames for an animation state."""
        frames = []
        sprite_dir = self.assets_dir / state
        
        if not sprite_dir.exists():
            # Return placeholder if directory doesn't exist
            print(f"Warning: Sprite directory {sprite_dir} not found. Using placeholder.")
            return frames
        
        for i in range(self.states[state]["frames"]):
            frame_path = sprite_dir / f"{i}.png"
            if frame_path.exists():
                frames.append(QPixmap(str(frame_path)))
            else:
                # Create placeholder frame
                frames.append(self._create_placeholder(state, i))
        
        return frames
    
    def _create_placeholder(self, state: str, frame: int) -> QPixmap:
        """Create a placeholder sprite for development."""
        width, height = 64, 64  # Default sprite size
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        
        # Simple pixel art placeholder (will be replaced with real sprites)
        # Color based on state
        colors = {
            "idle": QColor(52, 152, 219),    # Blue
            "speak": QColor(46, 204, 113),   # Green
            "think": QColor(155, 89, 182),   # Purple
            "alert": QColor(231, 76, 60),    # Red
        }
        color = colors.get(state, QColor(127, 140, 141))
        
        # Draw simple pixel art shape (circle-ish)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(color)
        painter.drawEllipse(8, 8, 48, 48)
        
        # Add simple face
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(20, 20, 10, 10)  # Left eye
        painter.drawEllipse(44, 20, 10, 10)  # Right eye
        
        painter.end()
        
        return pixmap
    
    def create_avatar_widget(self, width: int = 200, height: int = 200) -> QLabel:
        """Create a QLabel widget that displays animated avatar."""
        avatar = QLabel()
        avatar.setFixedSize(width, height)
        avatar.setScaledContents(True)
        
        # Load idle animation frames
        self.idle_frames = self.load_sprite_sheet("idle")
        if not self.idle_frames:
            # Create initial placeholder
            self.idle_frames = [self._create_placeholder("idle", 0)]
        
        # Set initial frame
        avatar.setPixmap(self.idle_frames[0])
        
        # Setup animation timer
        fps = self.states["idle"]["fps"]
        interval = 1000 // fps
        
        self.frame_timer = QTimer()
        self.frame_timer.timeout.connect(lambda: self._animate(avatar, self.idle_frames))
        self.frame_timer.start(interval)
        
        return avatar
    
    def _animate(self, widget: QLabel, frames: list):
        """Advance animation frame."""
        if not frames:
            return
        
        self.current_frame = (self.current_frame + 1) % len(frames)
        widget.setPixmap(frames[self.current_frame])
    
    def set_state(self, state: str):
        """Change animation state (idle, speak, think, alert)."""
        if state not in self.states:
            print(f"Unknown state: {state}")
            return
        
        self.current_state = state
        # Will be updated by the main window when state changes
        # This is a placeholder - actual implementation loads new frames
        print(f"Animation state changed to: {state}")
    
    def set_speaking(self, is_speaking: bool = True):
        """Toggle speaking animation."""
        self.set_state("speak" if is_speaking else "idle")
    
    def set_thinking(self, is_thinking: bool = True):
        """Toggle thinking animation."""
        self.set_state("think" if is_thinking else "idle")
    
    def set_alert(self, is_alert: bool = True):
        """Toggle alert animation."""
        self.set_state("alert" if is_alert else "idle")
