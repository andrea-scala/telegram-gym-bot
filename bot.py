from telegram.ext import ApplicationBuilder
from handlers.carica_scheda import carica_scheda_handler
from handlers.allenati import allenati_conv
from handlers.storico import storico_conv
from telegram.ext import CommandHandler
from telegram import Update
from telegram.ext import ContextTypes
from telegram import BotCommand
import os

app = ApplicationBuilder().token(os.getenv("BOT_TOKEN")).build()
app.bot.set_my_commands([
    BotCommand("start", "Avvia il bot"),
    BotCommand("caricascheda", "Carica la tua scheda di allenamento"),
    BotCommand("allenati", "Inizia un allenamento guidato"),
    BotCommand("storico", "Visualizza lo storico dei tuoi allenamenti")
])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Ciao! Sono il tuo bot palestra 💪. Usa /")

# Aggiunta al dispatcher
app.add_handler(CommandHandler("start", start))
app.add_handler(carica_scheda_handler)
app.add_handler(allenati_conv)
app.add_handler(storico_conv)

app.run_polling()
