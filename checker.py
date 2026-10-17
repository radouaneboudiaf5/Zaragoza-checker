import time
import requests
import os

TELEGRAM_BOT_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')

def send_telegram_notification(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            print("تم إرسال إشعار التيليجرام بنجاح!")
        else:
            print("فشل إرسال الإشعار:", response.text)
    except Exception as e:
        print("خطأ في الاتصال بتيليجرام:", e)

def check_zaragoza_appointments():
    print("جاري فحص موقع المواعيد في سرقسطة...")
    url = "https://icp.administracionelectronica.gob.es/icpplus/index.sh"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            print("تم الاتصال بالموقع بنجاح.")
        else:
            print(f"الموقع رد برمز خطأ: {response.status_code}")
    except Exception as e:
        print("حدث خطأ أثناء الاتصال بالموقع:", e)

if __name__ == "__main__":
    check_zaragoza_appointments()
