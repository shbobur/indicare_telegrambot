## Running the Telegram Bot

### Prerequisites
- Python 3.x
- Required packages: `python-telegram-bot`, `python-dotenv`

### Setup
1. Install the required packages:
```bash
pip install python-telebot python-dotenv
```

2. Create a `.env` file in the root directory with your bot token:
```
INDICARE_BOT_TOKEN=your_bot_token_here
```

3. Configure allowed users by updating the `allowed_user_ids` list in `src/indicare.py` with the appropriate Telegram usernames or phone numbers.

### Running the Bot
1. Navigate to the project directory
2. Run the bot:
```bash
python src/indicare.py
```

The bot will start and respond to messages from authorized users. It will:
- Respond to `/start` or `/hello` commands with a welcome message
- Format any text messages with Indicare's contact information
- Only respond to authorized users listed in the `allowed_user_ids`

### Features
- Message formatting for Indicare's promotional content
- User authorization system
- Logging system for tracking bot usage
- Markdown support for formatted messages
