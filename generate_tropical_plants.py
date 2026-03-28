import os
import sys

try:
    from PIL import Image, ImageDraw
except ImportError:
    print("This script uses Pillow to generate the PNG.")
    print("Please run: pip install Pillow")
    sys.exit(1)

def generate_plants():
    # Setup paths
    base_dir = os.path.dirname(os.path.abspath(__file__))
    assets_dir = os.path.join(base_dir, "assets")
    os.makedirs(assets_dir, exist_ok=True)
    
    # Sprite sheet dimensions: 3 frames of 32x32 tiles
    frame_width = 32
    frame_height = 32
    num_frames = 3
    img = Image.new("RGBA", (frame_width * num_frames, frame_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # Palette
    grass = (46, 139, 87, 255)
    dirt = (101, 67, 33, 255)
    wood = (139, 69, 19, 255)
    leaf = (0, 250, 154, 255)
    shadow = (20, 20, 20, 80)

    for i in range(num_frames):
        offset_x = i * frame_width
        
        # 1. Axonometric Base (Isometric diamond, 2:1 ratio)
        # Center of the base is roughly at (16, 22) relative to the frame
        base_poly = [
            (offset_x + 16, 20), # Top
            (offset_x + 28, 26), # Right
            (offset_x + 16, 32), # Bottom
            (offset_x + 4, 26)   # Left
        ]
        draw.polygon(base_poly, fill=grass)
        
        # Tile thickness/depth to give it a 3D isometric block look
        draw.polygon([(offset_x + 4, 26), (offset_x + 16, 32), (offset_x + 16, 36), (offset_x + 4, 30)], fill=dirt)
        draw.polygon([(offset_x + 16, 32), (offset_x + 28, 26), (offset_x + 28, 30), (offset_x + 16, 36)], fill=dirt)

        # 2. Plant Shadow
        draw.ellipse([offset_x + 10, 24, offset_x + 22, 28], fill=shadow)

        # 3. Palm Trunk
        trunk_top = 10
        draw.rectangle([offset_x + 14, trunk_top, offset_x + 16, 24], fill=wood)
        
        # 4. Swaying Leaves (Animation)
        sway = i - 1 # Frames: -1, 0, 1
        cx = offset_x + 15 + sway
        cy = trunk_top

        # Drawing leaves using thick lines for pixel art look
        draw.line([cx, cy, cx - 8, cy - 4], fill=leaf, width=2)   # Top-left
        draw.line([cx, cy, cx + 8, cy - 4], fill=leaf, width=2)   # Top-right
        draw.line([cx, cy, cx - 10, cy + 4], fill=leaf, width=2)  # Bottom-left
        draw.line([cx, cy, cx + 10, cy + 4], fill=leaf, width=2)  # Bottom-right
        draw.line([cx, cy, cx, cy - 8], fill=leaf, width=2)       # Straight up

    # Save to assets folder
    file_path = os.path.join(assets_dir, "tropical_plants.png")
    img.save(file_path, "PNG")
    print(f"Nano banana success! 🍌 Saved sprite sheet to: {file_path}")

if __name__ == "__main__":
    generate_plants()