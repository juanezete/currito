import telebot

TOKEN = ('6625376467:AAG8f85d1Hg1PLqC132f1buDFkHxHTlP2xg')
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message,"Buenas, soy Currito Bot \U0001F426 para interactuar conmigo utiliza un bot de la lista!:\n /teclado \n /mando \n /aleatorio \n /voz \n /camara")
    
@bot.message_handler(commands=['teclado'])
def send_welcome(message):
    bot.reply_to(message,"Modo TECLADO activado!")
    
@bot.message_handler(commands=['aleatorio'])
def send_welcome(message):
    bot.reply_to(message,"Modo ALEATORIO activado!")
    
@bot.message_handler(commands=['voz'])
def send_welcome(message):
    bot.reply_to(message,"Modo VOZ activado!")
    
@bot.message_handler(commands=['camara'])
def send_welcome(message):
    bot.reply_to(message,"Modo CÁMARA activado!")

@bot.message_handler(commands=['mando'])
def send_welcome(message):
    bot.reply_to(message,"Modo MANDO activado!")
    
bot.polling(none_stop=True)
    