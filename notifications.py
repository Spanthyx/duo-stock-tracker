import os
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from dotenv import load_dotenv

def send_message(message: str) -> None:
    load_dotenv()

    token = os.environ["TELEGRAM_BOT_TOKEN"]
    chat_id = os.environ["TELEGRAM_CHAT_ID"]

    url = f"https://api.telegram.org/bot{token}/sendMessage"

    data = urlencode({
        "chat_id": chat_id,
        "text": message
    }).encode("utf-8")

    request = Request(url, data=data, method="POST")

    with urlopen(request, timeout=15) as response:
        print("HTTP status:", response.status)