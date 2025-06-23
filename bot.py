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
async def post_startup(application):
    await application.bot.set_my_commands([
        BotCommand("start", "Avvia il bot"),
        BotCommand("caricascheda", "Carica la scheda"),
        BotCommand("allenati", "Inizia un allenamento"),
        BotCommand("storico", "Confronta allenamenti"),
    ])

app.post_init = post_startup

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Ciao! Sono il tuo bot palestra 💪\n\n"
        "Ecco i comandi che puoi usare:\n"
        "📋 /caricascheda – Carica la tua scheda di allenamento (anche via foto)\n"
        "🏋️ /allenati – Inizia l’allenamento guidato\n"
        "📈 /storico – Confronta le tue performance passate\n"
    )

# Aggiunta al dispatcher
app.add_handler(CommandHandler("start", start))
app.add_handler(carica_scheda_handler)
app.add_handler(allenati_conv)
app.add_handler(storico_conv)

app.run_polling()
