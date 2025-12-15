from PIL import Image, ImageDraw, ImageFont
from LCD.FB import FrameBuffer
from datetime import datetime
import jdatetime

fb = FrameBuffer()

img = Image.new("RGB", (fb.width, fb.height), color="white")
draw = ImageDraw.Draw(img)

# ================= CLOCK =================
now = datetime.now()          # local timezone
time_str = now.strftime("%H:%M:%S")

Hour = time_str.split(":")[0]
Min = time_str.split(":")[1]
Sec = time_str.split(":")[2]

# Load font (adjust size if needed)
ttf_path = "fonts/technology/Technology.ttf"
font_size = 40  # small font to fit buttons
font = ImageFont.truetype(ttf_path, font_size)

draw.text((15, 20), Hour, font=font, fill="black", anchor="mm")
draw.text((30, 27), ":", font=font, fill="black", anchor="mm")
draw.text((52, 20), Min, font=font, fill="black", anchor="mm")

# ================= DATE =================
from datetime import datetime
import jdatetime

now = datetime.now()
jnow = jdatetime.datetime.fromgregorian(datetime=now)

date_str = jnow.strftime("%Y/%m/%d")
# Load font (adjust size if needed)
ttf_path = "fonts/MS_Sans_Serif.ttf"
font_size = 10  # small font to fit buttons
font = ImageFont.truetype(ttf_path, font_size)

draw.rectangle([73, 18, 125, 30], fill="black")
draw.text((99, 25), date_str, font=font, fill="white", anchor="mm")

# ================= ID =================
EXAMPLE_ID = "54342113"

# READ ./img/tel.ong resize in 8 * 8 and put in (80, 10) of image
icon = Image.open("./img/tel.png").convert("RGBA")
icon = icon.resize((14, 14), Image.LANCZOS)

img.paste(icon, (72, 3), icon)

# Load font (adjust size if needed)
ttf_path = "fonts/MS_Sans_Serif.ttf"
font_size = 10  # small font to fit buttons
font = ImageFont.truetype(ttf_path, font_size)

draw.text((106, 10), EXAMPLE_ID, font=font, fill="black", anchor="mm")


# ================= BUTTONS =================
margin = 1  # horizontal margin
number_of_btns = 4
height_btns = 13
texts = ["Hist.", "Redial", "DND", "Menu"]

# Load font (adjust size if needed)
ttf_path = "fonts/MS_Sans_Serif.ttf"
font_size = 11  # small font to fit buttons
font = ImageFont.truetype(ttf_path, font_size)

for idx in range(number_of_btns):
    x0 = (fb.width // number_of_btns) * idx + margin
    x1 = (fb.width // number_of_btns) * (idx + 1) - margin
    y0 = fb.height - 1 - height_btns
    y1 = fb.height - 1

    # Draw black button
    draw.rectangle([x0, y0, x1, y1], fill="black")

    # Draw text centered in button
    cx = (x0 + x1) // 2 + 1
    cy = (y0 + y1) // 2 + 2
    draw.text((cx, cy), texts[idx], font=font, fill="white", anchor="mm")

# Write image to framebuffer
fb.write(img)
