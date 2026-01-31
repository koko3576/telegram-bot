import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# Carica variabili dal file .env
load_dotenv()

# Prendi le chiavi dal .env
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not TELEGRAM_TOKEN or not OPENAI_API_KEY:
    raise ValueError("Assicurati che TELEGRAM_TOKEN e OPENAI_API_KEY siano impostati nel file .env")

# Configura OpenAI
openai.api_key = OPENAI_API_KEY

# Funzione per i messaggi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": user_message}]
    )

    reply = response.choices[0].message.content
    await update.message.reply_text(reply)

# Comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono il tuo bot OpenAI. Mandami un messaggio e ti risponderò!")

# Funzione principale
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot in esecuzione...")
    app.run_polling()

if __name__ == "__main__":
    main()
