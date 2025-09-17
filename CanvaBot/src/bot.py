import logging
import os
from dotenv import load_dotenv
from PIL import Image
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler,
    ContextTypes, filters
)

load_dotenv()

# --- CONFIG ---
BOT_TOKEN = os.getenv('BOT_TOKEN')
YOUR_TELEGRAM_ID = int(os.getenv('YOUR_TELEGRAM_ID'))
REQUIRED_WIDTH = int(os.getenv('REQUIRED_WIDTH', '1280'))
REQUIRED_HEIGHT = int(os.getenv('REQUIRED_HEIGHT', '904'))
DOWNLOAD_DIR = os.getenv('DOWNLOAD_DIR', 'downloads')
CANVA_LINK = os.getenv('CANVA_LINK', 'https://www.canva.com/design/DAGxaXH4eV4/Cax_AqQe9bYZSRaUugLyvA/edit?utm_content=DAGxaXH4eV4&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton')

# --- LOGGING ---
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# --- COMMAND HANDLERS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("🖌️ Make one", url=CANVA_LINK),
            InlineKeyboardButton("📤 Submit one", callback_data="submit")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Welcome! Do you need to make a design or submit one?",
        reply_markup=reply_markup
    )

# --- BUTTON HANDLER ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "submit":
        await query.edit_message_text(
            text=f"Great! Please send me your PNG file with dimensions {REQUIRED_WIDTH}x{REQUIRED_HEIGHT}."
        )

# --- FILE HANDLER ---
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = None
    if update.message.document:
        if update.message.document.file_name.lower().endswith(".png"):
            file = await update.message.document.get_file()
        else:
            await update.message.reply_text("❌ Please send a PNG file, not JPG, PDF, or others.")
            return
    elif update.message.photo:
        # take the highest resolution photo
        file = await update.message.photo[-1].get_file()
    else:
        await update.message.reply_text("❌ Please send a PNG file.")
        return

    if not os.path.exists(DOWNLOAD_DIR):
        os.makedirs(DOWNLOAD_DIR)

    file_path = os.path.join(DOWNLOAD_DIR, f"{file.file_unique_id}.png")
    await file.download_to_drive(file_path)

    try:
        with Image.open(file_path) as img:
            width, height = img.size

        if width == REQUIRED_WIDTH and height == REQUIRED_HEIGHT:
            await update.message.reply_text("✅ Dimensions are correct! Sending to admin...")
            await context.bot.send_document(
                chat_id=YOUR_TELEGRAM_ID,
                document=open(file_path, "rb"),
                caption=f"Design from @{update.message.from_user.username or update.message.from_user.id}"
            )
        else:
            await update.message.reply_text(
                f"❌ Wrong dimensions! Expected {REQUIRED_WIDTH}x{REQUIRED_HEIGHT}, "
                f"but got {width}x{height}."
            )
    except Exception as e:
        await update.message.reply_text("⚠️ Error processing the image.")
        logging.error(e)
    finally:
        os.remove(file_path)  # cleanup

# --- MAIN ---
def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(
        (filters.Document.FileExtension("png") | filters.PHOTO),
        handle_photo
    ))

    # catch all other document types
    app.add_handler(MessageHandler(filters.Document.ALL, lambda u, c: u.message.reply_text("❌ Please send a PNG file only.")))

    app.run_polling()

if __name__ == "__main__":
    main()
