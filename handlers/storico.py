from telegram.ext import CommandHandler, MessageHandler, filters, ConversationHandler
from services.db import carica_storico

SCELTA_ESERCIZIO = 0

async def storico(update, context):
    await update.message.reply_text("📌 Inserisci il nome dell’esercizio di cui vuoi vedere lo storico (esatto o parte):")
    return SCELTA_ESERCIZIO

async def mostra_storico(update, context):
    esercizio = update.message.text.strip().lower()
    user_id = update.effective_user.id

    records = carica_storico(user_id, esercizio)
    if not records:
        await update.message.reply_text("⚠️ Nessun dato trovato per questo esercizio.")
        return ConversationHandler.END

    storico_by_data = {}
    for r in records:
        data, serie_index, ripetizioni, carico = r
        storico_by_data.setdefault(data, []).append((serie_index, ripetizioni, carico))

    msg = f"📈 Storico per *{esercizio.title()}*:
"
    for data in sorted(storico_by_data.keys()):
        msg += f"
📅 {data}:
"
        for serie in sorted(storico_by_data[data]):
            msg += f"  - Serie {serie[0]}: {serie[1]} rip. x {serie[2]} kg
"
    await update.message.reply_text(msg, parse_mode="Markdown")

    return ConversationHandler.END

storico_conv = ConversationHandler(
    entry_points=[CommandHandler("storico", storico)],
    states={SCELTA_ESERCIZIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, mostra_storico)]},
    fallbacks=[],
)
