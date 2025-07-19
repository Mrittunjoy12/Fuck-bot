import os
import json
import random
import smtplib
from email.mime.text import MIMEText
from telegram import Update, ForceReply
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

BOT_TOKEN = os.getenv("BOT_TOKEN")
SMTP_EMAIL = os.getenv("SMTP_EMAIL")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

DATABASE_FILE = "database.json"

def load_data():
    if not os.path.exists(DATABASE_FILE):
        return {}
    with open(DATABASE_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATABASE_FILE, "w") as f:
        json.dump(data, f)

def send_email(to_email, code):
    msg = MIMEText(f"Your verification code is: {code}")
    msg['Subject'] = "Verification Code"
    msg['From'] = SMTP_EMAIL
    msg['To'] = to_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(SMTP_EMAIL, SMTP_PASSWORD)
    server.send_message(msg)
    server.quit()

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Welcome! Please register with /register your_email@example.com")

def register(update: Update, context: CallbackContext):
    data = load_data()
    chat_id = str(update.message.chat_id)

    if len(context.args) != 1:
        update.message.reply_text("Usage: /register your_email@example.com")
        return

    email = context.args[0]
    code = str(random.randint(100000, 999999))

    data[chat_id] = {
        "email": email,
        "verified": False,
        "code": code
    }
    save_data(data)
    send_email(email, code)
    update.message.reply_text(f"Verification code sent to {email}. Please verify using /verify your_code")

def verify(update: Update, context: CallbackContext):
    data = load_data()
    chat_id = str(update.message.chat_id)

    if chat_id not in data:
        update.message.reply_text("You need to register first using /register")
        return

    if len(context.args) != 1:
        update.message.reply_text("Usage: /verify your_code")
        return

    code = context.args[0]
    if data[chat_id]["code"] == code:
        data[chat_id]["verified"] = True
        save_data(data)
        update.message.reply_text("Your email is verified! Thank you.")
    else:
        update.message.reply_text("Verification failed. Please check your code and try again.")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("register", register))
    dp.add_handler(CommandHandler("verify", verify))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
