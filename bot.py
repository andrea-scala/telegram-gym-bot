from telegram.ext import ApplicationBuilder
from handlers.carica_scheda import carica_scheda_handler
from handlers.allenati import allenati_conv
from handlers.storico import storico_conv

app = ApplicationBuilder().token("FAKE_TELEGRAM_TOKEN").build()

app.add_handler(carica_scheda_handler)
app.add_handler(allenati_conv)
app.add_handler(storico_conv)

app.run_polling()
