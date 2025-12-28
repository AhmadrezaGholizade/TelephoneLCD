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
from call_manager.call_handler import Call_handler
from hardcoded_data import *

def add_login_item():
    global menu_items
    menu_items = menu_items[0:5]
    menu_items.append(("login", {"text": "Login", "icon_path": "img/login.png"}))
def add_logout_item():
    global menu_items
    menu_items = menu_items[0:5]
    menu_items.append(("logout", {"text": "Logout", "icon_path": "img/logout.png"}))


last_event = None
login_state = False
def handle_event(event):
    global last_event, login_state
    if event.get("action") != "ping" and event.get("event") != "pong":
        print("EVENT RECEIVED:", event)
        last_event = event

    if isinstance(event, dict):
        if event.get("event") == "state":
            global STATUS_CHANGED, STATUS
            if event["value"] == "IDLE":
                STATUS_CHANGED = True
                STATUS = 'main_page'
                add_logout_item()
                print("IDLE: Return to main page")
                login_state = event["user"]["phoneNumber"]
                return
            
            if event["value"] == "LOGGED_OUT":
                STATUS_CHANGED = True
                STATUS = 'main_page'
                add_login_item()
                print("LOGED_OUT: Return to main page")
                login_state = None
                return
            
            if event["value"] == "RINGING":
                STATUS_CHANGED = True
                STATUS = 'ringing'
                print("RINGING:  go to RINGING page")
                return
            
            if event["value"] == "INCALL":
                STATUS_CHANGED = True
                STATUS = 'incall'
                print("CALL STARTED:  go to INCALL page")
                return

            if event["value"] == "CALLING":
                STATUS_CHANGED = True
                STATUS = 'calling'
                print("CALLING:  go to CALLING page")
                return

        if event.get("action") == "ping":
            ts = int(time.time() * 1000)
            msg = {
                "event": "pong",
                "ts": ts
            }
            callEngineClient.send(json.dumps(msg))
            return

# Manage LCD
fb = LCDFrameBuffer()
# Helps in Drawing
tools = Tools()


# Handle Key and Phone Events
event_handler = EventHandler()

# Connects to Call Back-end Service
callEngineClient = CallEngineClient(fb, tools)
callEngineClient.connect()
callEngineClient.start(handle_event)

# Handle messege sending to Back-end Service
callHandler = Call_handler(callEngineClient)

STATUS = "main_page"
STATUS_CHANGED = True

ITEM_INDEX = 0
PAGE_NUMBER = 0

# to Handle clock change
last_minute = datetime.now().minute
last_second = datetime.now().second

# Number Printing in typing number page
number_typing = ""



# Check the process of Ping Pong
last_ping = time.monotonic()
last_char_added_time = time.monotonic()
last_pressed = None
char_index = 0

username_text = ""
password_text = ""
active_field = "username"

capsOn = True

