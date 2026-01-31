import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# -----------------------------
# Configurazione logging
# -----------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# -----------------------------
# Variabili ambiente
# -----------------------------
TOKEN = os.environ.get("TELEGRAM_TOKEN")        # Token del bot Telegram
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")  # API Key OpenAI
OWNER_ID = int(os.environ.get("OWNER_ID", 0))  # ID Telegram autorizzato (0 = nessun controllo)

openai.api_key = OPENAI_API_KEY

# -----------------------------
# Funzioni del bot
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if OWNER_ID and update.effective_user.id != OWNER_ID:
        return  # ignora utenti non autorizzati
    await update.message.reply_text("Ciao! Sono pronto a rispondere ai tuoi messaggi.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Controllo OWNER_ID
    if OWNER_ID and update.effective_user.id != OWNER_ID:
        return  # ignora messaggi non autorizzati

    user_message = update.message.text
    try:
        # Chiamata OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        reply = f"Errore: {e}"

    await update.message.reply_text(reply)

# -----------------------------
# Funzione main
# -----------------------------
def main():
    app = Application.builder().token(TOKEN).build()

    # Comandi
    app.add_handler(CommandHandler("start", start))

    # Messaggi di testo
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    # Avvio del bot
    app.run_polling()

if __name__ == "__main__":
    main()
