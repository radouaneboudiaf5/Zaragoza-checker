import os
import requests

# إعداد البيانات الشخصية والموقع
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

NIE = "Z5249665N"
NAME = "Tariq mecheter"
COUNTRY = "ALGERIA"  # الجزائر

URL_BASE = "https://icp.administracionelectronica.gob.es/icpplus/citas"

def send_telegram(message):
    if BOT_TOKEN and CHAT_ID:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        payload = {"chat_id": CHAT_ID, "text": message}
        try:
            requests.post(url, json=payload, timeout=10)
        except Exception as e:
            print(f"Error sending Telegram message: {e}")

def check_appointments():
    session = requests.Session()
    session.headers.update({
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8"
    })

    try:
        # 1. إرسال طلب تصفح الجلسة واختيار سرقسطة (Zaragoza - Province 50)
        p_data = {"form": "", "provincia": "50"}
        res1 = session.post(f"{URL_BASE}/acInic", data=p_data, timeout=15)
        
        # 2. تحديد المعاملة: أخذ البصمات POLICÍA-TOMA DE HUELLAS (Expedición de tarjeta)
        tramite_data = {
            "form": "",
            "tipo": "pc",
            "provincia": "50",
            "sede": "4000",
            "tramite_grupo[1]": "4036" # رمز إجراء البصمات
        }
        res2 = session.post(f"{URL_BASE}/acTramite", data=tramite_data, timeout=15)

        # 3. محاكاة اختيار الدخول بدون الشهادة الرقمية (Presentación sin Cl@ve)
        res3 = session.post(f"{URL_BASE}/acEntrada", data={"form": ""}, timeout=15)

        # 4. إرسال البيانات الشخصية وراء الكواليس (NIE, Name, Country)
        user_data = {
            "txtIdCitado": NIE,
            "txtDesCitado": NAME,
            "txtPaisNac": "203", # الجزائر
            "btnEnviar": "Aceptar"
        }
        res4 = session.post(f"{URL_BASE}/acValidar", data=user_data, timeout=15)

        # 5. طلب صفحة الفحص النهائية للمواعيد
        res_final = session.post(f"{URL_BASE}/acCita", data={"form": "", "btnSiguiente": "Siguiente"}, timeout=15)
        text = res_final.text

        # التحقق من نص النتيجة
        if "En este momento no hay citas disponibles" in text or "no hay citas disponibles" in text:
            print("النتيجة: لا توجد مواعيد متاحة حالياً.")
        else:
            # تم العثور على موعد!
            msg = (
                "🎉 **تم العثور على موعد لـ TIE في Zaragoza!**\n\n"
                f"👤 **الاسم:** {NAME}\n"
                f"🆔 **الـ NIE:** {NIE}\n"
                "📍 **الإجراء:** أخذ البصمات (Toma de Huellas)\n\n"
                "سارع بالدخول الآن للحجز عبر الرابط:\n"
                "https://icp.administracionelectronica.gob.es/icpplus/index.html"
            )
            print("تم العثور على مواعيد! إرسال إشعار عبر تيليجرام...")
            send_telegram(msg)

    except Exception as e:
        print(f"حدث خطأ أثناء الاتصال بالنظام: {e}")

if __name__ == "__main__":
    check_appointments()
