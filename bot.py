import os
import json
import random
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters, ContextTypes
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Variabili d'ambiente
TOKEN = os.environ["BOT_TOKEN"]
OWNER_ID = int(os.environ["OWNER_ID"])

# Carica modello leggero IA
model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# File per memoria
MEMORY_FILE = "memory.json"

# Carica memoria esistente
if os.path.exists(MEMORY_FILE):
    with open(MEMORY_FILE, "r") as f:
        memory = json.load(f)
else:
    memory = {}

# Funzione generazione risposta IA
def generate_response(user_input):
    inputs = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors="pt")
    outputs = model.generate(inputs, max_length=150, pad_token_id=tokenizer.eos_token_id)
    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Funzione salva memoria
def save_memory():
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f)

# Comando /reset
async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != OWNER_ID:
        return
    memory.clear()
    save_memory()
    await update.message.reply_text("✅ Memoria cancellata!")

# Comando /riassunto
async def riassunto(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != OWNER_ID:
        return
    if not memory:
        await update.message.reply_text("📂 Nessuna memoria da riassumere.")
        return
    summary = "\n".join([f"{k}: {v}" for k, v in memory.items()])
    await update.message.reply_text(f"📝 Riassunto memoria:\n{summary}")

# Comando /studio
async def studio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != OWNER_ID:
        return
    await update.message.reply_text("📚 Scrivi il testo di studio e lo terrò a mente!")

# Funzione messaggi generici
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    if user_id != OWNER_ID:
        return
    
    text = update.message.text
    
    # Aggiorna memoria
    memory[text] = generate_response(text)
    save_memory()
    
    # Risposta IA
    response = memory[text]
    
    # Saluto personalizzato casuale
    greetings = ["🤖 Eccomi!", "💡 Ti ascolto!", "😎 Dimmi pure!"]
    await update.message.reply_text(f"{random.choice(greetings)} {response}")

# Main
def main():
    app = Application.builder().token(TOKEN).build()
    
    # Comandi
    app.add_handler(CommandHandler("reset", reset))
    app.add_handler(CommandHandler("riassunto", riassunto))
    app.add_handler(CommandHandler("studio", studio))
    
    # Messaggi generici
    app.add_handler(MessageHandler(filters.TEXT, handle_message))
    
    print("🤖 Bot avviato...")
    app.run_polling()

if __name__ == "__main__":
    main()
