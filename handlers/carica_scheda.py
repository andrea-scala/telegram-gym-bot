from telegram.ext import CommandHandler
from services.db import salva_scheda

async def carica_scheda(update, context):
    if context.args:
        testo = " ".join(context.args)
    elif update.message.reply_to_message:
        testo = update.message.reply_to_message.text
    else:
        await update.message.reply_text("📎 Inviami la scheda (testo), oppure rispondi a un messaggio con /caricascheda.")
        return

    salva_scheda(update.effective_user.id, testo)
    await update.message.reply_text("✅ Scheda salvata con successo.")

carica_scheda_handler = CommandHandler("caricascheda", carica_scheda)
