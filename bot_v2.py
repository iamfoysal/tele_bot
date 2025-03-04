import os
import smtplib
import openai
import re
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext, ConversationHandler


load_dotenv()
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
BOT_NAME = os.getenv("BOT_NAME", "AI Chatbot")

ASK_EMAIL = 1 
client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY)

def send_email(receiver_email, username):
    try:
        subject = "Welcome to the AI Chatbot!"
        body = f"Hello {username},\n\nThank you for starting a chat with me! I'm here to assist you.\n\nBest Regards,\n{BOT_NAME}"

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
    user = update.message.chat
    username = user.username or user.full_name or f"User_{user.id}"
    
    if "history" not in context.user_data:
        context.user_data["history"] = []

    await update.message.reply_text(f"🤖 Hello {username}! Please enter your email to continue:")
    context.user_data["username"] = username
    return ASK_EMAIL


async def ask_email(update: Update, context: CallbackContext):
    user_email = update.message.text
    username = context.user_data.get("username", "User")

    if not re.match(r"[^@]+@[^@]+\.[^@]+", user_email):
        await update.message.reply_text("❌ Invalid email format. Please enter a valid email:")
        return ASK_EMAIL

    send_email(user_email, username)
    await update.message.reply_text("✅ Thank you! A welcome email has been sent. Now, ask me anything!")
    return ConversationHandler.END


async def get_ai_response(update: Update, context: CallbackContext):
    """
    Process user messages and generate AI responses
    Args:
        update (Update): Telegram update object containing message info
        context (CallbackContext): Context object for user data storage
    Returns:
        None: Handles message processing and response asynchronously
    """
    user_message = update.message.text
    user_id = update.message.chat_id
    
    username = update.message.from_user.username or "Anonymous"
    print(f"Message received from {username}: {user_message}")

    if "history" not in context.user_data:
        context.user_data["history"] = []

    chat_history = context.user_data["history"]
    chat_history.append({"role": "user", "content": user_message})
    chat_history = chat_history[-10:]

    await context.bot.send_chat_action(chat_id=user_id, action="typing")

    try:
        response = await client.chat.completions.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Format all responses with clear sections, bullet points, and code blocks when needed."}
            ] + chat_history
        )
        ai_reply = response.choices[0].message.content
    except Exception as e:
        ai_reply = f"❌ Error: {str(e)}"

    chat_history.append({"role": "assistant", "content": ai_reply})
    context.user_data["history"] = chat_history

    await update.message.reply_text(ai_reply, parse_mode="Markdown")




async def history(update: Update, context: CallbackContext):

    chat_history = context.user_data.get("history", [])
    
    if not chat_history:
        await update.message.reply_text("❌ No chat history found.")
        return

    last_messages = "\n".join(
        f"**{msg['role'].capitalize()}**:\n{msg['content']}" for msg in chat_history[-5:]
    )

    await update.message.reply_text(f"📝 **Your last messages:**\n\n{last_messages}", parse_mode="Markdown")


async def clear_history(update: Update, context: CallbackContext):
    context.user_data["history"] = []
    await update.message.reply_text("✅ Chat history cleared!")


def main():
    """
    Main function to initialize and run the Telegram bot.
    This function sets up the bot with necessary handlers for different commands and messages.
    It creates a conversation handler for the start command and email collection,
    adds handlers for AI responses, chat history, and history clearing commands.
    Finally, it starts the bot in polling mode.
    Handlers:
        - start: Initiates the conversation
        - ask_email: Handles email collection
        - get_ai_response: Processes general text messages
        - history: Shows chat history
        - clear_history: Clears chat history
    Returns:
        None
    """
    app = Application.builder().token(TELEGRAM_TOKEN).build()

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={ASK_EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_email)]},
        fallbacks=[]
    )

    app.add_handler(conv_handler)
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, get_ai_response))
    app.add_handler(CommandHandler("history", history))
    app.add_handler(CommandHandler("clear", clear_history))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
