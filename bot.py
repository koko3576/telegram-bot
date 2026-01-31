import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import openai

# -----------------------------
# Logging
# -----------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# -----------------------------
# Variabili ambiente
# -----------------------------
TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OWNER_ID = int(os.environ.get("OWNER_ID", 0))  # ID Telegram autorizzato (0 = nessun controllo)

if not TOKEN or not OPENAI_API_KEY:
    raise ValueError("Assicurati che TELEGRAM_TOKEN e OPENAI_API_KEY siano impostati")

openai.api_key = OPENAI_API_KEY

# -----------------------------
# Comandi
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if OWNER_ID and update.effective_user.id != OWNER_ID:
        return
    await update.message.reply_text("Ciao! Scrivi qualcosa e ti risponderò usando OpenAI.")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if OWNER_ID and update.effective_user.id != OWNER_ID:
        return

    user_message = update.message.text
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_message}]
        )
        reply = response['choices'][0]['message']['content']
    except Exception as e:
        reply = f"Errore: {e}"

    await update.message.reply_text(reply)

# -----------------------------
# Main
# -----------------------------
def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

    app.run_polling()  # NO Updater, solo polling

if __name__ == "__main__":
    main()
