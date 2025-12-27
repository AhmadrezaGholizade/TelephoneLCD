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
    ("login", {"text": "Login", "icon_path": "img/login.png"}),
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
    {"nick_name": "Atena", "phone_number": "98765", "user_type": "WRTC"},
    {"nick_name": "reza", "phone_number": "71001", "user_type": "WRTC"},
    {"nick_name": "ali", "phone_number": "71002", "user_type": "WRTC"},
]
history_calls = [
    {
        "phone_number": "71002",
        "type": "incoming",
        "timestamp": 1734699220  # 2024-12-19 09:50:00
    },
    {
        "phone_number": "71001",
        "type": "incoming",
        "timestamp": 1734599220  # 2024-12-19 09:50:00
    },
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

CHARS={
    '0': ['0'],
    '1': ['1'],
    '2': ['2', 'A', 'B', 'C'],
    '3': ['3', 'D', 'E', 'F'],
    '4': ['4', 'G', 'H', 'I'],
    '5': ['5', 'J', 'K', 'L'],
    '6': ['6', 'M', 'N', 'O'],
    '7': ['7', 'P', 'Q', 'R', 'S'],
    '8': ['8', 'T', 'U', 'V'],
    '9': ['9', 'W', 'X', 'Y', 'Z'],
    '*': ['*', '.'],
    '#': ['#'],
}