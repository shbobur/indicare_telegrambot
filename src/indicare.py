import os
import telebot
from dotenv import load_dotenv
import logging
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

BOT_TOKEN = os.environ.get('INDICARE_BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

ORDER_LINK = "https://t.me/indicare_uz"
TELEGRAM_LINK = "t.me/indicareuz"
INSTAGRAM_LINK = "https://www.instagram.com/indicare.uz/"

# Load post templates
with open("templates.json", "r", encoding="utf-8") as file:
    templates_data = json.load(file)
    templates = templates_data["templates"]

# Define a list of allowed user IDs
allowed_user_ids = {
    '+821025321434', 'Dina', 'Dinora', # Dinora
    'shbobur2', 'Bobur',               # Bobur
    '+998971451106', 'Indira',         # Indira
    'indicare_uz'                      # Indicare account
}


# Define a function to check if the user is allowed
def is_allowed(user_id):
    return user_id in allowed_user_ids


def make_post_from_template(template_id, message):
    # Adjust for 0-based indexing
    template_index = template_id - 1
    if template_index < 0 or template_index >= len(templates):
        raise ValueError(f"Template ID {template_id} is out of range")
        
    template = templates[template_index]
    header = template["header"]
    FOOTER = "\n\n✨ [Buyurtma qiling]({order_link})! ✨\n\n📲 [Telegram]({telegram_link}) | 📷 [Instagram]({instagram_link})"
    # footer = template["footer"].format(
    footer = FOOTER.format(
        order_link=ORDER_LINK,
        telegram_link=TELEGRAM_LINK,
        instagram_link=INSTAGRAM_LINK
    )
    return f"{header}{message}{footer}"


@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    logger.info(f"Received /start or /hello command from {message.from_user.username}")
    if is_allowed(message.from_user.username):
        bot.reply_to(message, f'Hey {message.from_user.first_name}, text me anything and I make it a telegram post, so that you can forward to the group.')
    else:
        bot.reply_to(message, "You are not authorized to use this bot.")


@bot.message_handler(func=lambda msg: True)
def echo_all(message):
    logger.info(f"Received message: {message.text} from {message.from_user}")

    if is_allowed(message.from_user.username) or is_allowed(message.from_user.first_name):
        print('Sending back to ', message.from_user)
        # Use template IDs from 1 to len(templates)
        for i in range(1, len(templates) + 1):
            try:
                formatted_message = make_post_from_template(i, message.text)
                bot.send_message(
                    chat_id=message.chat.id,
                    text=formatted_message,
                    parse_mode='Markdown'
                )
            except Exception as e:
                logger.error(f"Error processing template {i}: {str(e)}")
    else:
        print('rejecting ', message)
        bot.reply_to(message, "You are not authorized to use this bot.")


bot.infinity_polling()
