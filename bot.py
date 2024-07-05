import subprocess
import json
import requests
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import schedule
import time as tm
from datetime import time, datetime
import os

print("Starting bot...")

# TOKEN = os.getenv('TOKEN')
daily_task_message_id = None

def escape_markdown_v2(text):
    """
    Helper function to escape text for Telegram MarkdownV2.
    """
    escape_chars = r'_*[]()~`>#+-=|{}.!'
    return ''.join(['\\' + char if char in escape_chars else char for char in text])

def fetch_daily_task():
    print("Fetching daily task with curl...")
    curl_command = [
        "curl",
        "-X", "POST", "https://leetcode.com/graphql/",
        "-H", "Content-type: application/json",
        "-H", "Origin: https://leetcode.com",
        "-H", "User-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "--data-raw", "{\"query\":\"query questionOfToday { activeDailyCodingChallengeQuestion { date link question { difficulty title } } }\",\"variables\":{},\"operationName\":\"questionOfToday\"}"
    ]

    try:
        result = subprocess.run(curl_command, capture_output=True, text=True)
        
        if result.returncode == 0:
            response = json.loads(result.stdout)
            if "data" in response and "activeDailyCodingChallengeQuestion" in response["data"]:
                daily_question = response["data"]["activeDailyCodingChallengeQuestion"]["question"]
                title = escape_markdown_v2(daily_question["title"])
                link = escape_markdown_v2("https://leetcode.com" + response["data"]["activeDailyCodingChallengeQuestion"]["link"])
                return f"Today's LeetCode task: ||{title}\n{link}||"
            else:
                print("Unexpected response structure:", response)
                return "Could not fetch today's LeetCode task."
        else:
            print(f"Error executing curl command: {result.stderr}")
            return "Error fetching today's LeetCode task."
    except Exception as e:
        print(f"Error fetching daily task with curl: {e}")
        return "Error fetching today's LeetCode task."

def fetch_motivational_quote():
    print("Fetching motivational quote...")
    try:
        response = requests.get("https://zenquotes.io/api/random")
        response.raise_for_status()
        quote_data = response.json()
        quote = escape_markdown_v2(quote_data[0]['q'])
        author = escape_markdown_v2(quote_data[0]['a'])
        return f"{quote} - {author}"
    except requests.exceptions.RequestException as e:
        print(f"Error fetching motivational quote: {e}")
        return "Error fetching motivational quote."

def send_daily_task(context: CallbackContext):
    global daily_task_message_id
    print("Sending daily task...")
    chat_id = context.job.context
    task_link = fetch_daily_task()
    message = context.bot.send_message(chat_id=chat_id, text=task_link, parse_mode='MarkdownV2', disable_web_page_preview=True)
    daily_task_message_id = message.message_id

def send_task_immediately(update: Update, context: CallbackContext):
    global daily_task_message_id
    print("Sending task immediately for testing...")
    chat_id = update.message.chat_id
    task_link = fetch_daily_task()
    message = context.bot.send_message(chat_id=chat_id, text=task_link, parse_mode='MarkdownV2', disable_web_page_preview=True)
    daily_task_message_id = message.message_id

def start(update: Update, context: CallbackContext):
    print("Starting scheduled task...")
    chat_id = update.message.chat_id
    context.job_queue.run_daily(send_daily_task, time=time(7, 0), context=chat_id)
    update.message.reply_text('I will send you daily LeetCode tasks at 7 AM!')

def handle_reply(update: Update, context: CallbackContext):
    global daily_task_message_id
    user = update.message.from_user
    user_name = user.username

    if update.message.reply_to_message and update.message.reply_to_message.message_id == daily_task_message_id:
        if user_name == 'bommie1005':
            display_name = 'Dina'
        else:
            display_name = user.first_name

        motivational_quote = fetch_motivational_quote()
        reply_text = f"{display_name}, good job. {motivational_quote}"
        update.message.reply_text(reply_text)

def main():
    print("Initializing Updater...")
    updater = Updater('7048375330:AAEIYAO4DJt91_fFfMmuFwNjafwnwt2D3AQ', use_context=True)
    dp = updater.dispatcher
    
    # Handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("send_now", send_task_immediately))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_reply))
    
    # Start the Bot
    print("Starting polling...")
    updater.start_polling()

    while True:
        schedule.run_pending()
        tm.sleep(1)

    updater.idle()

if __name__ == '__main__':
    print("Running main function...")
    main()
