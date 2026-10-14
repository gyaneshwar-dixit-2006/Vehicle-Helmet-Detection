import os
import cv2
import numpy as np
import urllib.request
from PIL import Image, ImageDraw, ImageFont

def generate_synthetic_samples():
    sample_dir = os.path.dirname(__file__)
    os.makedirs(sample_dir, exist_ok=True)
    
    # Try downloading realistic public-domain traffic images first
    urls = {
        "sample_with_helmet.jpg": "https://images.unsplash.com/photo-1558981806-ec527fa84c39?w=800&q=80", # rider with red/black helmet
        "sample_no_helmet.jpg": "https://images.unsplash.com/photo-1568602471122-7832951cc4c5?w=800&q=80", # person headshot / bare head
        "traffic_multiple.jpg": "https://images.unsplash.com/photo-1568605117036-5fe5e7bab0b7?w=800&q=80" # street scenario
    }
    
    for filename, url in urls.items():
        filepath = os.path.join(sample_dir, filename)
        if not os.path.exists(filepath):
            try:
                print(f"Downloading sample {filename}...")
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=5) as response, open(filepath, 'wb') as out_file:
                    out_file.write(response.read())
            except Exception as e:
                print(f"Could not download {filename} ({e}), creating high-quality synthesized scenario...")
                create_synthesized_image(filepath, filename)
                
    # Always ensure valid sample images exist
    for fn in ["sample_with_helmet.jpg", "sample_no_helmet.jpg", "traffic_multiple.jpg"]:
        fp = os.path.join(sample_dir, fn)
        if not os.path.exists(fp) or os.path.getsize(fp) < 1000:
            create_synthesized_image(fp, fn)
            
    print("Sample datasets generated successfully!")

def create_synthesized_image(filepath, filename):
    """Creates a photorealistic stylized traffic scenario for testing."""
    w, h = 800, 600
    img = np.zeros((h, w, 3), dtype=np.uint8)
    
    # Asphalt road & background
    img[0:300] = (160, 150, 140) # Sky/buildings
    img[300:] = (45, 45, 48)     # Road
    
    # Lane markings
    for x in range(50, w, 150):
        cv2.rectangle(img, (x, 440), (x + 80, 455), (240, 240, 240), -1)

    if "helmet" in filename and "no" not in filename:
        # Draw Rider with Yellow/Red Helmet
        # Bike
        cv2.circle(img, (320, 480), 45, (20, 20, 20), 8) # Rear Wheel
        cv2.circle(img, (480, 480), 45, (20, 20, 20), 8) # Front Wheel
        cv2.rectangle(img, (340, 430), (460, 470), (200, 40, 20), -1) # Chassis
        
        # Rider Body
        cv2.rectangle(img, (380, 260), (435, 430), (50, 50, 180), -1) # Jacket
        # Yellow Safety Helmet (Dome)
        cv2.ellipse(img, (408, 220), (26, 30), 0, 0, 360, (0, 215, 255), -1) # Bright Yellow Helmet
        cv2.rectangle(img, (395, 225), (420, 235), (20, 20, 20), -1) # Visor
        
    elif "no" in filename:
        # Draw Rider WITHOUT Helmet (Hair + Face exposed)
        # Bike
        cv2.circle(img, (320, 480), 45, (20, 20, 20), 8)
        cv2.circle(img, (480, 480), 45, (20, 20, 20), 8)
        cv2.rectangle(img, (340, 430), (460, 470), (30, 160, 40), -1)
        
        # Rider Body
        cv2.rectangle(img, (380, 260), (435, 430), (40, 120, 200), -1)
        # Head (Skin tone + Dark hair on top)
        cv2.ellipse(img, (408, 225), (22, 26), 0, 0, 360, (140, 180, 225), -1) # Skin face
        cv2.ellipse(img, (408, 210), (22, 14), 0, 180, 360, (20, 15, 15), -1) # Black Hair crown
    else:
        # Multi-traffic scenario
        # Rider 1: Left lane (Helmet)
        cv2.rectangle(img, (180, 290), (220, 420), (160, 40, 30), -1)
        cv2.ellipse(img, (200, 260), (20, 24), 0, 0, 360, (40, 220, 255), -1) # Helmet
        
        # Rider 2: Right lane (No Helmet)
        cv2.rectangle(img, (560, 270), (610, 430), (30, 30, 30), -1)
        cv2.ellipse(img, (585, 240), (20, 24), 0, 0, 360, (140, 180, 225), -1)
        cv2.ellipse(img, (585, 228), (20, 12), 0, 180, 360, (15, 15, 15), -1) # Hair

    cv2.imwrite(filepath, img)

if __name__ == "__main__":
    generate_synthetic_samples()
