from PIL import Image, ImageDraw, ImageFont
from LCD.FB import FrameBuffer
from graphic.tools import Tools
from datetime import datetime
from events.EventHandler import EventHandler
import time
from colon_pos import *

ITEM_INDEX = 0
PAGE_NUMBER = 0

menu_items = [
    ("contacts", {"text": "Contacts", "icon_path": "img/person.png"}),
    ("history", {"text": "History", "icon_path": "img/hist.png"}),
    ("setting", {"text": "Setting", "icon_path": "img/setting.png"}),
    ("messeges", {"text": "Messege", "icon_path": "img/messege.png"}),
    ("DND", {"text": "DND", "icon_path": "img/DND.png"}),
]

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

STATUS = "main_page"
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
        if changes.get("INDEX_RESET", False):
            PAGE_NUMBER = 0
            ITEM_INDEX = 0

    if STATUS=="menu":
        if changes and changes.get("MENU_ITEM_INDEX", 0) != 0:
            ITEM_INDEX += changes.get("MENU_ITEM_INDEX", 0)
            if ITEM_INDEX < 0:
                ITEM_INDEX = 0
            elif ITEM_INDEX >= len(menu_items):
                ITEM_INDEX = len(menu_items) - 1

        if changes and changes.get("OK", False):
            STATUS = menu_items[ITEM_INDEX][0]
            STATUS_CHANGED = True
            continue

            

        if STATUS_CHANGED:
            STATUS_CHANGED = False
        
            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)


            name_font = ImageFont.truetype("fonts/MS_Sans_Serif.ttf", 10)
            for i in range(len(menu_items)):
                x_pos = 87 if (i > 2) else 24
                n = i % 3

                print_name = menu_items[i][1]["text"].strip()
                color = "black"
                if i == ITEM_INDEX:
                    color = "white"
                    draw.rectangle([x_pos-16 , 12 * n, x_pos+38, 12 * (n+1)], fill="black")
                                       
                tools.draw_icon(draw, img, menu_items[i][1]["icon_path"], (13, 13), (x_pos-15,n*12), color=color)
                
                draw.text((x_pos, 12 * n), print_name, font=name_font, fill=color)

            tools.draw_buttons(draw, 124, fb.height, height=11,font_size=10,texts=("Back", "", "", ""))

            draw.rectangle([1, 1, 7, 35], fill="black")
            draw.rectangle([63, 1, 70, 35], fill="black")
            for i in range(len(menu_items)):
                x_pos = 64 if (i > 2) else 1
                n = i % 3
                draw.text((x_pos, 12 * n), f"{i+1}", font=name_font, fill="white")

            tools.draw_border(draw)
            fb.write(img)

    if STATUS == "contacts":
        if changes and changes.get("CONTACT_INDEX", 0) != 0:
            ITEM_INDEX += changes.get("CONTACT_INDEX", 0)
            if ITEM_INDEX < 0:
                ITEM_INDEX = 0
            elif ITEM_INDEX >= len(contacts):
                ITEM_INDEX = len(contacts) - 1
            
            PAGE_NUMBER = ITEM_INDEX // 3

        if STATUS_CHANGED:
            STATUS_CHANGED = False
        
            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)

            tools.draw_border(draw)
            tools.draw_contact_rows(draw, contacts, ITEM_INDEX, PAGE_NUMBER)
            tools.draw_scrollbar(draw, PAGE_NUMBER, len(contacts))
            # tools.draw_header(draw)
            tools.draw_buttons(draw, 124, fb.height, height=9, font_size=10,texts=("Back", "", "", ""))

            fb.write(img)

    if STATUS == "contact_info":
        if STATUS_CHANGED:
            if STATUS_CHANGED:
                STATUS_CHANGED = False

            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)
            tools.draw_border(draw)

            tools.draw_contact_info(draw, img, contacts[ITEM_INDEX], fb.width, fb.height)

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




            
    

