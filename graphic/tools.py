from PIL import Image, ImageDraw, ImageFont
from LCD.FB import LCDFrameBuffer
from datetime import datetime
import jdatetime

class Tools:
    hist_type_png = {
        "missed": "./img/miss.png",
        "incoming": "./img/in.png",
        "outgoing": "./img/out.png"
    }
    def render_main_page(self, draw, img, width, height, login_state, DND):
        self.draw_clock(draw)
        self.draw_date(draw)
        self.draw_id(draw, img, login_state)
        self.draw_buttons(draw, width, height)
        if not DND:
            draw.line([64, 34, 97, 48], width=2)

    def draw_call_page(self, fb, number, type_):
        img = Image.new("RGB", (fb.width, fb.height), color="white")
        draw = ImageDraw.Draw(img)
        self.draw_icon_2(draw, img, "./img/in.png", (13, 13), (1,1))
        name_font = ImageFont.truetype("fonts/MS_Sans_Serif.ttf", 11)
        type_dict = {
            "incall": "IN CALL",
            "ringing": "INCOMING CALL...",
            "calling": "OUTGOING CALL...",
        }
        draw.text((15, 3), type_dict[type_], font=name_font, fill="black")
        name_font = ImageFont.truetype("fonts/MS_Sans_Serif.ttf", 12)
        draw.text((15, 18), number, font=name_font, fill="black")

        if type_=="incall":
            self.draw_buttons(draw, fb.width, fb.height, texts=("HngUp", "", "", ""))
        if type_=="ringing":
            self.draw_buttons(draw, fb.width, fb.height, texts=("Answ.", "Reject", "", ""))
        if type_=="calling":
            self.draw_buttons(draw, fb.width, fb.height, texts=("HngUp", "", "", ""))
        fb.write(img)
    
    def draw_initialization(self,fb):
        img = Image.new("RGB", (fb.width, fb.height), color="black")
        draw = ImageDraw.Draw(img)
        name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 15)
        draw.text((8, 10), "CONNECTING...", font=name_font, fill="white")
        fb.write(img)
    

    def draw_clock(self, draw,
               pos_hour=(17, 20),
               pos_min=(55, 20),
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

    def draw_id(self,draw,
                img, login_state,
                icon_path="./img/tel.png",
                icon_pos=(72, 3),
                icon_size=(14, 14),
                text_pos=(106, 10),
                font_path="fonts/MS_Sans_Serif.ttf",
                font_size=10,
                color="black"):
        if login_state:
            font = ImageFont.truetype(font_path, font_size)
            self.draw_icon(draw, img, icon_path, icon_size, icon_pos)

            draw.text(text_pos, login_state, font=font, fill=color, anchor="mm")
        else: 
            font = ImageFont.truetype(font_path, 9)
            draw.text((107, 9), "SignedOut", font=font, fill=color, anchor="mm")
            self.draw_icon(draw, img, "./img/forbidden.png", (11, 11), (74, 4))

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

    def draw_contact_rows(self, draw, contacts, CONTACT_INDEX, CONTACT_PAGE_NUMBER):
        name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 10)

        for n, i in enumerate(range(CONTACT_PAGE_NUMBER * 3, min(CONTACT_PAGE_NUMBER * 3 + 3, len(contacts)))):
            name = contacts[i]["nick_name"].strip()
            print_name = name[:22] + "..." if len(name) > 22 else name

            # Black Theme for Selected Contact
            color = "black"
            if i == CONTACT_INDEX:
                color = "white"
                draw.rectangle([1, 1 + 13 * n, 122, -1 + 13 * (n+1)], fill="black")
                
            # Name    
            draw.text((3, 0 + 12 * n), print_name, font=name_font, fill=color)

    def draw_header(self, draw, header="Contacts"):
        name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 10)
        draw.rectangle([1, 0, 122, 9], fill="black")
        draw.text((57, 6), header, font=name_font, fill="white", anchor="mm")

    def draw_border(self, draw, pos=[0, 0, 127, 47] , width=1):
        draw.rectangle(pos, outline="black", width=width)

    def draw_scrollbar(self, draw, CONTACT_PAGE_NUMBER, len_contacts):
        draw.rectangle([124, 0, 124, 48], fill="black") # seperator line
        page_ratio = 3 / len_contacts * 48
        draw.rectangle([125, CONTACT_PAGE_NUMBER * page_ratio, 127, (CONTACT_PAGE_NUMBER + 1) * page_ratio], fill="black")

    def draw_icon(self, draw, img, icon_path, icon_size, icon_pos, color='black', threshold=128):
        # open icon (ignore alpha)
        icon = Image.open(icon_path).convert("L")  # grayscale
        icon = icon.resize(icon_size, Image.LANCZOS)

        # make binary mask using threshold
        mask = icon.point(lambda p: 0 if p > threshold else 255)

        # create solid color icon
        colored_icon = Image.new("RGBA", icon.size, color)

        # paste using threshold mask
        img.paste(colored_icon, icon_pos, mask)
    
    def draw_icon_2(self, draw, img, icon_path, icon_size, icon_pos): 
        icon = Image.open(icon_path).convert("RGBA") 
        icon = icon.resize(icon_size, Image.LANCZOS) 
        img.paste(icon, icon_pos, icon)

    def draw_contact_info(self, draw, img, contact, fb_width, fb_height):
        self.draw_icon(draw, img, "./img/person.png", (14, 14), (3,3))
        self.draw_icon(draw, img, "./img/tel.png", (14, 14), (3,17))

        name = contact["nick_name"].strip()
        print_name = name[:18] + "..." if len(name) > 18 else name

        number = contact["phone_number"].strip()
        print_number = number[:20] + "..." if len(number) > 20 else number

        name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 12)
        draw.text((18, 1), print_name, font=name_font, fill="black")

        number_font = ImageFont.truetype("fonts/MS_Sans_Serif.ttf", 11)
        type_font   = ImageFont.truetype("fonts/Google_Sans_Flex/static/GoogleSansFlex_9pt-Regular.ttf", 9)

        x, y = 18, 19
        draw.text((x, y), print_number, font=number_font, fill="black")

        w = draw.textlength(print_number, font=number_font)

        draw.text((x + w, y + 1), f"({contact['user_type'].strip()})",
                font=type_font, fill="black")

        self.draw_buttons(draw, fb_width, fb_height, texts=("Back", "Call", "", ""))

    def one_to_six_culs(self, draw, len_menu_items):
        name_font = ImageFont.truetype("fonts/MS_Sans_Serif.ttf", 10)

        draw.rectangle([1, 1, 7, 35], fill="black")
        draw.rectangle([63, 1, 70, 35], fill="black")
        for i in range(len_menu_items):
            x_pos = 64 if (i > 2) else 1
            n = i % 3
            draw.text((x_pos, 12 * n), f"{i+1}", font=name_font, fill="white")

    def draw_manu_items(self, draw, img, menu_items, BOLD_ITEM_INDEX):
        name_font = ImageFont.truetype("fonts/MS_Sans_Serif.ttf", 10)

        for i in range(len(menu_items)):
            x_pos = 87 if (i > 2) else 24
            n = i % 3

            print_name = menu_items[i][1]["text"].strip()
            color = "black"
            if i == BOLD_ITEM_INDEX:
                color = "white"
                draw.rectangle([x_pos-16 , 12 * n, x_pos+38, 12 * (n+1)], fill="black")
                                    
            self.draw_icon(draw, img, menu_items[i][1]["icon_path"], (13, 13), (x_pos-15,n*12), color=color)
            
            draw.text((x_pos, 12 * n), print_name, font=name_font, fill=color)

    def draw_history_items(self, draw, img, history_calls, contacts, ITEM_INDEX, PAGE_NUMBER):
        name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 10)
        for n, i in enumerate(range(PAGE_NUMBER * 3, min(PAGE_NUMBER * 3 + 3, len(history_calls)))):
            name = history_calls[i]["phone_number"].strip()
            for contact in contacts:
                if contact["phone_number"] == name:
                    name = contact["nick_name"]

            name = name[:15] + "..." if len(name) > 15 else name

            # # Black Theme for Selected Contact
            color = "black"
            if i == ITEM_INDEX:
                color = "white"
                draw.rectangle([11, 1 + 13 * n, 122, -1 + 13 * (n+1)], fill="black")
            
            self.draw_icon_2(draw, img, self.hist_type_png[history_calls[i]["type"]], (13, 13), (0,n*12))
            # Name    
            draw.text((12, 0 + 12 * n), name, font=name_font, fill=color)
    
    def render_logout_page(self, fb):
        img = Image.new("RGB", (fb.width, fb.height), color="white")
        draw = ImageDraw.Draw(img)
        self.draw_buttons(draw, fb.width, fb.height, height=11,font_size=10,texts=("Back", "Yes !", "", ""))
        name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 14)
        draw.text((3, 3), "Are You Sure?", font=name_font, fill="black")
        fb.write(img)

    def render_login_page(self, fb, capsOn,  active_field, username_text, password_text):
        img = Image.new("RGB", (fb.width, fb.height), color="white")
        draw = ImageDraw.Draw(img)
        caps_text = "Cps:ON" if capsOn else "Cps:Off"
        self.draw_buttons(draw, fb.width, fb.height, height=11,font_size=9,texts=("Back", "Enter", "Erase", caps_text))
        name_font = ImageFont.truetype("fonts/MS_Sans_Serif.ttf", 9)
        draw.text((3, 3), "UserName:", font=name_font, fill="black")
        draw.text((3, 21), "Password:", font=name_font, fill="black")

        self.draw_border(draw, pos=[45, 2, 123, 15])
        self.draw_border(draw, pos=[45, 20, 123, 33])
        if active_field == "username":
            draw.rectangle([44, 1, 124, 16], outline="black", width=2)
        else:
            draw.rectangle([44, 19, 124, 34], outline="black", width=2)

        name_font = ImageFont.truetype("fonts/MS_Sans_Serif.ttf", 11)
        un_prefix = ""
        if len(username_text) > 12:
            un_prefix = "..."
        draw.text((47, 3), un_prefix+username_text[-12:], font=name_font, fill="black")
        pw_prefix = ""
        if len(password_text) > 12:
            pw_prefix = "..."
        if password_text:
            draw.text((47, 21), pw_prefix + "*" * (len(password_text[-11:])-1) + password_text[-1], font=name_font, fill="black")
    
        
        fb.write(img)

    def render_history_info(self, fb, ITEM_INDEX, history_calls, hist_type_png, hist_type_text):
        img = Image.new("RGB", (fb.width, fb.height), color="white")

        draw = ImageDraw.Draw(img)

        self.draw_buttons(draw, fb.width, fb.height, height=9,font_size=10,texts=("Back", "Call", "", ""))

        self.draw_icon(draw, img, "./img/tel.png", (11, 11), (2,1))

        name = history_calls[ITEM_INDEX]["phone_number"].strip()
        name = name[:15] + "..." if len(name) > 15 else name

        name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 10)
        draw.text((14, 0), name, font=name_font, fill="black")

        self.draw_icon_2(draw, img, hist_type_png[history_calls[ITEM_INDEX]["type"]], (13, 13), (0,13))
        name_font = ImageFont.truetype("fonts/fonts/Sahel-Bold.ttf", 9)
        number_font = ImageFont.truetype("fonts/MS_Sans_Serif.ttf", 10)
        draw.text((14, 13), hist_type_text[history_calls[ITEM_INDEX]["type"]], font=number_font, fill="black")

        self.draw_icon(draw, img, "./img/hist.png", (11, 11), (2,26))

        dt_gregorian = datetime.fromtimestamp(history_calls[ITEM_INDEX]["timestamp"])
        dt_jalali = jdatetime.datetime.fromgregorian(datetime=dt_gregorian)
        draw.text((14, 26), dt_jalali.strftime("%Y/%m/%d %H:%M:%S"), font=number_font, fill="black")

        
        fb.write(img)

    


