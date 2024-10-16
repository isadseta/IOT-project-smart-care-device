# for testings
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import paho.mqtt.client as mqtt
import requests

# توکن بات تلگرام خود را در این قسمت قرار دهید
TOKEN = '7702894514:AAHMYZJxb3OJ9x7_oKi_mLmBjjhM6eB8kwE'

# تابعی برای پاسخ به دستور /start
def start(update, context):
    update.message.reply_text('سلام! من بات Smart Care هستم. چطور می‌توانم کمک کنم؟')

# تابعی برای پاسخ به پیام‌های متنی
def echo(update, context):
    update.message.reply_text(update.message.text)

# راه‌اندازی بات تلگرام
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# ثبت دستورات و پیام‌های دریافتی
dispatcher.add_handler(CommandHandler('start', start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# تنظیمات اولیه MQTT
MQTT_BROKER = "mqtt.eclipse.org"  # یا آدرس سرور MQTT خود
MQTT_PORT = 1883
TOPIC = "smartcare/device1/temperature"

# تابعی برای اتصال به MQTT
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(TOPIC)

# تابعی برای دریافت پیام‌ها از MQTT
def on_message(client, userdata, msg):
    print(f"Topic: {msg.topic}\nMessage: {msg.payload.decode()}")

# ساخت client برای ارتباط با MQTT
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

# اتصال به MQTT
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

# تابعی برای ارسال پیام به تلگرام
def send_notification(chat_id, message):
    updater.bot.send_message(chat_id=891611505, text=message)

# فرض کنید chat_id را از قبل دارید و می‌خواهید پیامی ارسال کنید
# send_notification(chat_id=123456789, message="وضعیت سلامتی بیمار به حالت اورژانسی تغییر کرد!")

# دریافت داده از REST API
response = requests.get("http://api.smartcare.com/patient/12345")
if response.status_code == 200:
    data = response.json()
    print(data)

# شروع بات
updater.start_polling()
updater.idle()
