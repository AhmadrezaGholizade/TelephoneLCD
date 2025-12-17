from PIL import Image, ImageDraw, ImageFont
from LCD.FB import FrameBuffer
from datetime import datetime
import jdatetime

class Tools:
    def render_main_page(self, draw, img, width, height):
        self.draw_clock(draw)
        self.draw_date(draw)
        self.draw_id(draw, img)
        self.draw_buttons(draw, width, height)

    # ================= CLOCK =================
    def draw_clock(self, draw,
               pos_hour=(15, 20),
               pos_colon=(30, 27),
               pos_min=(52, 20),
               font_path="fonts/technology/Technology.ttf",
               font_size=40,
               color="black",
               bg="white"):

        now = datetime.now()
        h, m, s = now.strftime("%H:%M:%S").split(":")
        sec = int(s)

        font = ImageFont.truetype(font_path, font_size)

        # Draw hour & minute (always visible)
        draw.text(pos_hour, h, font=font, fill=color, anchor="mm")
        draw.text(pos_min, m, font=font, fill=color, anchor="mm")

        # # Blink colon
        # colon_color = color if (sec % 2 == 0) else bg
        # draw.text(pos_colon, ":", font=font, fill=colon_color, anchor="mm")


    # ================= DATE =================
    def draw_date(self,draw,
                rect=(73, 18, 125, 30),
                text_pos=(99, 25),
                font_path="fonts/MS_Sans_Serif.ttf",
                font_size=10,
                bg="black",
                fg="white"):

        now = datetime.now()
        jnow = jdatetime.datetime.fromgregorian(datetime=now)
        date_str = jnow.strftime("%Y/%m/%d")

        font = ImageFont.truetype(font_path, font_size)

        draw.rectangle(rect, fill=bg)
        draw.text(text_pos, date_str, font=font, fill=fg, anchor="mm")


    # ================= ID =================
    def draw_id(self,draw,
                img,
                example_id="54342113",
                icon_path="./img/tel.png",
                icon_pos=(72, 3),
                icon_size=(14, 14),
                text_pos=(106, 10),
                font_path="fonts/MS_Sans_Serif.ttf",
                font_size=10,
                color="black"):

        icon = Image.open(icon_path).convert("RGBA")
        icon = icon.resize(icon_size, Image.LANCZOS)
        img.paste(icon, icon_pos, icon)

        font = ImageFont.truetype(font_path, font_size)
        draw.text(text_pos, example_id, font=font, fill=color, anchor="mm")


    # ================= BUTTONS =================
    def draw_buttons(self,draw,
                    fb_width,
                    fb_height,
                    texts=("Hist.", "Redial", "DND", "Menu"),
                    margin=1,
                    height=13,
                    font_path="fonts/MS_Sans_Serif.ttf",
                    font_size=11,
                    bg="black",
                    fg="white"):

        font = ImageFont.truetype(font_path, font_size)
        n = len(texts)

        for i, txt in enumerate(texts):
            x0 = (fb_width // n) * i + margin
            x1 = (fb_width // n) * (i + 1) - margin
            y0 = fb_height - 1 - height
            y1 = fb_height - 1

            draw.rectangle([x0, y0, x1, y1], fill=bg)

            cx = (x0 + x1) // 2 + 1
            cy = (y0 + y1) // 2 + 2
            draw.text((cx, cy), txt, font=font, fill=fg, anchor="mm")
            