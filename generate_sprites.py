#!/usr/bin/env python3
"""
Generate Hermes Girl full-body sprite sheets for the avatar.

Creates pixel art sprites in 64x64 PNG format using only Pillow.
No PyQt6 required - runs standalone.

Features:
- Full body character (not just head)
- 4 animation states: idle, speak, think, alert
- 4-6 frames per state
- Consistent Hermes theme (blue/purple colors)
- 1990s fighting game style
"""

import sys
from pathlib import Path
from PIL import Image, ImageDraw

# Ensure assets directory exists
ASSETS_DIR = Path(__file__).parent.parent / "assets" / "hermes_girl"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)


def create_full_body_avatar(state: str, frame: int, width: int = 64, height: int = 64) -> Image.Image:
    """Create a full-body pixel art Hermes Girl avatar frame using Pillow."""
    # Create transparent image
    image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # Color palette (Hermes theme - blue/purple)
    colors = {
        'skin': (255, 224, 204, 255),
        'skin_shadow': (230, 190, 170, 255),
        'hair': (142, 68, 173, 255),  # Purple
        'hair_highlight': (189, 85, 204, 255),
        'eye_white': (255, 255, 255, 255),
        'eye_pupil': (44, 62, 80, 255),
        'eye_highlight': (135, 206, 250, 255),
        'mouth': (200, 100, 100, 255),
        'outfit_top': (52, 152, 219, 255),  # Blue top
        'outfit_top_highlight': (79, 172, 255, 255),
        'outfit_bottom': (41, 128, 185, 255),  # Blue pants/skirt
        'outfit_accent': (231, 76, 60, 255),  # Red accent (Hermes branding)
        'shoes': (44, 62, 80, 255),
        'outline': (44, 62, 80, 80),
    }
    
    # Adjust colors based on state
    if state == 'alert':
        colors['outfit_top'] = (231, 76, 60, 255)  # Red for alert
        colors['outfit_top_highlight'] = (255, 100, 100, 255)
    elif state == 'think':
        colors['outfit_top'] = (155, 89, 182, 255)  # Purple for think
        colors['outfit_top_highlight'] = (189, 85, 204, 255)
    elif state == 'speak':
        colors['outfit_top'] = (46, 204, 113, 255)  # Green for speak
    
    # === FULL BODY LAYOUT (64x64) ===
    # Head: 20x20 at top (y: 8-28)
    # Torso: 24x20 (y: 24-44)
    # Legs: 16x16 (y: 42-58)
    # Feet: 20x6 (y: 56-62)
    
    # --- HAIR (back layer) ---
    hair_y = 6
    if state == 'think' and frame % 2 == 0:
        hair_y = 4  # Hair floats when thinking
    
    # Main hair shape (ellipse)
    draw.ellipse([18, hair_y, 46, hair_y + 22], fill=colors['hair'])
    # Hair side pieces
    draw.ellipse([10, hair_y + 8, 20, hair_y + 20], fill=colors['hair'])
    draw.ellipse([44, hair_y + 8, 54, hair_y + 20], fill=colors['hair'])
    # Hair highlight
    draw.ellipse([24, hair_y + 4, 32, hair_y + 10], fill=colors['hair_highlight'])
    
    # --- HEAD/FACE ---
    face_y = 12
    draw.ellipse([22, face_y, 42, face_y + 18], fill=colors['skin'])
    
    # Face outline (subtle shadow)
    draw.ellipse([24, face_y + 2, 40, face_y + 16], fill=colors['skin_shadow'])
    
    # --- EYES ---
    eye_y = 18
    if state == 'speak' and frame % 3 == 0:
        eye_y = 19  # Eyes close slightly when speaking
    elif state == 'alert' and frame % 2 == 1:
        eye_y = 17  # Eyes wide when alert
    
    # Left eye
    draw.ellipse([26, eye_y, 32, eye_y + 6], fill=colors['eye_white'])
    draw.ellipse([28, eye_y + 1, 31, eye_y + 4], fill=colors['eye_pupil'])
    draw.ellipse([29, eye_y + 1, 30, eye_y + 2], fill=colors['eye_highlight'])
    
    # Right eye
    draw.ellipse([36, eye_y, 42, eye_y + 6], fill=colors['eye_white'])
    draw.ellipse([38, eye_y + 1, 41, eye_y + 4], fill=colors['eye_pupil'])
    draw.ellipse([39, eye_y + 1, 40, eye_y + 2], fill=colors['eye_highlight'])
    
    # --- MOUTH ---
    mouth_y = 24
    if state == 'speak':
        # Open mouth when speaking
        draw.ellipse([31, mouth_y + 1, 33, mouth_y + 3], fill=colors['mouth'])
    elif state == 'alert':
        # Small O mouth when alert
        draw.ellipse([31, mouth_y, 33, mouth_y + 2], fill=colors['mouth'])
    else:
        # Smile for idle/think (simple arc)
        draw.arc([29, 23, 35, 27], 0, 90, fill=(200, 100, 100, 255), width=1)
    
    # --- TORSO/TOP ---
    torso_y = 28
    if state == 'alert' and frame % 2 == 1:
        torso_y = 26  # Body shakes when alert
    
    # Main torso (rectangle)
    draw.rectangle([20, torso_y, 44, torso_y + 16], fill=colors['outfit_top'])
    
    # Torso highlight
    draw.rectangle([22, torso_y + 2, 30, torso_y + 12], fill=colors['outfit_top_highlight'])
    
    # Hermes accent (red stripe/branding)
    draw.rectangle([20, torso_y + 8, 44, torso_y + 11], fill=colors['outfit_accent'])
    
    # --- LEGS/PANTS ---
    leg_y = 42
    draw.rectangle([22, leg_y, 30, leg_y + 14], fill=colors['outfit_bottom'])  # Left leg
    draw.rectangle([34, leg_y, 42, leg_y + 14], fill=colors['outfit_bottom'])  # Right leg
    
    # --- FEET ---
    foot_y = 54
    draw.rectangle([18, foot_y, 28, foot_y + 5], fill=colors['shoes'])  # Left foot
    draw.rectangle([36, foot_y, 46, foot_y + 5], fill=colors['shoes'])  # Right foot
    
    # --- SPECIAL EFFECTS BY STATE ---
    if state == 'think':
        # Thought bubble indicator
        if frame % 2 == 0:
            draw.ellipse([48, 8, 58, 18], fill=(255, 255, 255, 200))
            draw.ellipse([52, 14, 58, 20], fill=(255, 255, 255, 180))
    elif state == 'alert':
        # Alert indicator (star/spark)
        if frame % 2 == 1:
            draw.ellipse([6, 10, 14, 18], fill=(255, 200, 0, 255))
    elif state == 'speak':
        # Speech bubble indicator
        if frame % 4 == 0:
            draw.ellipse([8, 20, 16, 28], fill=(200, 255, 200, 180))
    
    return image


