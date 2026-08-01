import os
import telebot
from google import genai

# Ye code aapke secret keys ko safely read karega jab hum ise host karenge
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = genai.Client(api_key=GEMINI_API_KEY)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Main Gemini AI hoon. Aap mujhse kuch bhi pooch sakte hain!")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # Telegram me 'typing...' dikhane ke liye
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Gemini se answer mangna
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=message.text,
        )
        
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Sorry, mujhe kuch samajhne me error aa gayi!")

if __name__ == "__main__":
    print("Bot is awake and listening...")
    bot.infinity_polling(skip_pending=True)
  
