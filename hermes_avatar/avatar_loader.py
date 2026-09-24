"""
Avatar loader module - loads Hermes Girl avatar images with fallback support.

Supports:
- Real sprite sheets (when available)
- Single PNG fallback image
- Procedural placeholder (last resort)
"""

from PyQt6.QtGui import QPixmap, QPainter, QPalette, QColor
from PyQt6.QtCore import Qt
from pathlib import Path
import yaml


class AvatarLoader:
    """Loads avatar images with intelligent fallback."""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            config_path = Path(__file__).parent.parent / "config.yaml"
        
        self.config = self._load_config(config_path)
        self.assets_dir = Path(__file__).parent.parent / "assets" / "hermes_girl"
        
    def _load_config(self, config_path: str) -> dict:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    
    def get_avatar_image(self, size: tuple = (200, 200)) -> QPixmap:
        """
        Load avatar image with fallback chain:
        1. Real sprite sheet (idle/0.png)
        2. Single fallback PNG (fallback.png)
        3. Procedural placeholder
        
        Args:
            size: (width, height) for the avatar
            
        Returns:
            QPixmap ready to display
        """
        width, height = size
        
        # Try 1: Real sprite sheet
        idle_frame = self.assets_dir / "idle" / "0.png"
        if idle_frame.exists():
            pixmap = QPixmap(str(idle_frame))
            if not pixmap.isNull():
                return pixmap.scaled(width, height, Qt.AspectMode.KeepAspectRatio, Qt.Transformation.SmoothTransformation)
        
        # Try 2: Single fallback PNG
        fallback_img = self.assets_dir / "fallback.png"
        if fallback_img.exists():
            pixmap = QPixmap(str(fallback_img))
            if not pixmap.isNull():
                return pixmap.scaled(width, height, Qt.AspectMode.KeepAspectRatio, Qt.Transformation.SmoothTransformation)
        
        # Try 3: Procedural placeholder (last resort)
        return self._create_placeholder(width, height)
    
    def _create_placeholder(self, width: int, height: int) -> QPixmap:
        """Create a better-looking procedural placeholder."""
        pixmap = QPixmap(width, height)
        pixmap.fill(Qt.GlobalColor.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Background gradient (subtle)
        from PyQt6.QtGui import QLinearGradient
        gradient = QLinearGradient(0, 0, 0, height)
        gradient.setColorAt(0, QColor(52, 152, 219))    # Light blue
        gradient.setColorAt(1, QColor(41, 128, 185))    # Dark blue
        painter.setBrush(gradient)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(10, 10, width - 20, height - 20)
        
        # Face (white)
        painter.setBrush(QColor(255, 255, 255))
        painter.drawEllipse(width // 2 - 25, height // 2 - 20, 50, 40)
        
        # Eyes (black pupils)
        painter.setBrush(QColor(44, 62, 80))  # Dark blue-gray
        painter.drawEllipse(width // 2 - 35, height // 2 - 15, 12, 12)  # Left eye
        painter.drawEllipse(width // 2 + 23, height // 2 - 15, 12, 12)  # Right eye
        
        # Smile (simple curve)
        painter.setPen(QColor(44, 62, 80).lighter(120))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawArc(width // 2 - 20, height // 2 + 5, 40, 20, 0, 90 * 16)
        
        # Hair hint (purple accent - Hermes theme)
        painter.setBrush(QColor(142, 68, 173))  # Purple
        painter.drawEllipse(width // 2 - 8, height // 2 - 25, 16, 16)  # Hair accent
        
        painter.end()
        
        return pixmap
    
    def get_animation_frames(self, state: str = "idle") -> list:
        """
        Load animation frames for a state.
        
        Returns list of QPixmaps, or single placeholder if no frames found.
        """
        frames = []
        state_dir = self.assets_dir / state
        
        if state_dir.exists():
            # Try to load frames
            for i in range(20):  # Try up to 20 frames
                frame_path = state_dir / f"{i}.png"
                if frame_path.exists():
                    pixmap = QPixmap(str(frame_path))
                    if not pixmap.isNull():
                        frames.append(pixmap)
                    else:
                        break  # Stop if we hit a null image
                else:
                    break  # Stop if file doesn't exist
        
        if not frames:
            # Return single placeholder
            frames = [self._create_placeholder(64, 64)]
        
        return frames
