import logging
import os
import random
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, JobQueue

# Load environment variables from .env file
load_dotenv()

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Predefined list of motivational quotes
QUOTES = [
    "Believe you can and you're halfway there.",
    "Your limitation—it's only your imagination.",
    "Push yourself, because no one else is going to do it for you.",
    "Great things never come from comfort zones.",
    "Success doesn’t just find you. You have to go out and get it.",
    "The harder you work for something, the greater you'll feel when you achieve it.",
    "Dream bigger. Do bigger.",
    "Don’t stop when you’re tired. Stop when you’re done.",
    "Wake up with determination. Go to bed with satisfaction.",
    "Do something today that your future self will thank you for.",
    "Little things make big days.",
    "It’s going to be hard, but hard does not mean impossible.",
    "Don’t wait for opportunity. Create it.",
    "Sometimes we’re tested not to show our weaknesses, but to discover our strengths.",
    "The key to success is to focus on goals, not obstacles.",
    "Dream it. Wish it. Do it.",
    "No matter how slow you go, you’re still lapping everyone on the couch.",
    "Good things come to those who work hard.",
    "Don’t watch the clock; do what it does. Keep going.",
    "You don’t have to be great to start, but you have to start to be great.",
    "The only way to do great work is to love what you do.",
    "The future depends on what you do today.",
    "Believe in yourself and all that you are. Know that there is something inside you that is greater than any obstacle.",
    "The pain you feel today will be the strength you feel tomorrow.",
    "Failure is the opportunity to begin again more intelligently.",
    "It always seems impossible until it’s done.",
    "Your only limit is your mind.",
    "Push yourself, because no one else is going to do it for you.",
    "Do what you can with all you have, wherever you are.",
    "You are never too old to set another goal or to dream a new dream.",
    "You learn more from failure than from success. Don’t let it stop you. Failure builds character.",
    "Don’t be afraid to give up the good to go for the great.",
    "The only place where success comes before work is in the dictionary.",
    "It’s not whether you get knocked down, it’s whether you get up.",
    "We generate fears while we sit. We overcome them by action.",
    "What you get by achieving your goals is not as important as what you become by achieving your goals.",
    "Act as if what you do makes a difference. It does.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "Hardships often prepare ordinary people for an extraordinary destiny.",
    "You are braver than you believe, stronger than you seem, and smarter than you think.",
    "Keep your face always toward the sunshine—and shadows will fall behind you.",
    "Start where you are. Use what you have. Do what you can.",
    "It’s not about perfect. It’s about effort.",
    "Strive not to be a success, but rather to be of value.",
    "The best revenge is massive success.",
    "The only limit to our realization of tomorrow is our doubts of today.",
    "Failure will never overtake me if my determination to succeed is strong enough.",
    "If you’re going through hell, keep going.",
    "If you want something you never had, you have to do something you’ve never done.",
    "Success is walking from failure to failure with no loss of enthusiasm.",
    "Just when the caterpillar thought the world was over, it became a butterfly.",
    "Success is not how high you have climbed, but how you make a positive difference to the world.",
    "You can waste your lives drawing lines. Or you can live your life crossing them.",
    "Believe you can and you're halfway there.",
    "It does not matter how slowly you go as long as you do not stop.",
    "Start where you are. Use what you have. Do what you can.",
    "The best way to predict your future is to create it.",
    "I am not a product of my circumstances. I am a product of my decisions.",
    "Don’t wish it were easier; wish you were better.",
    "We may encounter many defeats but we must not be defeated.",
    "You have to fight through some bad days to earn the best days of your life.",
    "Life is 10% what happens to us and 90% how we react to it.",
    "It’s not about how bad you want it. It’s about how hard you’re willing to work for it.",
    "The difference between who you are and who you want to be is what you do.",
    "Your life does not get better by chance, it gets better by change.",
    "Do something today that your future self will thank you for.",
    "Start each day with a positive thought and a grateful heart.",
    "The only way to achieve the impossible is to believe it is possible.",
    "If it doesn’t challenge you, it doesn’t change you.",
    "The only place where dreams become impossible is in your own thinking.",
    "Do what you can with all you have, wherever you are.",
    "Success is not final, failure is not fatal: It is the courage to continue that counts.",
    "Our greatest glory is not in never falling, but in rising every time we fall.",
    "A winner is a dreamer who never gives up.",
    "Don’t be pushed around by the fears in your mind. Be led by the dreams in your heart.",
    "Don’t let yesterday take up too much of today.",
    "Don’t wait for opportunity. Create it.",
    "You are enough just as you are.",
    "Great things never come from comfort zones.",
    "If you’re offered a seat on a rocket ship, don’t ask what seat! Just get on.",
    "The purpose of our lives is to be happy.",
    "Happiness is not something ready-made. It comes from your own actions.",
    "Life is what happens when you’re busy making other plans.",
    "Success usually comes to those who are too busy to be looking for it.",
    "The way to get started is to quit talking and begin doing.",
    "Don’t be afraid to give up the good to go for the great.",
    "If you set your goals ridiculously high and it’s a failure, you will fail above everyone else’s success.",
    "Hardships often prepare ordinary people for an extraordinary destiny.",
    "The ones who are crazy enough to think they can change the world, are the ones who do.",
    "There is no secret to success. It is the result of preparation, hard work, and learning from failure.",
    "In the end, it’s not the years in your life that count. It’s the life in your years.",
    "Success is not the key to happiness. Happiness is the key to success. If you love what you are doing, you will be successful.",
    "The best time to plant a tree was 20 years ago. The second best time is now.",
    "The only impossible journey is the one you never begin.",
    "Your time is limited, so don’t waste it living someone else’s life.",
    "Every moment is a fresh beginning.",
    "Live as if you were to die tomorrow. Learn as if you were to live forever.",
    "The best way to get started is to quit talking and begin doing."
]

# Function to handle the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the Daily Quotes Bot! Use /subscribe to receive daily quotes.")

# Function to handle the /chatid command
async def chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await update.message.reply_text(f"Your chat ID is: {chat_id}")

# Function to send a motivational quote every minute
async def send_minute_quote(context: ContextTypes.DEFAULT_TYPE):
    quote = random.choice(QUOTES)
    await context.bot.send_message(chat_id=context.job.chat_id, text=quote)

# Function to subscribe to daily quotes
async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    job_removed = remove_job_if_exists(str(chat_id), context)
    context.job_queue.run_repeating(send_minute_quote, interval=60, first=10, chat_id=chat_id, name=str(chat_id))
    text = "You have subscribed to receive a motivational quote every minute!" if job_removed else "You are already subscribed."
    await update.message.reply_text(text)

# Function to unsubscribe from daily quotes
async def unsubscribe(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = "You have unsubscribed from receiving motivational quotes." if job_removed else "You were not subscribed."
    await update.message.reply_text(text)

# Helper function to remove existing jobs
def remove_job_if_exists(name: str, context: ContextTypes.DEFAULT_TYPE):
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True

if __name__ == '__main__':
    # Load Telegram Bot API token from environment variable
    TELEGRAM_BOT_API = os.getenv("TELEGRAM_BOT_API")
    
    # Create the application
    application = ApplicationBuilder().token(TELEGRAM_BOT_API).build()
    
    # Register the command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('chatid', chat_id))
    application.add_handler(CommandHandler('subscribe', subscribe))
    application.add_handler(CommandHandler('unsubscribe', unsubscribe))
    
    # Start polling
    application.run_polling()
