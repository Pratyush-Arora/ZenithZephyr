import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}! How can I assist you today?",
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Sure, I'm here to help!")

async def handle_greetings(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_message = update.message.text.lower()
    if any(keyword in user_message for keyword in ["hi", "hello", "hey"]):
        await update.message.reply_text("Hello! How can I help you?")
    elif "how are you" in user_message:
        await update.message.reply_text("I'm just a bot, but thanks for asking!")

async def handle_syllabus(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Replace this with the path to your syllabus image or any image you want to send
    syllabus_image_path = "S1.png"
    try:
        with open(syllabus_image_path, "rb") as image:
            await update.message.reply_photo(photo=image)
    except Exception as e:
        logger.error(f"Error sending syllabus image: {e}")
        await update.message.reply_text("Sorry, there was an error. Please try again later.")

async def handle_deep_learning(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    deep_learning_image_path = "deep_learn_syll.png"
    try:
        with open(deep_learning_image_path, "rb") as image:
            await update.message.reply_photo(photo=image)
    except Exception as e:
        logger.error(f"Error sending deep learning image: {e}")
        await update.message.reply_text("Sorry, there was an error. Please try again later.")


async def handle_management(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # Replace these with the paths to your management images or any images you want to send
    management_image_path_1 = "mang1.png"
    management_image_path_2 = "mang2.png"

    try:
        with open(management_image_path_1, "rb") as image_1, open(management_image_path_2, "rb") as image_2:
            await update.message.reply_photo(photo=image_1)
            await update.message.reply_photo(photo=image_2)
    except Exception as e:
        logger.error(f"Error sending management images: {e}")
        await update.message.reply_text("Sorry, there was an error. Please try again later.")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(update.message.text)

def main() -> None:
    application = Application.builder().token("YOUR_BOT TOKEN").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("syllabus", handle_syllabus))
    #application.add_handler(MessageHandler(filters.TEXT & filters.COMMAND, handle_deep_learning, pass_args=True))
    application.add_handler(CommandHandler("management", handle_management))
    application.add_handler(CommandHandler("Dl", handle_deep_learning))
    application.add_handler(CommandHandler("dl", handle_deep_learning))
    application.add_handler(CommandHandler("deeplearning", handle_deep_learning))


    # Handle greetings and simple queries
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_greetings))

    # Fallback to echo for any other messages
    application.add_handler(MessageHandler(filters.TEXT, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
