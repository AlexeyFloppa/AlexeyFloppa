import os
import random
from PIL import Image
from datetime import datetime

SOURCE_DIR = "floppas"
OUTPUT_DIR = "generated"

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Filter valid floppa images
all_floppas = [f for f in os.listdir(SOURCE_DIR) if f.endswith(".png") and "pfp" not in f]
selected = random.sample(all_floppas, 6)

# Save daily floppa
Image.open(os.path.join(SOURCE_DIR, selected[0])).save(os.path.join(OUTPUT_DIR, "daily-floppa.png"))

# Save 5 separate random floppa images
for i, fname in enumerate(selected[1:], 1):
    img = Image.open(os.path.join(SOURCE_DIR, fname))
    img.save(os.path.join(OUTPUT_DIR, f"random-{i}.png"))
