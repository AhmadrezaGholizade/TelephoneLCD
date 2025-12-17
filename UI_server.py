from PIL import Image, ImageDraw, ImageFont
from LCD.FB import FrameBuffer
from graphic.tools import Tools
from datetime import datetime
from events.EventHandler import EventHandler
import time
from colon_pos import *



CONTACT_INDEX = 0
CONTACT_PAGE_NUMBER = 0

contacts = [
    {"nick_name": "Ali Rahmatlahi",        "phone_number": "09123456789"},
    {"nick_name": "حسین هزار دستان کلکچالی",        "phone_number": "09123456789"},
    {"nick_name": "احمدرضا قلی زاده تلیکانی اصل",        "phone_number": "09123456789"},
    {"nick_name": "Reza",       "phone_number": "02144556677"},
    {"nick_name": "سارا کریمی",       "phone_number": "989121234567"},
    {"nick_name": "NimaNimaNimaNimaNimaNimaNimaNima",       "phone_number": "447911123456"},
    {"nick_name": "Maryam",     "phone_number": "0913555777"},
    {"nick_name": "حسین",    "phone_number": "120"},
    {"nick_name": "هوتن",    "phone_number": "004917612345678"},
    {"nick_name": "آرمان",      "phone_number": "+5551234"},
    {"nick_name": "Zahra",      "phone_number": "0012025550198"},
    {"nick_name": "شکیبا",      "phone_number": "888777666555"},
    {"nick_name": "مهدی",      "phone_number": "09011223344"},
    {"nick_name": "Navid",      "phone_number": "987654321012345"},
    {"nick_name": "Atena",      "phone_number": "98765"}
]

fb = FrameBuffer()
tools = Tools()
event_handler = EventHandler()

STATUS = "contacts"
STATUS_CHANGED = True

last_minute = datetime.now().minute
last_second = datetime.now().second


while True:
    time.sleep(0.13)
    now = datetime.now()
    changes = event_handler.handle_key(STATUS)
    if changes:
        STATUS_CHANGED = True
        STATUS = changes['STATUS']

    if STATUS == "contacts":
        if changes and changes.get("CONTACT_INDEX", 0) != 0:
            CONTACT_INDEX += changes.get("CONTACT_INDEX", 0)
            if CONTACT_INDEX < 0:
                CONTACT_INDEX = 0
            elif CONTACT_INDEX >= len(contacts):
                CONTACT_INDEX = len(contacts) - 1
            
            CONTACT_PAGE_NUMBER = CONTACT_INDEX // 3

        if STATUS_CHANGED:
            STATUS_CHANGED = False
        
            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, 127, 47], outline="black")

            # ====== CONTACTS =======
            name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 10)
            number_font = ImageFont.truetype("fonts/MS_Sans_Serif.ttf", 10)

            for n, i in enumerate(range(CONTACT_PAGE_NUMBER * 3, min(CONTACT_PAGE_NUMBER * 3 + 3, len(contacts)))):
                name = contacts[i]["nick_name"].strip()
                print_name = name[:22] + "..." if len(name) > 22 else name

                # Black Theme for Selected Contact
                color = "black"
                if i == CONTACT_INDEX:
                    color = "white"
                    draw.rectangle([1, 11 + 13 * n, 122, 9 + 13 * (n+1)], fill="black")
                    
                # Name    
                draw.text((3, 10 + 12 * n), print_name, font=name_font, fill=color)

            # ====== Draw Scroll Bar, TOP, Bott ======
            draw.rectangle([124, 0, 124, 48], fill="black") # seperator line
            page_ratio = 3 / len(contacts) * 48
            draw.rectangle([125, CONTACT_PAGE_NUMBER * page_ratio, 127, (CONTACT_PAGE_NUMBER + 1) * page_ratio], fill="black")

            # if CONTACT_PAGE_NUMBER == 0:
            draw.rectangle([1, 0, 122, 9], fill="black")
            draw.text((37, -2), "Contacts", font=name_font, fill="white")
            # if CONTACT_INDEX // 3 == (len(contacts)-1) // 3:
            #     draw.rectangle([1, 41, 123, 46], fill="black")
            fb.write(img)

    if STATUS == "contact_info":
        if STATUS_CHANGED:
            if STATUS_CHANGED:
                STATUS_CHANGED = False

            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)
            draw.rectangle([0, 0, 127, 47], outline="black")

            icon = Image.open("./img/person.png").convert("RGBA")
            icon = icon.resize((14, 14), Image.LANCZOS)
            img.paste(icon, (3,3), icon)

            icon = Image.open("./img/tel.png").convert("RGBA")
            icon = icon.resize((14, 14), Image.LANCZOS)
            img.paste(icon, (3,17), icon)

            name = contacts[CONTACT_INDEX]["nick_name"].strip()
            print_name = name[:18] + "..." if len(name) > 18 else name

            number = contacts[CONTACT_INDEX]["phone_number"].strip()
            print_number = number[:20] + "..." if len(number) > 20 else number

            name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 12)
            draw.text((18, 1), print_name, font=name_font, fill="black")

            number_font = ImageFont.truetype("fonts/MS_Sans_Serif.ttf", 11)
            draw.text((18, 19), print_number, font=number_font, fill="black")

            tools.draw_buttons(draw, fb.width, fb.height, texts=("Back", "Call", "", ""))

            fb.write(img)
    
    if STATUS == "main_page":
        # Full redraw when minute changes
        if (now.minute != last_minute) or STATUS_CHANGED:
            if STATUS_CHANGED:
                STATUS_CHANGED = False
            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)
            tools.render_main_page(draw, img, fb.width, fb.height)
            fb.write(img)
            last_minute = now.minute
        else:
            if now.second != last_second:
                # Just toggle the colon region - super fast!
                fb.toggle_region(COLON_X, COLON_Y, COLON_W, COLON_H)
                fb.toggle_region(COLON2_X, COLON2_Y, COLON2_W, COLON2_H)
                last_second = now.second




            
    

