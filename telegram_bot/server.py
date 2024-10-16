# telegram authetication finished
from telebot import TeleBot
from telebot.types import InlineKeyboardButton,InlineKeyboardMarkup
import os
import requests
import urllib
import time,json


def change_domain_name(url):
    """Extracts the port number from a URL.

    Args:
        url: The input URL.

    Returns:
        The port number, or None if no port is specified.
    """

    parsed_url = urllib.parse.urlparse(url)
    port = parsed_url.port

    if port is None:
        # Default port for common protocols
        if parsed_url.scheme == "http":
            port = 80
        elif parsed_url.scheme == "https":
            port = 443
        elif parsed_url.scheme == "ftp":
            port = 21
    new_url=f"http://localhost:{port}"
    return new_url

bot = TeleBot(token='7765834121:AAGv4Rvsh-lVhsBmjnA_cH6etECDOs1JzhU')

system_config=None

try:
    if os.environ['service_catalog'] == None:
        os.environ['service_catalog'] = 'http://localhost:50010'
except:
    os.environ['service_catalog'] = 'http://localhost:50010'


def reload_config():
    global system_config
    # getting system configs
    service_catalog_address = os.environ['service_catalog'] + "/ServiceCatalog/summary"
    while True:
        try:
            system_config = requests.get(service_catalog_address)
            print("==================================================================================")
            print("Configuration loaded successfully.")
            print(system_config)
            break
        except Exception as ex:
            print("==================================================================================")
            print(f"Unsucceessfull loading cofiguration because of \n {ex}.")
            time.sleep(5)

def system_config_loader():
    global system_config
    reload_config()
    system_config_as_cixtionary = {}
    for service_item in system_config.json():
        print(service_item)
        system_config_as_cixtionary[service_item["service_name"]] = service_item
    print(system_config_as_cixtionary)
    return system_config_as_cixtionary

@bot.message_handler(commands=['start'])
def send_welcome(message):
    resource_catalog=system_config_loader()["relational_database_access"]["service_value"]
    resource_catalog=change_domain_name(resource_catalog)
    current_user_with_chat_id=requests.get(resource_catalog+f"/UsersDAL?user_telegram_bot_id={message.chat.id}").json()
    print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    print(resource_catalog+f"/UsersDAL?user_telegram_bot_id={message.chat.id}")
    if len(current_user_with_chat_id)>0:
        if current_user_with_chat_id[0]["user_type"] == 2:
            button1 = InlineKeyboardButton(text="Sick person report", callback_data="doctor_Sick_person_report")
            button2 = InlineKeyboardButton(text="Send message", callback_data="doctor_send_message")
            inline_keyboard=InlineKeyboardMarkup(row_width=2)
            inline_keyboard.add(button1,button2)
            bot.send_message(message.chat.id, "Choose an option:", reply_markup=inline_keyboard)
            bot.register_next_step_handler(message, handle_doctor_select_operation)
        else:
            button1 = InlineKeyboardButton(text="My report", callback_data="Sick_person_report")
            button2 = InlineKeyboardButton(text="Send message", callback_data="send_message")
            inline_keyboard=InlineKeyboardMarkup(row_width=2)
            inline_keyboard.add(button1,button2)
            bot.send_message(message.chat.id, "Choose an option:", reply_markup=inline_keyboard)
            bot.register_next_step_handler(message, handle_sick_person_select_operation)
    else:
        bot.send_message(message.chat.id, "Please enter your SCD username and password seprated by &")
        bot.register_next_step_handler(message, handle_authentication)
        def handle_authentication(message):
    credentials = message.text.strip()
    username = credentials.split("&")[0]
    password = credentials.split("&")[1]
    relational_database_url=system_config_loader()["relational_database_access"]["service_value"]
    relational_database_url=change_domain_name(relational_database_url)
    relational_database_url=relational_database_url+f"/UsersDAL?user_email={username}"
    current_user_with_chat_id=requests.get(relational_database_url).text
    current_user_with_chat_id=json.loads(current_user_with_chat_id)
    if len(current_user_with_chat_id)>0 and current_user_with_chat_id[0]["user_password"]==password:
        relational_database_url=system_config_loader()["relational_database_access"]["service_value"]
        relational_database_url=change_domain_name(relational_database_url)
        relational_database_url=relational_database_url+f"/UsersDAL/{current_user_with_chat_id[0]['id']}"
        current_user_with_chat_id[0]["user_telegram_bot_id"]=message.chat.id
        requests.put(relational_database_url,json.dumps(current_user_with_chat_id[0]))
        if current_user_with_chat_id[0]["user_type"] == 2:
            button1 = InlineKeyboardButton(text="Sick person report", callback_data="doctor_Sick_person_report")
            button2 = InlineKeyboardButton(text="Send message", callback_data="doctor_send_message")
            inline_keyboard=InlineKeyboardMarkup(row_width=2)
            inline_keyboard.add(button1,button2)
            #bot.register_next_step_handler(message, handle_doctor_select_operation)
            bot.send_message(message.chat.id, "Choose an option:", reply_markup=inline_keyboard)
        else:
            button1 = InlineKeyboardButton(text="My report", callback_data="Sick_person_report")
            button2 = InlineKeyboardButton(text="Send message", callback_data="send_message")
            inline_keyboard=InlineKeyboardMarkup(row_width=2)
            inline_keyboard.add(button1,button2)
            #bot.register_next_step_handler(message, handle_sick_person_select_operation)
            bot.send_message(message.chat.id, "Choose an option:", reply_markup=inline_keyboard)
    else:
        bot.send_message(message.chat.id, "Wrong credentials. \n Please enter your SCD username and password seprated by &")
        bot.register_next_step_handler(message, handle_authentication)
