# 🤖 Telegram Gym Bot

Bot Telegram per tracciare i tuoi allenamenti in palestra in modo semplice e automatico!

---

## 📦 Contenuto del progetto

- `bot.py`: entrypoint principale del bot
- `handlers/`: gestisce i comandi `/caricascheda`, `/allenati`, `/storico`
- `services/db.py`: gestisce salvataggi e caricamenti nel database SQLite
- `gymbot.db`: (verrà creato automaticamente) database locale
- `requirements.txt`: librerie richieste (puoi generarlo con `pip freeze`)

---

## 🚀 Come farlo funzionare

### 1. Clona o estrai il progetto

Se hai lo ZIP:

```bash
unzip telegram_gym_bot.zip
cd telegram_gym_bot
```

---

### 2. Crea un bot su Telegram

1. Vai su [@BotFather](https://t.me/BotFather)
2. Scrivi `/newbot`
3. Dai un nome e un username
4. Copia il token che ti fornisce

---

### 3. Installa le dipendenze

Si consiglia Python 3.10+

```bash
pip install python-telegram-bot
```

---

### 4. Inserisci il token nel `bot.py`

Sostituisci `"FAKE_TELEGRAM_TOKEN"` con il tuo token reale nella riga:

```python
app = ApplicationBuilder().token("IL_TUO_TOKEN").build()
```

---

### 5. Avvia il bot

```bash
python bot.py
```

---

## 📋 Comandi disponibili

| Comando          | Funzione |
|------------------|---------|
| `/caricascheda`  | Carica la scheda palestra (testo o reply) |
| `/allenati`      | Ti guida serie per serie, salvataggio automatico |
| `/storico`       | Mostra lo storico di un esercizio |

---

## 💾 I dati vengono salvati in

- `gymbot.db`: database SQLite locale
  - Tabella `schede`
  - Tabella `sessioni`

---

## 🔜 Prossimi sviluppi

- OCR: inserimento da foto scheda
- Grafici PNG con andamento carico/ripetizioni
- Notifiche automatiche e reminder

---

Creato con 💪 da ChatGPT per la tua forma fisica.
