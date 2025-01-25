import logging
from dotenv import load_dotenv
import os
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.constants import ParseMode  # Updated import for ParseMode
from telegram.ext import (
    ApplicationBuilder,  # Replaces Updater
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,  # New context type
    filters  # Replaces Filters
)

# Load environment variables
load_dotenv()

# Set up logging
logger = logging.getLogger(__name__)

# Store bot screaming status
screaming = False

# Pre-assign menu text
FIRST_MENU = "<b>Menu 1</b>\n\nA beautiful menu with a shiny inline button."
SECOND_MENU = "<b>Menu 2</b>\n\nA better menu with even more shiny inline buttons."

# Pre-assign button text
NEXT_BUTTON = "Next"
BACK_BUTTON = "Back"
TUTORIAL_BUTTON = "Tutorial"

# Build keyboards
FIRST_MENU_MARKUP = InlineKeyboardMarkup([[
    InlineKeyboardButton(NEXT_BUTTON, callback_data=NEXT_BUTTON)
]])
SECOND_MENU_MARKUP = InlineKeyboardMarkup([
    [InlineKeyboardButton(BACK_BUTTON, callback_data=BACK_BUTTON)],
    [InlineKeyboardButton(TUTORIAL_BUTTON, url="https://core.telegram.org/bots/api")]
])


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function would be added to the dispatcher as a handler for messages coming from the Bot API
    """
    global screaming

    # Print to console
    print(f'{update.message.from_user.first_name} wrote {update.message.text}')

    if screaming and update.message.text:
        await context.bot.send_message(
            chat_id=update.message.chat_id,
            text=update.message.text.upper(),
            entities=update.message.entities  # Preserve markdown entities
        )
    else:
        # This is equivalent to forwarding, without the sender's name
        await update.message.copy(chat_id=update.message.chat_id)


async def scream(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function handles the /scream command
    """
    global screaming
    screaming = True
    await update.message.reply_text("Screaming mode activated!")


async def whisper(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This function handles /whisper command
    """
    global screaming
    screaming = False
    await update.message.reply_text("Whispering mode activated!")


async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This handler sends a menu with the inline buttons we pre-assigned above
    """
    await context.bot.send_message(
        chat_id=update.message.from_user.id,
        text=FIRST_MENU,
        parse_mode=ParseMode.HTML,
        reply_markup=FIRST_MENU_MARKUP
    )


async def button_tap(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    This handler processes the inline buttons on the menu
    """
    data = update.callback_query.data
    text = ''
    markup = None

    if data == NEXT_BUTTON:
        text = SECOND_MENU
        markup = SECOND_MENU_MARKUP
    elif data == BACK_BUTTON:
        text = FIRST_MENU
        markup = FIRST_MENU_MARKUP

    # Close the query to end the client-side loading animation
    await update.callback_query.answer()

    # Update message content with corresponding menu section
    await update.callback_query.message.edit_text(
        text=text,
        parse_mode=ParseMode.HTML,
        reply_markup=markup
    )


def main() -> None:
    BOT_TOKEN = os.environ.get('GPT_BOT_TOKEN')

    # Build the application
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    # Register command handlers
    application.add_handler(CommandHandler("scream", scream))
    application.add_handler(CommandHandler("whisper", whisper))
    application.add_handler(CommandHandler("menu", menu))

    # Register handler for inline buttons
    application.add_handler(CallbackQueryHandler(button_tap))

    # Echo any message that is not a command
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the bot
    application.run_polling()


if __name__ == '__main__':
    main()
