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

### [Deploy](https://blog.devops.dev/free-hosting-for-your-telegram-bot-its-easier-than-you-think-66a5e5c000bb) using Cloudflare webhook/worker:

1. **Deploy to Cloudflare**:
   - Go to [dash.cloudflare.com](https://dash.cloudflare.com) and log in/sign up
   - Navigate to Workers & Pages in the left menu
   - For first-time deployment:
     - Click "Create application" -> "Create Worker"
     - Give it a name and click "Deploy"
   - For existing deployment:
     - Click the worker name
     - Press "Edit code" to update it

2. **Set Environment Variables**:
   - Click "Settings" -> "Environment Variables"
   - Add variable named `API_KEY` with your Telegram bot token as the value
   - Save and deploy

3. **Check Current Webhook Status**:
   ```bash
   curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getWebhookInfo"
   ```
   Response will look like:
   ```json
   {"ok":true,"result":{"url":"","has_custom_certificate":false,"pending_update_count":1}}
   ```
   If the `"url":""` is empty, it means no webhook is set up.

4. **Set Up Webhook**:
   ```bash
   curl "https://api.telegram.org/bot<YOUR_BOT_TOKEN>/setWebhook?url=<YOUR_WORKER_URL>"
   ```
   Replace:
   - `<YOUR_BOT_TOKEN>` with your Telegram bot token
   - `<YOUR_WORKER_URL>` with your Cloudflare Worker URL (e.g., `https://your-worker.your-subdomain.workers.dev`)

5. **Verify Webhook Setup**:
   - Run the getWebhookInfo command again
   - The response should now show your Worker URL:
   ```json
   {"ok":true,"result":{"url":"https://your-worker.your-subdomain.workers.dev","has_custom_certificate":false}}
   ```

**Note**: When the webhook is properly set up, you don't need to run the Python bot (`src/indicare.py`). The bot will work through the Cloudflare Worker instead.

### Features
- Message formatting for Indicare's promotional content
- User authorization system
- Logging system for tracking bot usage
- Markdown support for formatted messages
