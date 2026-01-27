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
# contacts = [
#     {"nickName": "Ali Rahmatlahi", "phoneNumber": "09123456789", "protocolType": "SIP"},
#     {"nickName": "حسین هزار دستان کلکچالی", "phoneNumber": "09123456789", "protocolType": "SIP"},
#     {"nickName": "احمدرضا قلی زاده تلیکانی اصل", "phoneNumber": "09123456789", "protocolType": "SIP"},
#     {"nickName": "Reza", "phoneNumber": "02144556677", "protocolType": "SIP"},
#     {"nickName": "سارا کریمی", "phoneNumber": "989121234567", "protocolType": "WRTC"},
#     {"nickName": "NimaNimaNimaNimaNimaNimaNimaNima", "phoneNumber": "447911123456", "protocolType": "WRTC"},
#     {"nickName": "Maryam", "phoneNumber": "0913555777", "protocolType": "SIP"},
#     {"nickName": "حسین", "phoneNumber": "120", "protocolType": "SIP"},
#     {"nickName": "هوتن", "phoneNumber": "004917612345678", "protocolType": "WRTC"},
#     {"nickName": "آرمان", "phoneNumber": "+5551234", "protocolType": "WRTC"},
#     {"nickName": "Zahra", "phoneNumber": "0012025550198", "protocolType": "SIP"},
#     {"nickName": "شکیبا", "phoneNumber": "888777666555", "protocolType": "WRTC"},
#     {"nickName": "مهدی", "phoneNumber": "09011223344", "protocolType": "SIP"},
#     {"nickName": "Navid", "phoneNumber": "987654321045", "protocolType": "WRTC"},
#     {"nickName": "Atena", "phoneNumber": "98765", "protocolType": "WRTC"},
#     {"nickName": "reza", "phoneNumber": "71001", "protocolType": "WRTC"},
#     {"nickName": "ali", "phoneNumber": "71002", "protocolType": "WRTC"},
# ]
contacts = []

# history_calls = [
#     {
#         "phoneNumber": "71002",
#         "type": "incoming",
#         "timestamp": 1734699220  # 2024-12-19 09:50:00
#     },
#     {
#         "phoneNumber": "71001",
#         "type": "incoming",
#         "timestamp": 1734599220  # 2024-12-19 09:50:00
#     },
#     {
#         "phoneNumber": "09123456789",
#         "type": "incoming",
#         "timestamp": 1734598200  # 2024-12-19 09:50:00
#     },
#     {
#         "phoneNumber": "4432",
#         "type": "incoming",
#         "timestamp": 1734598200  # 2024-12-19 09:50:00
#     },
#     {
#         "phoneNumber": "09123456789",
#         "type": "missed",
#         "timestamp": 1734594300  # 2024-12-19 08:45:00
#     },
#     {
#         "phoneNumber": "021556677",
#         "type": "outgoing",
#         "timestamp": 1734589800  # 2024-12-19 07:30:00
#     },
#     {
#         "phoneNumber": "989121234567",
#         "type": "incoming",
#         "timestamp": 1734546000  # 2024-12-18 19:20:00
#     },
#     {
#         "phoneNumber": "447911123456",
#         "type": "missed",
#         "timestamp": 1734517200  # 2024-12-18 11:00:00
#     },
#     {
#         "phoneNumber": "0901223344",
#         "type": "outgoing",
#         "timestamp": 1734474000  # 2024-12-17 23:00:00
#     },
#     {
#         "phoneNumber": "0012025550198",
#         "type": "incoming",
#         "timestamp": 1734438000  # 2024-12-17 13:00:00
#     },
#     {
#         "phoneNumber": "004917612345678",
#         "type": "missed",
#         "timestamp": 1734393000  # 2024-12-16 23:30:00
#     },
#     {
#         "phoneNumber": "004917612345678",
#         "type": "missed",
#         "timestamp": 1734393000  # 2024-12-16 23:30:00
#     }
# ]

history_calls = []

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