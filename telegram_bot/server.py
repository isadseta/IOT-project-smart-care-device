import sys
import threading
from telebot import TeleBot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import os
import requests
import urllib
import time, json
from io import BytesIO

from mosqitues_sample_reciever import run_reciever_in_threading

try:
    if os.environ['service_catalog'] == None:
        os.environ['service_catalog'] = 'http://localhost:50010'
except:
    os.environ['service_catalog'] = 'http://localhost:50010'

try:
    if os.environ['telegram_token'] == None:
        os.environ['telegram_token'] = '7765834121:AAGv4Rvsh-lVhsBmjnA_cH6etECDOs1JzhU'
except:
    os.environ['telegram_token'] = '7765834121:AAGv4Rvsh-lVhsBmjnA_cH6etECDOs1JzhU'

try:
    if os.environ['mosquitto_url'] == None:
        os.environ['mosquitto_url'] = "10.48.83.230"
except:
    os.environ['mosquitto_url'] = "10.48.83.230"

try:
    if os.environ['mosquitto_port'] == None:
        os.environ['mosquitto_port'] = "1883"
except:
    os.environ['mosquitto_port'] = "1883"


def change_domain_name(url):
    if os.environ['environment'] == 'RUNNING':
        return url
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
    new_url = f"http://localhost:{port}"
    return new_url


bot = TeleBot(os.environ["telegram_token"])

system_config = None


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
    resource_catalog = system_config_loader()["relational_database_access"]["service_value"]
    resource_catalog = change_domain_name(resource_catalog)
    current_user_with_chat_id = requests.get(
        resource_catalog + f"/UsersDAL?user_telegram_bot_id={message.chat.id}").json()
    print("+++++++++++++++++++++++++++++++++++++++++++++++++")
    print(resource_catalog + f"/UsersDAL?user_telegram_bot_id={message.chat.id}")
    if len(current_user_with_chat_id) > 0:
        if current_user_with_chat_id[0]["user_type"] == 2:
            button1 = InlineKeyboardButton(text="Sick person report", callback_data="doctor_Sick_person_report")
            button2 = InlineKeyboardButton(text="Send message", callback_data="doctor_send_message")
            inline_keyboard = InlineKeyboardMarkup(row_width=2)
            inline_keyboard.add(button1, button2)
            bot.send_message(message.chat.id, "Choose an option:", reply_markup=inline_keyboard)
        else:
            button1 = InlineKeyboardButton(text="My report", callback_data="Sick_person_report")
            button2 = InlineKeyboardButton(text="Send message", callback_data="Sick_person_send_message")
            inline_keyboard = InlineKeyboardMarkup(row_width=2)
            inline_keyboard.add(button1, button2)
            bot.send_message(message.chat.id, "Choose an option:", reply_markup=inline_keyboard)
    else:
        bot.send_message(message.chat.id, "Please enter your SCD username and password seprated by &")
        bot.register_next_step_handler(message, handle_authentication)


def handle_authentication(message):
    credentials = message.text.strip()
    username = credentials.split("&")[0]
    password = credentials.split("&")[1]
    relational_database_url = system_config_loader()["relational_database_access"]["service_value"]
    relational_database_url = change_domain_name(relational_database_url)
    relational_database_url = relational_database_url + f"/UsersDAL?user_email={username}"
    current_user_with_chat_id = requests.get(relational_database_url).text
    current_user_with_chat_id = json.loads(current_user_with_chat_id)
    if len(current_user_with_chat_id) > 0 and current_user_with_chat_id[0]["user_password"] == password:
        relational_database_url = system_config_loader()["relational_database_access"]["service_value"]
        relational_database_url = change_domain_name(relational_database_url)
        relational_database_url = relational_database_url + f"/UsersDAL/{current_user_with_chat_id[0]['id']}"
        current_user_with_chat_id[0]["user_telegram_bot_id"] = message.chat.id
        requests.put(relational_database_url, json.dumps(current_user_with_chat_id[0]))
        if current_user_with_chat_id[0]["user_type"] == 2:
            button1 = InlineKeyboardButton(text="Sick person report", callback_data="doctor_Sick_person_report")
            button2 = InlineKeyboardButton(text="Send message", callback_data="doctor_send_message")
            inline_keyboard = InlineKeyboardMarkup(row_width=2)
            inline_keyboard.add(button1, button2)
            #bot.register_next_step_handler(message, handle_doctor_select_operation)
            bot.send_message(message.chat.id, "Choose an option:", reply_markup=inline_keyboard)
        else:
            button1 = InlineKeyboardButton(text="My report", callback_data="Sick_person_report")
            button2 = InlineKeyboardButton(text="Send message", callback_data="Sick_person_send_message")
            inline_keyboard = InlineKeyboardMarkup(row_width=2)
            inline_keyboard.add(button1, button2)
            bot.send_message(message.chat.id, "Choose an option:", reply_markup=inline_keyboard)
    else:
        bot.send_message(message.chat.id,
                         "Wrong credentials. \n Please enter your SCD username and password seprated by &")
        bot.register_next_step_handler(message, handle_authentication)


