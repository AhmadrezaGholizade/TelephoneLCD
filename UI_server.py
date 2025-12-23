from PIL import Image, ImageDraw, ImageFont
from LCD.FB import LCDFrameBuffer
from graphic.tools import Tools
from datetime import datetime
from events.EventHandler import EventHandler
import time
from colon_pos import *
import jdatetime
from server_sock.CallEngineClient import CallEngineClient
import json


STATUS = "main_page"
STATUS_CHANGED = True

ITEM_INDEX = 0
PAGE_NUMBER = 0

last_state = None

def handle_event(event):
    if event.get("action") != "ping" and event.get("event") != "pong":
        print("EVENT RECEIVED:", event)

    if isinstance(event, dict):

        if event.get("event") == "state":
            last_state = event
            print(f"Last state Updated: {last_state}")

            global STATUS_CHANGED, STATUS
            if event["value"] == "IDLE":
                STATUS_CHANGED = True
                STATUS = 'main_page'
                print("IDLE: Return to main page")
            
            if event["value"] == "RINGING":
                STATUS_CHANGED = True
                STATUS = 'ringing'
                print("RINGING:  go to RINGING page")

        if event.get("action") == "ping":
            # print("PING RECIEVED")
            ts = int(time.time() * 1000)
            msg = {
                "event": "pong",
                "ts": ts
            }
            callEngineClient.send(json.dumps(msg))


hist_type_text = {
    "missed": "Missed Call",
    "incoming": "Incoming Call",
    "outgoing": "Outgoing Call"
}

hist_type_png = {
    "missed": "./img/miss.png",
    "incoming": "./img/in.png",
    "outgoing": "./img/out.png"
}

menu_items = [
    ("contacts", {"text": "Contacts", "icon_path": "img/person.png"}),
    ("history", {"text": "History", "icon_path": "img/hist.png"}),
    ("setting", {"text": "Setting", "icon_path": "img/setting.png"}),
    ("messeges", {"text": "Messege", "icon_path": "img/messege.png"}),
    ("DND", {"text": "DND", "icon_path": "img/DND.png"}),
]

contacts = [
    {"nick_name": "Ali Rahmatlahi", "phone_number": "09123456789", "user_type": "SIP"},
    {"nick_name": "حسین هزار دستان کلکچالی", "phone_number": "09123456789", "user_type": "SIP"},
    {"nick_name": "احمدرضا قلی زاده تلیکانی اصل", "phone_number": "09123456789", "user_type": "SIP"},
    {"nick_name": "Reza", "phone_number": "02144556677", "user_type": "SIP"},
    {"nick_name": "سارا کریمی", "phone_number": "989121234567", "user_type": "WRTC"},
    {"nick_name": "NimaNimaNimaNimaNimaNimaNimaNima", "phone_number": "447911123456", "user_type": "WRTC"},
    {"nick_name": "Maryam", "phone_number": "0913555777", "user_type": "SIP"},
    {"nick_name": "حسین", "phone_number": "120", "user_type": "SIP"},
    {"nick_name": "هوتن", "phone_number": "004917612345678", "user_type": "WRTC"},
    {"nick_name": "آرمان", "phone_number": "+5551234", "user_type": "WRTC"},
    {"nick_name": "Zahra", "phone_number": "0012025550198", "user_type": "SIP"},
    {"nick_name": "شکیبا", "phone_number": "888777666555", "user_type": "WRTC"},
    {"nick_name": "مهدی", "phone_number": "09011223344", "user_type": "SIP"},
    {"nick_name": "Navid", "phone_number": "987654321045", "user_type": "WRTC"},
    {"nick_name": "Atena", "phone_number": "98765", "user_type": "WRTC"}
]


