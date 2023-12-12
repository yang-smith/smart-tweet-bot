import logging
import os
from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext, ConversationHandler

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)
load_dotenv()

# Define a few command handlers. These usually take the two arguments update and
# context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def ask_chatgpt(question: str) -> str:
    vectorstore = db_init()
    result = ""
    model = ChatOpenAI(model="gpt-3.5-turbo")
    prompt = ChatPromptTemplate.from_template(prompt_vector)
    chain = prompt | model | StrOutputParser()
    result_str = show_search(query=question, db=vectorstore)
    result = chain.invoke({"context": result_str, "question": question})
    return result


async def answer_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        "Please type the message you want to send to ChatGPT.",
        reply_markup=ForceReply(selective=True),
    )
    return ANSWER

async def handle_answer(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chatgpt_response = await ask_chatgpt(user_message)
    await update.message.reply_text(chatgpt_response)
    return ConversationHandler.END

COLLECT, ANSWER = range(2)

def main() -> None:
    """Start the bot."""
    # print(os.environ.get('OPENAI_API_KEY'))
    # print(os.environ.get('OPENAI_API_BASE'))
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    application = Application.builder().token(BOT_TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()