from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import random
import os

# Prende variabili da Render
TOKEN = os.environ["8098876870:AAHLOOJ-SftED23Mnk0_MYLMh0iqcX5U0Aw"]
OWNER_ID = int(os.environ["7399537812"])

# Risposte base da assistente
responses = [
    "Ciao! Come posso aiutarti? 😊",
    "Dimmi pure!",
    "Interessante. Continua!",
    "Ok, ti ascolto 👂",
    "Capito! Vuoi un consiglio?",
    "Sono qui per te 💪"
]

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id

    # Risponde solo a te
    if user_id != OWNER_ID:
        return

    text = update.message.text

    reply = random.choice(responses)
    await update.message.reply_text(reply)

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    print("Bot avviato...")
    app.run_polling()

if __name__ == "__main__":
    main()
