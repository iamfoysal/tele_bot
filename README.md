## Overview
This is a Telegram bot that interacts with users, collects their email addresses, sends a welcome email, and responds to their messages using OpenAI's GPT-4 model. It also maintains a chat history and allows users to clear or view their chat history.

LIVE: [HappyCoder](https://t.me/dev_ai_agent_bot)

### User Commands
- `/start`: Starts the conversation and prompts the user to enter their email.
- input your email address: Validates the email format and sends a welcome email. example: `example@gmail.com`
- `/help`: Displays the help message.
- `/clear`: Clears the chat history.
- `/history`: Displays the chat history.
- Send any message: The bot will respond with an AI-generated text based on the user's input.


## Functions
Note" Here bot_v2 is the main file of the bot now its updated with the new features and functions.
### `send_email(receiver_email, username)`
Sends a welcome email to the specified receiver.

**Parameters:**
- `receiver_email` (str): The email address of the receiver.
- `username` (str): The username of the receiver.

**Exceptions:**
- Prints an error message if the email could not be sent.

### `start(update: Update, context: CallbackContext)`
Handles the `/start` command. Prompts the user to enter their email and initializes the chat history.

**Parameters:**
- `update` (Update): The update object that contains the message data.
- `context` (CallbackContext): The context object that contains the bot data.

**Returns:**
- `ASK_EMAIL`: The next state in the conversation handler.

### `ask_email(update: Update, context: CallbackContext)`
Handles the user's email input. Validates the email format and sends a welcome email.

**Parameters:**
- `update` (Update): The update object that contains the message data.
- `context` (CallbackContext): The context object that contains the bot data.

**Returns:**
- `ASK_EMAIL`: If the email format is invalid.
- `ConversationHandler.END`: If the email is valid and the email is sent.

### `get_ai_response(update: Update, context: CallbackContext)`
Handles incoming messages from the user and responds with AI-generated text. Maintains a chat history and formats the AI response.

**Parameters:**
- `update` (Update): The update object that contains the message data.
- `context` (CallbackContext): The context object that contains the bot data.

### `history(update: Update, context: CallbackContext)`
Displays the last few messages from the chat history.

**Parameters:**
- `update` (Update): The update object that contains the message data.
- `context` (CallbackContext): The context object that contains the bot data.

### `clear_history(update: Update, context: CallbackContext)`
Clears the chat history.

**Parameters:**
- `update` (Update): The update object that contains the message data.
- `context` (CallbackContext): The context object that contains the bot data.

### `main()`
Main function to run the bot. Sets up the application and handlers, and starts polling for updates.

**Execution:**
- Prints "🤖 Bot is running..." to the console.
- Runs the bot using `app.run_polling()`.

## Environment Variables
The following environment variables need to be set in the `.env` file for the bot to function correctly:

- `TELEGRAM_TOKEN`: The token for your Telegram bot.
- `OPENAI_API_KEY`: The API key for OpenAI.
- `EMAIL_SENDER`: The email address used to send emails.
- `EMAIL_PASSWORD`: The password for the email sender account.
- `BOT_NAME`: The name of the bot (default is "AI Chatbot").

### Example `.env` file
```env
TELEGRAM_TOKEN=your_telegram_token
OPENAI_API_KEY=your_openai_api_key
EMAIL_SENDER=your_email@example.com
EMAIL_PASSWORD=your_email_password
BOT_NAME=YourBotName
```


## Setup Telegram Bot
First, create a bot using BotFather on Telegram:

- Start a chat with BotFather (/start).
- Use the /newbot command to create a bot.
- Give your bot a name and username.
- BotFather will provide you with an API Token—save it for later.