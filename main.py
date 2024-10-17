import telebot
from telebot import types
import requests

#Conexion con nuestro bot
TOKEN = ''
API_KEY = ''

bot = telebot.TeleBot(TOKEN)
BASE_URL = 'https://api.openweathermap.org/data/2.5/weather?'

#Creacion de comandos simples 
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, (
        '¡Hola! Soy el bot del grupo 8 de la cátedra de Soporte a la Gestión de Datos con Programación Visual.\n'
        'Fui creado por Andrea Matteucci, Agostina Chiara y Laura Tulian.\n'
        '¡Estoy aquí para ayudarte! Usa el comando /help para conocer mis funciones.'
    ))

@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, (
        '¡Aquí tienes una lista de comandos que puedes usar para interactuar conmigo:\n'
        '/start - Inicia una conversación y te da la bienvenida.\n'
        '/help - Muestra esta lista de comandos disponibles.\n'
        '/foto - Te envía una imagen divertida.\n'
        '/python - Pregunta si te gusta python y te da opciones para responder.\n'
        '/clima + nombre_ciudad - Te proporciona la temperatura actual y la descripción del clima en la ciudad especificada.\n'
        '\n¡Intenta usar uno de estos comandos y diviértete!'
    ))


@bot.message_handler(commands=['python'])
def send_options(message):
    markup = types.InlineKeyboardMarkup(row_width=2)

    #Creando botones
    btn_si = types.InlineKeyboardButton('Si', callback_data='python_si')
    btn_no = types.InlineKeyboardButton('No', callback_data='python_no')

    #Agrega los botones al markup
    markup.add(btn_si, btn_no)

    #Enviar mensaje con los botones
    bot.send_message(message.chat.id, "¿Te gusta programar en python?", reply_markup=markup)

@bot.callback_query_handler(func=lambda call:True)
def callbacj_query(call):
    if call.data == 'python_si':
        bot.answer_callback_query(call.id, '¡A mi tambien!')
    elif call.data == 'python_no':
         bot.answer_callback_query(call.id, '¡Vaya! Entonces, ¿qué haces cursando esta materia?')

@bot.message_handler(commands=['foto'])
def send_image(message):
    img_url = 'https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png'
    bot.send_photo(chat_id=message.chat.id, photo=img_url, caption='¡Mira! Aquí tienes al rey de los lenguajes de programación. 🐍')

def get_weather(city_name):
    complete_url= BASE_URL + "q=" + city_name + "&appid=" + API_KEY
    response = requests.get(complete_url)
    data = response.json()

    if data["cod"] != '404':
        main_data = data["main"]
        weather_data = data["weather"][0]
        temperature = main_data["temp"] -273.15
        description = weather_data["description"]
        return f"Temperatura: {temperature:.2f} C° \nDescripcion: {description.capitalize()}"
    else:
        return 'Ciudad no encontrada'

@bot.message_handler(commands=["clima"])
def send_weather(message):
    city_name = " ".join(message.text.split()[1:])
    if city_name:
        weather_info = get_weather(city_name)
        bot.reply_to(message, weather_info)
    else:
        bot.reply_to(message, "Por favor, proporciona nombre de la ciudad. Ejemplo: /clima Madrid")
    
if __name__ == "__main__":
    bot.polling(none_stop=True)
