import os
import json
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Legge variabili d'ambiente
TOKEN = os.environ["BOT_TOKEN"]
OWNER_ID = int(os.environ["OWNER_ID"])

# Carica memoria
MEMORY_FILE = "memory.json"
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {}

# Modello leggero per free instance
MODEL_NAME = "microsoft/DialoGPT-small"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForCausalLM.from_pretrained(MODEL_NAME)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    text = update.message.text

    # Solo risponde all'owner
    if int(user_id) != OWNER_ID:
        return

    # Recupera la memoria dell'utente
    history = memory.get(user_id, [])
    history.append(text)

    # Genera risposta
    input_ids = tokenizer.encode(text + tokenizer.eos_token, return_tensors="pt")
    chat_history_ids = model.generate(input_ids, max_length=100, pad_token_id=tokenizer.eos_token_id)
    reply = tokenizer.decode(chat_history_ids[:, input_ids.shape[-1]:][0], skip_special_tokens=True)

    # Salva risposta in memoria
    history.append(reply)
    memory[user_id] = history
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

    await update.message.reply_text(reply)

# Comandi extra
async def reset_memory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.message.from_user.id)
    if int(user_id) == OWNER_ID:
        memory[user_id] = []
        with open(MEMORY_FILE, "w") as f:
            json.dump(memory, f)
        await update.message.reply_text("✅ Memoria resettata!")

# Setup bot
app = Application.builder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.add_handler(CommandHandler("reset", reset_memory))

print("🤖 Bot avviato...")
app.run_polling()
