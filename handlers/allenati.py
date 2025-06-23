from telegram import ReplyKeyboardMarkup
from telegram.ext import ConversationHandler, MessageHandler, filters, CommandHandler
from services.db import carica_scheda, salva_sessione
from datetime import date

SCELTA_GIORNO, ESECUZIONE_ESERCIZIO = range(2)

async def allenati(update, context):
    scheda = carica_scheda(update.effective_user.id)
    if not scheda:
        await update.message.reply_text("⚠️ Nessuna scheda trovata. Usa /caricascheda prima.")
        return ConversationHandler.END

    giorni = list(scheda.keys())
    context.user_data["scheda"] = scheda
    context.user_data["giorni"] = giorni

    keyboard = [[g] for g in giorni]
    await update.message.reply_text("📆 Scegli il giorno di allenamento:", reply_markup=ReplyKeyboardMarkup(keyboard, one_time_keyboard=True))
    return SCELTA_GIORNO

async def scelta_giorno(update, context):
    giorno = update.message.text
    scheda = context.user_data["scheda"]

    if giorno not in scheda:
        await update.message.reply_text("❌ Giorno non valido.")
        return ConversationHandler.END

    context.user_data["giorno_corrente"] = giorno
    context.user_data["esercizi"] = scheda[giorno]
    context.user_data["index_esercizio"] = 0
    context.user_data["allenamento"] = []

    await manda_prossimo_esercizio(update, context)
    return ESECUZIONE_ESERCIZIO

async def manda_prossimo_esercizio(update, context):
    esercizi = context.user_data["esercizi"]
    idx = context.user_data["index_esercizio"]

    if idx >= len(esercizi):
        salva_sessione(update.effective_user.id, str(date.today()), context.user_data["giorno_corrente"], context.user_data["allenamento"])
        await update.message.reply_text("✅ Allenamento salvato con successo!")
        return ConversationHandler.END

    esercizio = esercizi[idx]
    context.user_data["esercizio_corrente"] = esercizio
    context.user_data["serie_corrente"] = []
    context.user_data["serie_index"] = 0

    serie = esercizio["serie_ripetizioni"] or "serie non definite"
    note = esercizio["note"] or "nessuna nota"
    await update.message.reply_text(f"🏋️ Esercizio {idx+1}: *{esercizio['titolo']}* Serie: {serie} Note: {note}", parse_mode='Markdown')
    await update.message.reply_text("👉 Serie 1: Quante ripetizioni? (o scrivi 'salta')")
    return ESECUZIONE_ESERCIZIO

async def esecuzione_esercizio(update, context):
    testo = update.message.text.strip().lower()

    if testo == "salta":
        context.user_data["serie_corrente"].append({"ripetizioni": 0, "carico": 0})
    else:
        try:
            ripetizioni = int(testo)
            context.user_data["rip_temp"] = ripetizioni
            await update.message.reply_text("📦 Quanto carico (kg)?")
            return ESECUZIONE_ESERCIZIO
        except ValueError:
            await update.message.reply_text("❌ Inserisci un numero valido di ripetizioni o 'salta'")
            return ESECUZIONE_ESERCIZIO
        return

    return await gestisci_carico(update, context, saltata=True)

async def gestisci_carico(update, context, saltata=False):
    if not saltata:
        try:
            carico = float(update.message.text.strip())
        except ValueError:
            await update.message.reply_text("❌ Inserisci un numero valido per il carico (kg)")
            return ESECUZIONE_ESERCIZIO

        ripetizioni = context.user_data.pop("rip_temp")
        context.user_data["serie_corrente"].append({
            "ripetizioni": ripetizioni,
            "carico": carico
        })

    serie_idx = context.user_data["serie_index"] + 1
    context.user_data["serie_index"] = serie_idx

    esercizio = context.user_data["esercizio_corrente"]
    serie_totali = extract_serie(esercizio["serie_ripetizioni"])

    if serie_idx < serie_totali:
        await update.message.reply_text(f"👉 Serie {serie_idx+1}: Quante ripetizioni? (o scrivi 'salta')")
        return ESECUZIONE_ESERCIZIO
    else:
        context.user_data["allenamento"].append({
            "esercizio": esercizio["titolo"],
            "serie": context.user_data["serie_corrente"]
        })
        context.user_data["index_esercizio"] += 1
        return await manda_prossimo_esercizio(update, context)

def extract_serie(serie_str):
    if not serie_str:
        return 4
    try:
        parts = serie_str.lower().split("x")
        return int(parts[0])
    except:
        return 4

allenati_conv = ConversationHandler(
    entry_points=[CommandHandler("allenati", allenati)],
    states={
        SCELTA_GIORNO: [MessageHandler(filters.TEXT & ~filters.COMMAND, scelta_giorno)],
        ESECUZIONE_ESERCIZIO: [MessageHandler(filters.TEXT & ~filters.COMMAND, esecuzione_esercizio)],
    },
    fallbacks=[],
)