while True:
    time.sleep(0.05)
    
    # Send ping 
    if (time.monotonic() - last_ping) > 5:
        last_ping = time.monotonic()
        callHandler.send_ping()

    # Get key changes
    changes = event_handler.handle_key(STATUS)

    # Handle Call orders from changes
    callHandler.main_handler(changes, number_typing, username_text, password_text)

    # Chack Screen light timeout
    event_handler.check_light_timeout(fb)

    # Reset PAGE if changes is not None
    if changes:
        if changes.get('STATUS', False):
            STATUS_CHANGED = True
            STATUS = changes['STATUS']

        # Reset index
        if changes.get("INDEX_RESET", False):
            PAGE_NUMBER = 0
            ITEM_INDEX = 0

        # Set Index
        if changes.get("INDEX_SET", False):
            ITEM_INDEX = changes.get("INDEX_SET", False)

    # Ringing Page
    if STATUS=="ringing":

        if STATUS_CHANGED:
            target_number = ""
            if 'from' in last_event.keys():
                target_number = last_event['from']['phoneNumber']
            elif 'to' in last_event.keys():
                target_number = last_event['to']['phoneNumber']
            elif 'with' in last_event.keys():
                target_number = last_event['with']['phoneNumber']
            STATUS_CHANGED = False
            tools.draw_call_page(fb, target_number, STATUS)
            

    # Calling Page
    if STATUS=="calling":
        if not number_typing:
            STATUS_CHANGED = True
            STATUS = 'main_page'
            continue
        
        if STATUS_CHANGED:
            target_number = ""
            if 'from' in last_event.keys():
                target_number = last_event['from']['phoneNumber']
            elif 'to' in last_event.keys():
                target_number = last_event['to']['phoneNumber']
            elif 'with' in last_event.keys():
                target_number = last_event['with']['phoneNumber']
            STATUS_CHANGED = False
            STATUS_CHANGED = False
            tools.draw_call_page(fb, target_number, STATUS)

    
    if STATUS=="incall":

        if STATUS_CHANGED:
            target_number = ""
            if 'from' in last_event.keys():
                target_number = last_event['from']['phoneNumber']
            elif 'to' in last_event.keys():
                target_number = last_event['to']['phoneNumber']
            elif 'with' in last_event.keys():
                target_number = last_event['with']['phoneNumber']
            STATUS_CHANGED = False
            STATUS_CHANGED = False
            tools.draw_call_page(fb, target_number, STATUS)



    if STATUS=="type_number":
        if changes:
            if changes.get("FIRST_CHAR", False) != False:
                number_typing = changes.get("FIRST_CHAR", False)
            if changes.get("ADD_CHAR", False):
                number_typing += changes.get("ADD_CHAR", False)
            if changes.get("CALL_ITEM", False):
                number_typing = contacts[ITEM_INDEX]['phone_number']
            if changes.get("CALL_HISTORY_ITEM", False):
                number_typing = history_calls[ITEM_INDEX]["phone_number"].strip()
            if changes.get("ERASE", False):
                if number_typing:
                    number_typing = number_typing[:-1]
            
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

            tools.draw_buttons(draw, fb.width, fb.height, height=9,font_size=10,texts=("Back", "Call", "Erase", ""))
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
        
            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)

            tools.draw_history_items(draw, img, history_calls, contacts, ITEM_INDEX, PAGE_NUMBER)

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

        if changes and changes.get("key", False) and ITEM_INDEX in set([0,1,5]): # TEMP 0,1,5
            if changes.get("key", False) == 'Ok': 
                STATUS = menu_items[ITEM_INDEX][0]
            else:
                STATUS = menu_items[int(changes.get("key", False))-1][0]
            ITEM_INDEX = 0
            PAGE_NUMBER = 0
            username_text = ""
            password_text = ""
            STATUS_CHANGED = True
            last_char_added_time = time.monotonic()
            last_pressed = changes.get("key", False)
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
            tools.draw_buttons(draw, 124, fb.height, height=9, font_size=10,texts=("Back", "Detail", "Call", ""))

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
        now = datetime.now()
        # Full redraw when minute changes
        if (now.minute != last_minute) or STATUS_CHANGED:
            if STATUS_CHANGED:
                STATUS_CHANGED = False
            img = Image.new("RGB", (fb.width, fb.height), color="white")
            draw = ImageDraw.Draw(img)
            tools.render_main_page(draw, img, fb.width, fb.height, login_state)
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

            tools.render_history_info(fb, ITEM_INDEX, history_calls, hist_type_png, hist_type_text)

    elif STATUS == "login":
        if changes and changes.get("pressed_button", False):
            pressed = changes.get("pressed_button", "")

            if pressed in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "*", "#"]:
                

                if (pressed == last_pressed) and (time.monotonic() - last_char_added_time) < 0.5:
                    continue
                elif (pressed == last_pressed) and (time.monotonic() - last_char_added_time) < 1.2:
                    char_index += 1
                    if char_index >= len(CHARS[pressed]):
                        char_index = 0      

                    if not capsOn:
                        adding_char = CHARS[pressed][char_index].lower()
                    else:
                        adding_char = CHARS[pressed][char_index]              

                    if active_field == "username":
                        username_text = username_text[:-1] + adding_char
                    elif active_field == "password":
                        password_text = password_text[:-1] + adding_char
                    STATUS_CHANGED = True
                else: 
                    char_index = 0

                    if not capsOn:
                        adding_char = CHARS[pressed][char_index].lower()
                    else:
                        adding_char = CHARS[pressed][char_index]

                    if active_field == "username":
                        username_text += adding_char
                    elif active_field == "password":
                        password_text += adding_char
                    STATUS_CHANGED = True

                last_char_added_time = time.monotonic()
                last_pressed = pressed
                    
            elif pressed in ["Down", "Up", "DND", "Menu"]:
                if (time.monotonic() - last_char_added_time) < 0.5:
                    continue
                last_char_added_time = time.monotonic()
                if pressed == "Menu":
                    capsOn = not capsOn
                    STATUS_CHANGED = True
                elif pressed == "Up":
                    active_field = "username"
                    STATUS_CHANGED = True
                elif pressed == "Down":
                    active_field = "password"
                    STATUS_CHANGED = True
                elif pressed == "DND":
                    if active_field == "username" and username_text:
                        username_text = username_text[:-1]
                    elif active_field == "password" and password_text:
                        password_text = password_text[:-1]
                    STATUS_CHANGED = True



        if STATUS_CHANGED:
            STATUS_CHANGED = False
            tools.render_login_page(fb, capsOn, active_field, username_text, password_text)

    elif STATUS == "logout":
        if STATUS_CHANGED:
            STATUS_CHANGED = False
            tools.render_logout_page(fb)




            
    





            
    

