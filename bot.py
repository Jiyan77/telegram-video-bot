import os
import json
import logging
import time
import pytz
import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Load environment variables
BOT_TOKEN = "7802962867:AAGezJxqs-DKNKDdMj2XdBj2_YUueS4KPcY"  # টেলিগ্রাম বট টোকেন
TARGET_GROUP_ID = "-1002300932976"  # টার্গেট গ্রুপ আইডি
BACKUP_CHANNEL_URL = "https://t.me/+exNiJX3B_1AzNjdh"  # ব্যাকআপ চ্যানেল লিংক
BROADCAST_INTERVAL_HOURS = 24  # ব্রডকাস্ট মেসেজের সময়সীমা (ঘন্টায়)

# JSON file to store user data
USERS_FILE = "users.json"

# Load user data from JSON file
def load_users():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r') as file:
                return json.load(file)
        else:
            # Create empty users structure if file doesn't exist
            return {"users": []}
    except Exception as e:
        logger.error(f"Error loading users file: {e}")
        return {"users": []}

# Save user data to JSON file
def save_users(users_data):
    try:
        with open(USERS_FILE, 'w') as file:
            json.dump(users_data, file)
    except Exception as e:
        logger.error(f"Error saving users file: {e}")

# Track user interaction with the bot
def track_user_sync(user_id, username=None, first_name=None):
    users_data = load_users()
    
    # Check if user already exists
    user_exists = False
    for user in users_data["users"]:
        if user["id"] == user_id:
            user_exists = True
            user["last_activity"] = datetime.now().isoformat()
            if username:
                user["username"] = username
            if first_name:
                user["first_name"] = first_name
            break
    
    # Add new user if not exists
    if not user_exists:
        users_data["users"].append({
            "id": user_id,
            "username": username,
            "first_name": first_name,
            "joined_date": datetime.now(pytz.timezone('Asia/Dhaka')).isoformat(),
            "last_activity": datetime.now(pytz.timezone('Asia/Dhaka')).isoformat()
        })
    
    save_users(users_data)

# Create the bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Send broadcast message to all users
async def send_broadcast_message():
    users_data = load_users()
    
    # Create the inline keyboard with the backup group button
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ব্যাকআপ চ্যানেল", url=BACKUP_CHANNEL_URL)]
    ])
    
    message_text = (
        "ভিডিও আনলক করতে আমাদের ব্যাকআপ "
        "চ্যানেলে জয়েন করুন। সরাসরি ভিডিও "
        "দেওয়ার কারণে যে কোনো সময় আমাদের "
        "গ্রুপ ব্যান হতে পারে তাই অবশ্যই ব্যাকআপ "
        "গ্রুপে জয়েন থাকবেন।\n\n"
        "Please join our backup group to stay with us. Click on the \"Backup Channel\" button to join our backup."
    )
    
    sent_count = 0
    failed_count = 0
    
    # Send message to all users
    for user in users_data["users"]:
        try:
            await bot.send_message(
                chat_id=user["id"],
                text=message_text,
                reply_markup=keyboard
            )
            sent_count += 1
            # Small delay to avoid hitting Telegram's rate limits
            await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Failed to send broadcast to user {user['id']}: {e}")
            failed_count += 1
    
    logger.info(f"Broadcast completed: {sent_count} messages sent, {failed_count} failed")

@dp.message(Command("start"))
async def start_command(message: types.Message) -> None:
    """Send a message when the command /start is issued."""
    user = message.from_user
    
    # Track the user who started the bot
    track_user_sync(user.id, user.username, user.first_name)
    
    # Create keyboard with backup channel button
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ব্যাকআপ চ্যানেল", url=BACKUP_CHANNEL_URL)]
    ])
    
    await message.answer(
        "This is a video sender bot. This bot send anonymously 18+ desi video to দেশি ভিডিও group. "
        "please upload desi video only.\n\n"
        "This bot is made by @your_next1.",
        reply_markup=keyboard
    )

@dp.message(Command("help"))
async def help_command(message: types.Message) -> None:
    """Send a message when the command /help is issued."""
    user = message.from_user
    
    # Track the user who used help command
    track_user_sync(user.id, user.username, user.first_name)
    
    # Create keyboard with backup channel button
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="ব্যাকআপ চ্যানেল", url=BACKUP_CHANNEL_URL)]
    ])
    
    await message.answer(
        "This is a video sender bot. This bot send anonymously 18+ desi video to দেশি ভিডিও group. "
        "please upload desi video only.\n\n"
        "This bot is made by @your_next1.",
        reply_markup=keyboard
    )

@dp.message(F.video)
async def handle_video(message: types.Message) -> None:
    """Handle video messages and forward them anonymously to the target group."""
    if not TARGET_GROUP_ID:
        await message.answer("Error: Target group ID not configured. Please contact the administrator.")
        logger.error("TARGET_GROUP_ID environment variable not set")
        return

    user = message.from_user
    # Track the user who sent video
    track_user_sync(user.id, user.username, user.first_name)
    logger.info(f"Received video from user {user.id} ({user.first_name})")
    
    # Check if the caption contains any text or links
    if message.caption:
        # Check if caption contains links
        if 'http' in message.caption or 't.me' in message.caption:
            await message.answer("Please remove any links from the video caption and try again.")
            logger.info(f"Rejected video with links in caption from user {user.id}")
            return
        # If any caption text exists
        await message.answer("Please remove caption text from the video and try again.")
        logger.info(f"Rejected video with caption text from user {user.id}")
        return

    try:
        # Get the video message
        video = message.video
        
        # Send the video to the target group (this creates a new message rather than forwarding)
        await bot.send_video(
            chat_id=int(TARGET_GROUP_ID),  # Convert to integer to ensure proper format
            video=video.file_id,
            # No caption
            duration=video.duration,
            width=video.width,
            height=video.height,
            supports_streaming=True
        )
        
        await message.answer("Your video has been anonymously shared to the group!")
        logger.info(f"Successfully forwarded video from user {user.id} to group {TARGET_GROUP_ID}")
    
    except Exception as e:
        await message.answer("Sorry, there was an error sharing your video. Please try again later.")
        logger.error(f"Error forwarding video: {e}")

@dp.message(~F.video & (F.photo | F.document | F.audio | F.voice | F.animation | F.sticker))
async def handle_non_video(message: types.Message) -> None:
    """Handle non-video messages with a rejection message."""
    user = message.from_user
    # Track the user who sent non-video content
    track_user_sync(user.id, user.username, user.first_name)
    try:
        await message.answer("Please upload only desi video.")
        logger.info(f"Rejected non-video content from user {user.id} ({user.first_name})")
    except Exception as e:
        logger.error(f"Error sending rejection message: {e}")

async def main():
    """Main function to start the bot."""
    try:
        logger.info("Starting bot")
        print("Bot is starting...")
        
        # Setup scheduler for broadcasting messages
        scheduler = AsyncIOScheduler()
        scheduler.add_job(send_broadcast_message, 'interval', 
                        hours=BROADCAST_INTERVAL_HOURS, 
                        next_run_time=datetime.now() + timedelta(hours=1))
        
        # Start the scheduler
        scheduler.start()
        
        # Start polling
        await dp.start_polling(bot)
        
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped")
    except Exception as e:
        logger.error(f"Error in main: {e}")
        print(f"Error in main: {e}")
        
if __name__ == "__main__":
    asyncio.run(main())