def handle_doctor_select_operation(message, operation):
    resource_catalog = system_config_loader()["relational_database_access"]["service_value"]
    resource_catalog = change_domain_name(resource_catalog)
    current_user_with_chat_id = requests.get(
        resource_catalog + f"/UsersDAL?user_telegram_bot_id={message.chat.id}").json()
    if operation == "doctor_send_message":
        resource_catalog = system_config_loader()["resource_catalog"]["service_value"]
        resource_catalog = change_domain_name(resource_catalog)
        list_of_sick_person = requests.get(
            resource_catalog + f"/UsersDoctorsRelationService?docter_user_id={current_user_with_chat_id[0]['id']}").text
        list_of_sick_person = json.loads(list_of_sick_person)
        inline_keyboard = InlineKeyboardMarkup(row_width=2)
        for sick_person in list_of_sick_person:
            button = InlineKeyboardButton(text=f"{sick_person['sick_user_name']}",
                                          callback_data=f"{'doctor_send_message_to|' + str(sick_person['sick_user_id']) + '|' + str(current_user_with_chat_id[0]['id'])}")
            inline_keyboard.add(button)
        bot.send_message(message.chat.id, "Choose an person:", reply_markup=inline_keyboard)
    else:
        resource_catalog = system_config_loader()["resource_catalog"]["service_value"]
        resource_catalog = change_domain_name(resource_catalog)
        list_of_sick_person = requests.get(
            resource_catalog + f"/UsersDoctorsRelationService?docter_user_id={current_user_with_chat_id[0]['id']}").text
        list_of_sick_person = json.loads(list_of_sick_person)
        inline_keyboard = InlineKeyboardMarkup(row_width=3)
        for sick_person in list_of_sick_person:
            button = InlineKeyboardButton(text=f"{sick_person['sick_user_name']}",
                                          callback_data=f"{'doctor_review_report_of|' + str(sick_person['sick_user_id'])}")
            inline_keyboard.add(button)
        bot.send_message(message.chat.id, "Choose an person:", reply_markup=inline_keyboard)


def handle_doctor_send_message_type_message(message, operation):
    destination_user = operation.split("|")[1]
    source_user = operation.split("|")[2]
    print("source user : " + source_user)
    print("destination user : " + destination_user)
    bot.send_message(message.chat.id, "type a message to send")
    bot.register_next_step_handler(message, send_message_to_user, source_user, destination_user)


def send_message_to_user(message, source_user, destination_user):
    send_message_body = '{"sende_user_id":' + source_user + ',"reciever_user_id":' + destination_user + ',"message_content":"' + message.text + '"}'

    notification_server_url = system_config_loader()["notifications"]["service_value"]
    notification_server_url = change_domain_name(notification_server_url)
    notification_server_url = notification_server_url + "/MessagingMicroservice"
    requests.post(notification_server_url, send_message_body)
    bot.send_message(message.chat.id,
                     f"message from {source_user} to {destination_user} sent with content {message.text}")
    send_welcome(message)


def handle_doctor_send_message_send_message(message, source_user, destination_user):
    pass


def handle_doctor_select_operation_send_report(message, operation):
    destination_user = operation.split("|")[1]
    reporting_server_url = system_config_loader()["reporting"]["service_value"]
    reporting_server_url = change_domain_name(reporting_server_url)
    mock_heart_body_temprature = reporting_server_url + "/MockSampleBodyTemprature"
    mock_heart_rate_url = reporting_server_url + "/MockSampleHeartChart"
    image_url = mock_heart_body_temprature  # Replace with the actual image URL
    response = requests.get(image_url)
    print(image_url)
    if response.status_code == 200:
        # Fetch image from URL and send it
        image_data = BytesIO(response.content)
        bot.send_photo(message.chat.id, photo=image_data)
    else:
        bot.send_message(message.chat.id, "Failed to fetch the image from the URL.")

    image_url = mock_heart_rate_url  # Replace with the actual image URL
    response = requests.get(image_url)

    print(image_url)
    if response.status_code == 200:
        # Fetch image from URL and send it
        image_data = BytesIO(response.content)
        bot.send_photo(message.chat.id, photo=image_data)
    else:
        bot.send_message(message.chat.id, "Failed to fetch the image from the URL.")

    send_welcome(message)