history_calls = [
    {
        "phone_number": "09123456789",
        "type": "incoming",
        "timestamp": 1734598200  # 2024-12-19 09:50:00
    },
    {
        "phone_number": "4432",
        "type": "incoming",
        "timestamp": 1734598200  # 2024-12-19 09:50:00
    },
    {
        "phone_number": "09123456789",
        "type": "missed",
        "timestamp": 1734594300  # 2024-12-19 08:45:00
    },
    {
        "phone_number": "021556677",
        "type": "outgoing",
        "timestamp": 1734589800  # 2024-12-19 07:30:00
    },
    {
        "phone_number": "989121234567",
        "type": "incoming",
        "timestamp": 1734546000  # 2024-12-18 19:20:00
    },
    {
        "phone_number": "447911123456",
        "type": "missed",
        "timestamp": 1734517200  # 2024-12-18 11:00:00
    },
    {
        "phone_number": "0901223344",
        "type": "outgoing",
        "timestamp": 1734474000  # 2024-12-17 23:00:00
    },
    {
        "phone_number": "0012025550198",
        "type": "incoming",
        "timestamp": 1734438000  # 2024-12-17 13:00:00
    },
    {
        "phone_number": "004917612345678",
        "type": "missed",
        "timestamp": 1734393000  # 2024-12-16 23:30:00
    },
    {
        "phone_number": "004917612345678",
        "type": "missed",
        "timestamp": 1734393000  # 2024-12-16 23:30:00
    }
]

fb = LCDFrameBuffer()
tools = Tools()
event_handler = EventHandler()
callEngineClient = CallEngineClient()




last_minute = datetime.now().minute
last_second = datetime.now().second

number_typing = ""

callEngineClient.connect()
callEngineClient.start(handle_event)

last_ping = time.monotonic()