def generate_sprite_sheet(state: str, num_frames: int):
    """Generate and save sprite sheet for a state."""
    state_dir = ASSETS_DIR / state
    state_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"Generating {state} animation ({num_frames} frames)...")
    
    for frame in range(num_frames):
        image = create_full_body_avatar(state, frame)
        
        # Save as PNG
        output_path = state_dir / f"{frame}.png"
        image.save(str(output_path), 'PNG')
        print(f"  ✓ Frame {frame}: {output_path}")
    
    print(f"✓ {state} animation complete!\n")


def main():
    """Generate all sprite sheets."""
    print("🎨 Generating Hermes Girl Full-Body Sprite Sheets\n")
    print("Style: 1990s fighting game pixel art")
    print("Size: 64x64 pixels per frame (full body)")
    print("Theme: Blue/purple (Hermes colors)\n")
    
    # Generate all states
    generate_sprite_sheet("idle", 4)
    generate_sprite_sheet("speak", 6)
    generate_sprite_sheet("think", 4)
    generate_sprite_sheet("alert", 4)
    
    print("✅ All sprite sheets generated!")
    print(f"\nSprites saved to: {ASSETS_DIR}")
    print("\nNext steps:")
    print("1. Review the sprites in assets/hermes_girl/")
    print("2. Customize colors/design if needed")
    print("3. Run the app: python -m hermes_avatar.main")


if __name__ == "__main__":
    main()
