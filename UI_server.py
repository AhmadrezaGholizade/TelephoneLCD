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

            tools.draw_border(draw)
            tools.draw_contact_rows(draw, contacts, CONTACT_INDEX, CONTACT_PAGE_NUMBER)
            tools.draw_scrollbar(draw, CONTACT_PAGE_NUMBER, len(contacts))
            tools.draw_header(draw)

            fb.write(img)

    if STATUS == "contact_info":
        if STATUS_CHANGED:
            if STATUS_CHANGED:
                STATUS_CHANGED = False

            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)
            tools.draw_border(draw)

            tools.draw_contact_info(draw, img, contacts[CONTACT_INDEX], fb.width, fb.height)

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




            
    