while True:
    time.sleep(0.05)
    now = datetime.now()

    if (time.monotonic() - last_ping) > 5:
        last_ping = time.monotonic()
        ts = int(time.time() * 1000)  # milliseconds
        msg = {
            "action": "ping",
            "ts": ts
        }

        callEngineClient.send(json.dumps(msg))

    changes = event_handler.handle_key(STATUS)

    event_handler.check_light_timeout(fb)

    if changes:
        STATUS_CHANGED = True
        STATUS = changes['STATUS']
        if changes.get("INDEX_RESET", False):
            PAGE_NUMBER = 0
            ITEM_INDEX = 0
        if changes.get("INDEX_SET", False):
            ITEM_INDEX = changes.get("INDEX_SET", False)

    # print(STATUS, STATUS_CHANGED)

    if STATUS=="ringing":
        if changes and changes.get("REJECT", False):
            msg = {
                "action": "reject"
            }
            callEngineClient.send(json.dumps(msg))


        if STATUS_CHANGED:
            STATUS_CHANGED = False
            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)
            name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 14)
            draw.text((18, 1), "RINGING...", font=name_font, fill="black")
            fb.write(img)


    if STATUS=="calling":
        if number_typing and changes and changes.get("CALL", False):
            msg = {
                "action": "call",
                "number": number_typing
            }
            callEngineClient.send(json.dumps(msg))
        
        if STATUS_CHANGED:
            STATUS_CHANGED = False
            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)
            name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 14)
            draw.text((18, 1), "CALLING...", font=name_font, fill="black")
            fb.write(img)
    
    if STATUS=="incall":
        if changes and changes.get("ANSWER", False):
            msg = {
                "action": "answer"
            }
            callEngineClient.send(json.dumps(msg))
        if changes and changes.get("HANGUP", False):
            msg = {
                "action": "hangup"
            }
            callEngineClient.send(json.dumps(msg))
        
        if STATUS_CHANGED:
            STATUS_CHANGED = False
            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)
            name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 14)
            draw.text((18, 1), "INCALL...", font=name_font, fill="black")
            fb.write(img)


    if STATUS=="type_number":
        if changes:
            if changes.get("FIRST_CHAR", False) != False:
                number_typing = changes.get("FIRST_CHAR", False)
            if changes.get("ADD_CHAR", False):
                number_typing += changes.get("ADD_CHAR", False)
            


        if STATUS_CHANGED:
            STATUS_CHANGED = False
            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)

            if not number_typing:
                number_font = ImageFont.truetype("fonts/MS_Sans_Serif.ttf", 18)
                draw.text((4, 8), "Type Number...", font=number_font, fill="black")

            else:
                number_font = ImageFont.truetype("fonts/MS_Sans_Serif.ttf", 18)
                draw.text((4, 8), number_typing, font=number_font, fill="black")

            tools.draw_buttons(draw, fb.width, fb.height, height=9,font_size=10,texts=("Back", "Call", "Add", ""))
            fb.write(img)


    if STATUS=="history":
        if changes and changes.get("HISTORY_INDEX", 0) != 0:
            ITEM_INDEX += changes.get("HISTORY_INDEX", 0)
            if ITEM_INDEX < 0:
                ITEM_INDEX = 0
                continue
            elif ITEM_INDEX >= len(history_calls):
                ITEM_INDEX = len(history_calls) - 1
                continue
            
            PAGE_NUMBER = ITEM_INDEX // 3

        if STATUS_CHANGED:
            STATUS_CHANGED = False

            for h in history_calls:
                for contact in contacts:
                    if contact["phone_number"] == h["phone_number"]:
                        h["phone_number"] = contact["nick_name"]
        
            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)

            tools.draw_history_items(draw, img, history_calls, ITEM_INDEX, PAGE_NUMBER)

            tools.draw_scrollbar(draw, PAGE_NUMBER, len(history_calls))
            tools.draw_buttons(draw, 124, fb.height, height=9,font_size=10,texts=("Back", "Detail", "", ""))

            fb.write(img)

    elif STATUS=="menu":
        if changes and changes.get("MENU_ITEM_INDEX", 0) != 0:
            ITEM_INDEX += changes.get("MENU_ITEM_INDEX", 0)
            if ITEM_INDEX < 0:
                ITEM_INDEX = 0
                continue
            elif ITEM_INDEX >= len(menu_items):
                ITEM_INDEX = len(menu_items) - 1
                continue

        if changes and changes.get("key", False):
            if changes.get("key", False) == 'Ok':
                STATUS = menu_items[ITEM_INDEX][0]
            else:
                STATUS = menu_items[int(changes.get("key", False))-1][0]
            ITEM_INDEX = 0
            PAGE_NUMBER = 0
            STATUS_CHANGED = True
            continue

        if STATUS_CHANGED:
            STATUS_CHANGED = False
        
            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)

            tools.draw_manu_items(draw, img, menu_items, ITEM_INDEX)

            tools.draw_buttons(draw, 124, fb.height, height=11,font_size=10,texts=("Back", "", "", ""))

            tools.one_to_six_culs(draw, len(menu_items))

            tools.draw_border(draw)
            fb.write(img)

    elif STATUS == "contacts":
        if changes and changes.get("CONTACT_INDEX", 0) != 0:
            ITEM_INDEX += changes.get("CONTACT_INDEX", 0)
            if ITEM_INDEX < 0:
                ITEM_INDEX = 0
                continue
            elif ITEM_INDEX >= len(contacts):
                ITEM_INDEX = len(contacts) - 1
                continue
            
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

    elif STATUS == "contact_info":
        if STATUS_CHANGED:
            STATUS_CHANGED = False

            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)
            tools.draw_border(draw)

            tools.draw_contact_info(draw, img, contacts[ITEM_INDEX], fb.width, fb.height)

            fb.write(img)
    
    elif STATUS == "main_page":
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

    elif STATUS == "history_info":
        if STATUS_CHANGED:
            STATUS_CHANGED = False
            img = Image.new("RGB", (fb.width, fb.height), color="white")

            draw = ImageDraw.Draw(img)

            tools.draw_buttons(draw, fb.width, fb.height, height=9,font_size=10,texts=("Back", "", "", ""))

            tools.draw_icon(draw, img, "./img/tel.png", (11, 11), (2,1))

            name = history_calls[ITEM_INDEX]["phone_number"].strip()
            name = name[:15] + "..." if len(name) > 15 else name

            name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 10)
            draw.text((14, 0), name, font=name_font, fill="black")

            tools.draw_icon_2(draw, img, hist_type_png[history_calls[ITEM_INDEX]["type"]], (13, 13), (0,13))
            name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 9)
            number_font = ImageFont.truetype("fonts/MS_Sans_Serif.ttf", 10)
            draw.text((14, 13), hist_type_text[history_calls[ITEM_INDEX]["type"]], font=number_font, fill="black")

            tools.draw_icon(draw, img, "./img/hist.png", (11, 11), (2,26))

            dt_gregorian = datetime.fromtimestamp(history_calls[ITEM_INDEX]["timestamp"])
            dt_jalali = jdatetime.datetime.fromgregorian(datetime=dt_gregorian)
            draw.text((14, 26), dt_jalali.strftime("%Y/%m/%d %H:%M:%S"), font=number_font, fill="black")

            
            fb.write(img)




            
    

