# CanvaBot

A Telegram bot for managing Canva design submissions. Users can either create a design via a Canva link or submit a PNG file, which is validated for specific dimensions (1280x904) before forwarding to the admin.

## Features
- `/start` command presents options to make a design or submit one.
- Inline buttons for user interaction.
- Accepts PNG files (as documents or photos) and checks dimensions.
- Forwards valid submissions to the admin's Telegram ID.
- Temporary download handling with cleanup.

## Setup
1. Clone the repository:
   ```
   git clone <repo-url>
   cd CanvaBot
   ```

2. Copy the environment file:
   ```
   cp .env.example .env
   ```
   Edit `.env` with your values:
   - `BOT_TOKEN`: Your Telegram bot token from BotFather.
   - `YOUR_TELEGRAM_ID`: Your Telegram user ID (admin).
   - `REQUIRED_WIDTH` and `REQUIRED_HEIGHT`: Dimensions for validation (default 1280x904).
   - `DOWNLOAD_DIR`: Directory for temporary files (default "downloads").
   - `CANVA_LINK`: Link to the Canva design template.

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Run the bot:
   ```
   python src/bot.py
   ```

## Project Structure
- `src/`: Source code directory.
  - `bot.py`: Main bot application.
- `downloads/`: Temporary directory for file downloads (ignored in git).
- `requirements.txt`: Python dependencies.
- `.env.example`: Template for environment variables.
- `.gitignore`: Ignores sensitive files, caches, and environments.
- `README.md`: This file.

## Dependencies
- python-telegram-bot: For Telegram API interaction.
- Pillow: For image processing.
- python-dotenv: For loading environment variables.

## Usage
- Start the bot with `/start` to see options.
- Use the "Make one" button to open Canva.
- Use "Submit one" to upload a PNG file.
- The bot will validate and forward if correct.

## Notes
- Ensure your bot has permissions to receive documents and photos.
- The bot runs in polling mode; for production, consider webhooks.
- Downloads are cleaned up after processing.
