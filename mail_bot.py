import os
import smtplib
import openai
import re
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    CallbackContext, 
    ConversationHandler
    )


load_dotenv()


TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

ASK_EMAIL = 1
bot_name = os.getenv("BOT_NAME")
client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)




def send_email(receiver_email, username):
    try:
        subject = "Welcome to the AI Chatbot!"
        body = f"Hello {username},\n\nThank you for starting a chat with me! I'm here to assist you.\n\nBest Regards,\n{bot_name}"

        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, receiver_email, msg.as_string())
        server.quit()
        print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error sending email: {str(e)}")


async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("🤖 Hello! Please enter your email to continue:")
    return ASK_EMAIL


async def ask_email(update: Update, context: CallbackContext):
    user_email = update.message.text
    print("User email:", user_email)
    print("Username:", update.message.chat.username)
    username = update.message.chat.username or "User"

   
    if not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
        await update.message.reply_text("Invalid email format. Please enter a valid email:")
        return ASK_EMAIL


    send_email(user_email, username)

    await update.message.reply_text("Thank you! Now, ask me anything!")
    return ConversationHandler.END


async def get_ai_response(text):
    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo",  
            messages=[{"role": "user", "content": text}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    print("User message:", user_message)
    ai_response = await get_ai_response(user_message)
    print("AI response:", ai_response)
    await update.message.reply_text(ai_response)

# Main function to run the bot
def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)]},
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
