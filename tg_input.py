import json
import requests
import time
import telebot
import restore
import queue
import threading
import concurrent.futures
from telebot import types


bot = telebot.TeleBot("5836636187:AAGADUyLUl7NxeSCImS3mpN6_I7dFm338V4")

is_process_running = False
file_id = ''
request_queue = queue.Queue()
user_states = {}

languages = {
    "uzbek": {
        "start":  "\n<b>Salom, bu FotoEffectBot.</b>"
"\nBu bot orqali siz xira rasmlaringzini tiniqlashirishingiz mumkin."
"\n"
"\n"
"\nRasimingizni file holatida yuboring",
        "running_process": "Rasim ishlov jarayonida.",
        "wait": "Jarayon ishga tushgan. Ilstimos kuting!",
        "error": "Rasimni tiklashda xatolik yuz berdi.",
        "correct_type": "Iltimos, rasimni file holatida yuboring."
    },
    "russian": {
        "start":  "\n<b>Привет, это FotoEffectBot.</b>"
"\nЭтот бот может улучшить качество ваших фотографий."
"\nПользуйтесь на здоровье!"
"\n"
"\n"
"\nОтправьте фотографий в формате файл без сжатия.",
        "running_process": "изображение обрабатывается.",
        "wait": "Процесс запущен. Пожалуйста, подождите!",
        "error": "Ошибка во время обработки изображения.",
        "correct_type": "Пожалуйста, отправьте изображение в формате файл."
    },
    "english": {
        "start": "\n<b>Hello, this is FotoEffectBot.</b>"
"\nThis bot allows you to restore your photos, and makes them better.""\n"
"\n"
"\nSend photos as files.",
        "running_process": "Image is being processed..",
        "wait": "Process is running. Please wait!",
        "error": "Error occurred while processing image.",
        "correct_type": "Please send image in file format."
    }
}

    
@bot.message_handler(commands=["start", "help"])
def start(msg):
    start_msg = ''
    
    if msg.from_user.language_code == "uz":
        start_msg = languages['uzbek']["start"]
    elif msg.from_user.language_code == "ru":
        start_msg = languages['russian']["start"]
    else:
        start_msg = languages['english']["start"]
        
    bot.send_message(msg.chat.id,
    start_msg, parse_mode="HTML")
    


    
@bot.message_handler(content_types=["text"])
def handle_message(msg):
    global callback_data
    global is_process_running
    
    process_msg = ''
    
    if msg.from_user.language_code == "uz":
        process_msg = languages['uzbek']["wait"]
    elif msg.from_user.language_code == "ru":
        process_msg = languages['russian']["wait"]
    else:
        process_msg = languages['english']["wait"]
    

    if is_process_running:
        bot.reply_to(msg, process_msg)
    else:
        is_process_running = True


@bot.message_handler(content_types=["photo", "document", "video"])
def handle_photo(msg):
    global file_id
    global is_process_running
    global file_url
    global chat_id
    chat_id = msg.chat.id
    
    wait_msg = ''
    correct_type_msg = ''
    running_process_msg = ''
    
    if msg.from_user.language_code == "uz":
        wait_msg = languages['uzbek']["wait"]
        correct_type_msg = languages['uzbek']["correct_type"]
    elif msg.from_user.language_code == "ru":
        wait_msg = languages['russian']["wait"]
        correct_type_msg = languages['russian']["correct_type"]
        running_process_msg = languages['russian']["running_process"]
    else:
        wait_msg = languages['english']["wait"]
        correct_type_msg = languages['english']["correct_type"]
        running_process_msg = languages['english']["running_process"]
    

    if chat_id in user_states and user_states[chat_id] == "processing":
        bot.send_message(chat_id, wait_msg)
        return
    # Geeting file_id-----------------
    if msg.content_type == "document":
        file_id = msg.document.file_id
    else:
        bot.send_message(chat_id, correct_type_msg)
        return
    file_url = 'https://api.telegram.org/file/bot5836636187:AAGADUyLUl7NxeSCImS3mpN6_I7dFm338V4/' + get_file_path(file_id)
    user_states[chat_id] = "queued"
    bot.send_message(chat_id, running_process_msg)
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future = executor.submit(restore_image, file_url, chat_id)
        future.add_done_callback(callback)


def callback(future):
    result = future.result()
    bot.send_photo(result[1], result[0])
    user_states[result[1]] = "done"
    

def restore_image(file_url, chat_id):
    
    try:
        # code to restore image
        restored_image = restore.restore(file_url)
    except Exception as e:
        bot.send_message(chat_id, "Error occurred while processing image. Please try later.")
        return None
    return (restored_image, chat_id)

        
def get_file_path(file_id):
    url = "https://api.telegram.org/bot5836636187:AAGADUyLUl7NxeSCImS3mpN6_I7dFm338V4/getFile"
    data = {"file_id": file_id}
    response = requests.post(url, json=data)
    file_info = json.loads(response.text)
    file_path = file_info["result"]["file_path"]
    return file_path
        

bot.infinity_polling()





