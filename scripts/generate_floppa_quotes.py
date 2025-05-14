import json, random, os
from PIL import Image, ImageDraw, ImageFont

# Load quotes
with open("floppa_quotes/quotes.json", "r") as f:
    quotes = json.load(f)

quote = random.choice(quotes)
author = "– AlexeyFloppa"

# --- Load Random Layout Images ---
bg_folder = "floppa_quotes/bg_layouts"
floppa_folder = "floppa_quotes/floppa_layouts"

bg_file = random.choice(os.listdir(bg_folder))
floppa_file = random.choice(os.listdir(floppa_folder))

# Open images
background = Image.open(os.path.join(bg_folder, bg_file)).convert("RGB")
floppa_overlay = Image.open(os.path.join(floppa_folder, floppa_file)).convert("RGBA")

# Composite base + Floppa overlay
background.paste(floppa_overlay, (0, 0), floppa_overlay)

# Prepare drawing
width, height = background.size
draw = ImageDraw.Draw(background)

# Right-side text zone
text_zone_x = 320
text_zone_width = 480

# Colors
text_color = (255, 255, 255)
author_color = (160, 160, 160)

# Load fonts
try:
    font = ImageFont.truetype("arial.ttf", 28)
    author_font = ImageFont.truetype("arial.ttf", 20)
except:
    font = ImageFont.load_default()
    author_font = ImageFont.load_default()

# Wrap text
def wrap_text(text, font, max_width):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        test_line = f"{line} {word}".strip()
        if draw.textlength(test_line, font=font) <= max_width:
            line = test_line
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines

# Light bold
def draw_bold_text(x, y, text, font, color):
    offsets = [(0, 0), (1, 0), (0, 1)]  # subtle fake bold
    for dx, dy in offsets:
        draw.text((x + dx, y + dy), text, font=font, fill=color)

# Calculate wrapped text
wrapped_quote = wrap_text(f"“{quote}”", font, text_zone_width)
line_height = font.getbbox("A")[3] + 8
author_height = author_font.getbbox("A")[3]
total_height = len(wrapped_quote) * line_height + author_height + 10
start_y = (height - total_height) // 2

# Draw quote
for i, line in enumerate(wrapped_quote):
    line_width = draw.textlength(line, font=font)
    x = text_zone_x + (text_zone_width - line_width) / 2
    y = start_y + i * line_height
    draw_bold_text(x, y, line, font, text_color)

# Draw author
author_width = draw.textlength(author, font=author_font)
author_x = text_zone_x + (text_zone_width - author_width) / 2
author_y = start_y + len(wrapped_quote) * line_height + 10
draw.text((author_x, author_y), author, font=author_font, fill=author_color)

# Save output
os.makedirs("generated", exist_ok=True)
background.save("generated/daily-floppa-quote.png")

# background.save("daily_floppa_quote.png")
