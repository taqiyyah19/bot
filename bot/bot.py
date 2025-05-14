import pandas as pd
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')  

if not TOKEN:
    print("Bot token tidak ditemukan! Pastikan .env sudah benar.")
    exit()

try:
    data = pd.read_csv('D:/bot/dummy bot tele - Sheet1.csv')
except FileNotFoundError:
    print("File CSV tidak ditemukan! Pastikan path file benar.")
    exit()

def cari_mahasiswa(nim):
    hasil = data[data['NIM'].astype(str) == str(nim)]
    if not hasil.empty:
        row = hasil.iloc[0]
        return f"NAMA: {row['NAMA']}\nJURUSAN: {row['JURUSAN']}"
    else:
        return "NIM tidak ditemukan."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Masukkan NIM untuk melihat data mahasiswa.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    nim_input = update.message.text.strip()
    response = cari_mahasiswa(nim_input)
    await update.message.reply_text(response)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot sedang berjalan...")
    app.run_polling()
