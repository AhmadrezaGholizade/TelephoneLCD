from PIL import Image, ImageDraw, ImageFont
from LCD.FB import FrameBuffer
from graphic.main_page import MainPage
from datetime import datetime
import time

fb = FrameBuffer()
main = MainPage()

# Initial full render
img = Image.new("RGB", (fb.width, fb.height), color="white")
draw = ImageDraw.Draw(img)
main.render(draw, img, fb.width, fb.height)
fb.write(img)

last_minute = datetime.now().minute

# Define colon region (adjust these values based on your colon position)
COLON_X = 27  # x position
COLON_Y = 14   # y position
COLON_W = 4  # width
COLON_H = 4  # height

COLON2_X = 27  # x position
COLON2_Y = 25   # y position
COLON2_W = 4  # width
COLON2_H = 4  # height

while True:
    time.sleep(1)
    now = datetime.now()
    
    # Full redraw when minute changes
    if now.minute != last_minute:
        img = Image.new("RGB", (fb.width, fb.height), color="white")
        draw = ImageDraw.Draw(img)
        main.render(draw, img, fb.width, fb.height)
        fb.write(img)
        last_minute = now.minute
    else:
        # Just toggle the colon region - super fast!
        fb.toggle_region(COLON_X, COLON_Y, COLON_W, COLON_H)
        fb.toggle_region(COLON2_X, COLON2_Y, COLON2_W, COLON2_H)

