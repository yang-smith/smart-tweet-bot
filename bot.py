import logging
import os
import ai
from dotenv import load_dotenv
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext, ConversationHandler
from schedule import content_list, reset_time, schedule_daily_action


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





async def enhance_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        "Please type the message you want to send to ChatGPT.",
        reply_markup=ForceReply(selective=True),
    )
    return ENHANCE

async def handle_enhance(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    chatgpt_response = await ai.ai_enhance(user_message)
    await update.message.reply_text(chatgpt_response)
    return ConversationHandler.END

async def add_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        "Please type the message you want to add to post list.",
        reply_markup=ForceReply(selective=True),
    )
    return ADD

async def handle_add(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    content_list.append(user_message)
    await update.message.reply_text("add into list.")
    return ConversationHandler.END

async def settime_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        "Set post time. use something like '12:20' ",
        reply_markup=ForceReply(selective=True),
    )
    return SETTIME

async def handle_settime(update: Update, context: CallbackContext) -> None:
    user_message = update.message.text
    reset_time(user_message)
    await update.message.reply_text("set post time success.")
    return ConversationHandler.END

ENHANCE, ADD, SETTIME = range(3)

def main() -> None:
    """Start the bot."""
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('enhance', enhance_command),
            CommandHandler('add2list', add_command),
            CommandHandler('settime', settime_command),
        ],
        states={
            ENHANCE: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_enhance)],
            ADD: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_add)],
            SETTIME: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_settime)],
        },
        fallbacks=[],
    )
    application.add_handler(conv_handler)
    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()