def handle_doctor_select_operation(message,operation):
    print("1")
    resource_catalog=system_config_loader()["relational_database_access"]["service_value"]
    print("2")
    resource_catalog=change_domain_name(resource_catalog)
    print("3")
    current_user_with_chat_id=requests.get(resource_catalog+f"/UsersDAL?user_telegram_bot_id={message.chat.id}").json()
    print("4")
    if operation=="doctor_send_message":
        print("5")
        resource_catalog=system_config_loader()["resource_catalog"]["service_value"]
        print("6")
        resource_catalog=change_domain_name(resource_catalog)
        print("7")
        print(resource_catalog+f"/UsersDoctorsRelationService?docter_user_id={current_user_with_chat_id[0]['id']}")
        list_of_sick_person=requests.get(resource_catalog+f"/UsersDoctorsRelationService&docter_user_id={current_user_with_chat_id[0]['id']}").text
        print(list_of_sick_person)
        list_of_sick_person=json.loads(list_of_sick_person)
        print(list_of_sick_person)
        print("81")
        inline_keyboard=InlineKeyboardMarkup(row_width=2)
        print("9")
        for sick_person in list_of_sick_person:
            button = InlineKeyboardButton(text=f"{sick_person['sick_user_name']}", callback_data=f"{sick_person['sick_user_id']}")
            inline_keyboard.add(button)
        print("11")
        bot.send_message(message.chat.id, "Choose an person:", reply_markup=inline_keyboard)
        print("12")
        bot.register_next_step_handler(message, handle_doctor_select_operation_send_message)
    else:
        resource_catalog=system_config_loader()["resource_catalog"]["service_value"]
        resource_catalog=change_domain_name(resource_catalog)
        list_of_sick_person=requests.get(resource_catalog+f"/UsersDoctorsRelationService&docter_user_id={current_user_with_chat_id[0].id}").json()
        inline_keyboard=InlineKeyboardMarkup(row_width=2)
        for sick_person in list_of_sick_person:
            button = InlineKeyboardButton(text=f"{sick_person['sick_user_name']}", callback_data=f"{sick_person['sick_user_id']}")
            inline_keyboard.add(button)
        bot.send_message(message.chat.id, "Choose an person:", reply_markup=inline_keyboard)
        bot.register_next_step_handler(message, handle_doctor_select_operation_send_report)



def handle_doctor_select_operation_send_message(message):
    pass
def handle_doctor_select_operation_send_report(message):
    pass

def handle_sick_person_select_operation(message):
    pass

def handle_doctors(message):
    pass

def handle_sickperson(message):
    pass
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print("Handle operation called")
    print(call.data)
    if call.data == "doctor_Sick_person_report":
        handle_doctor_select_operation(call.message,call.data)
    elif call.data == "doctor_send_message":
        handle_doctor_select_operation(call.message,call.data)


bot.polling()