def handle_sick_person_select_operation(message, operation):
    resource_catalog = system_config_loader()["relational_database_access"]["service_value"]
    resource_catalog = change_domain_name(resource_catalog)
    current_user = requests.get(resource_catalog + f"/UsersDAL?user_telegram_bot_id={message.chat.id}").json()
    reporting_server_url = system_config_loader()["reporting"]["service_value"]
    reporting_server_url = change_domain_name(reporting_server_url)
    mock_heart_body_temprature = reporting_server_url + "/MockSampleBodyTemprature"

    mock_heart_rate_url = reporting_server_url + "/MockSampleHeartChart"
    image_url = mock_heart_body_temprature  # Replace with the actual image URL
    response = requests.get(image_url)
    bot.send_message(message.chat.id,
                     "Hello " + current_user[0]["user_lastname"] + " " + current_user[0]["user_name"] + ".")
    print(image_url)
    if response.status_code == 200:
        # Fetch image from URL and send it
        image_data = BytesIO(response.content)
        bot.send_photo(message.chat.id, photo=image_data)
    else:
        bot.send_message(message.chat.id, "Failed to fetch the image from the URL.")

    image_url = mock_heart_rate_url  # Replace with the actual image URL
    response = requests.get(image_url)

    print(image_url)
    if response.status_code == 200:
        # Fetch image from URL and send it
        image_data = BytesIO(response.content)
        bot.send_photo(message.chat.id, photo=image_data)
    else:
        bot.send_message(message.chat.id, "Failed to fetch the image from the URL.")

    send_welcome(message)


def handle_Sick_person_send_message(message, operation):
    resource_catalog = system_config_loader()["relational_database_access"]["service_value"]
    resource_catalog = change_domain_name(resource_catalog)
    current_user = requests.get(resource_catalog + f"/UsersDAL?user_telegram_bot_id={message.chat.id}").json()
    resource_catalog = system_config_loader()["resource_catalog"]["service_value"]
    resource_catalog = change_domain_name(resource_catalog)
    list_of_sick_person = requests.get(
        resource_catalog + f"/UsersDoctorsRelationService?sick_user_id={current_user[0]['id']}").text
    list_of_sick_person = json.loads(list_of_sick_person)
    if len(list_of_sick_person) < 1:
        bot.send_message(message.chat.id, "Your doctor is not specified \n please contact the administrator.")
        send_welcome(message)
        return
    doctor_user_id = list_of_sick_person[0]["docter_user_id"]
    #
    bot.send_message(message.chat.id, "type a message to send")
    bot.register_next_step_handler(message, handle_Sick_person_send_message_to_doctor, current_user[0]['id'],
                                   doctor_user_id)


def handle_Sick_person_send_message_to_doctor(message, loggined_user_id, doctor_user_id):
    send_message_body = '{"sende_user_id":' + str(loggined_user_id) + ',"reciever_user_id":' + str(
        doctor_user_id) + ',"message_content":"' + str(message.text) + '"}'

    notification_server_url = system_config_loader()["notifications"]["service_value"]
    notification_server_url = change_domain_name(notification_server_url)
    notification_server_url = notification_server_url + "/MessagingMicroservice"
    requests.post(notification_server_url, send_message_body)
    bot.send_message(message.chat.id,
                     f"message from {loggined_user_id} to {doctor_user_id} sent with content {message.text}")
    send_welcome(message)


def handle_doctors(message):
    pass


def handle_sickperson(message):
    pass


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    print(call.data)
    if call.data == "doctor_Sick_person_report":
        handle_doctor_select_operation(call.message, call.data)
    elif call.data == "doctor_send_message":
        handle_doctor_select_operation(call.message, call.data)
    elif call.data.startswith("doctor_send_message_to"):
        handle_doctor_send_message_type_message(call.message, call.data)
    elif call.data.startswith("doctor_review_report_of"):
        handle_doctor_select_operation_send_report(call.message, call.data)
    elif call.data.startswith("Sick_person_report"):
        handle_sick_person_select_operation(call.message, call.data)
    elif call.data.startswith("Sick_person_send_message"):
        handle_Sick_person_send_message(call.message, call.data)
    else:
        send_welcome(call.message)


mqtt_reviever_thread = threading.Thread(target=run_reciever_in_threading)
mqtt_reviever_thread.start()
sys.stdout.flush()

while True:
    try:
        print("Hello")
        print(os.environ['telegram_token'])
        bot.polling()
    except Exception as ex:
        print("We have error in bot \n call administrator.")
        print(ex)
