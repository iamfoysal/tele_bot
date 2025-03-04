import os
import openai
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application, 
    CommandHandler, 
    MessageHandler, 
    filters, 
    CallbackContext
    )

load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)


async def get_ai_response(text):
    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo", 
            messages=[{"role": "user", "content": text}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("🤖 Hello! I'm an AI chatbot. Ask me anything!")

async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    print(f"User: {user_message}")

    ai_response = await get_ai_response(user_message)
    print(f"AI: {ai_response}")
    await update.message.reply_text(ai_response)


def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
