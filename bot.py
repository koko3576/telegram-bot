import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import openai

# -----------------------------
# LOGGING
# -----------------------------
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

# -----------------------------
# VARIABILI D'AMBIENTE
# -----------------------------
TOKEN = os.environ.get("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OWNER_ID = int(os.environ.get("OWNER_ID", 0))  # opzionale, 0 = nessun filtro

if not TOKEN or not OPENAI_API_KEY:
    raise ValueError("Assicurati che TELEGRAM_TOKEN e OPENAI_API_KEY siano impostati")

openai.api_key = OPENAI_API_KEY

# -----------------------------
# HANDLER COMANDI
# -----------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if OWNER_ID and update.effective_user.id != OWNER_ID:
        return  # ignora messaggi non autorizzati
    await update.message.reply_text("Ciao! Sono il tuo bot basato su OpenAI.")

# -----------------------------
# HANDLER MESSAGGI
# -----------------------------
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if OWNER_ID and update.effective_user.id != OWNER_ID:
        return  # ignora messaggi non autorizzati

    user_text = update.message.text

    # Chiamata a OpenAI ChatGPT
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_text}],
            temperature=0.7
        )
        answer = response.choices[0].message.content
    except Exception as e:
        logger.error(f"Errore OpenAI: {e}")
        answer = "Si è verificato un errore nella richiesta a OpenAI."

    await update.message.reply_text(answer)

# -----------------------------
# MAIN
# -----------------------------
def main():
    app = Application.builder().token(TOKEN).build()

    # Comandi
    app.add_handler(CommandHandler("start", start))

    # Messaggi
   app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

