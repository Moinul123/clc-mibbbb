import requests
import urllib.parse
import json

# Define your bot token
TOKEN = "7150044305:AAHwaCBBP798BwlEMoyZiXHKc0r6SqZLgqU"

# Admin details
admin_id = 5645032505
admin_username = "jamesalise"

# Store user details
user_details = {}

# Function to send a simple text message to a user
def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={urllib.parse.quote(text)}"
    requests.get(url)

# Function to send message to a user with inline keyboard markup
def send_message_with_inline_keyboard(chat_id, text, inline_keyboard):
    keyboard = {"inline_keyboard": inline_keyboard}
    payload = {"chat_id": chat_id, "text": text, "reply_markup": json.dumps(keyboard)}
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, json=payload)

# Command handlers
def start(chat_id, name, username):
    send_message(chat_id, "𝐖𝐞𝐥𝐜𝐨𝐦𝐞 𝐭𝐨 𝐌𝐈𝐁 𝐂𝐚𝐥𝐜𝐮𝐥𝐚𝐭𝐨𝐫 𝐁𝐨𝐭!\n\nThis bot can perform calculations.Send me any arithmetic expression like '2+2' and I'll solve it for you.\n\n#𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐘 𝐌𝐈𝐁 𝐭𝐞𝐚𝐦")
    # Register the user with their name and username when they start using the bot
    user_details[chat_id] = {'name': name, 'username': username}

def help_command(chat_id):
    send_message(chat_id, "This bot can perform calculations.Send me any arithmetic expression like '2+2' and I'll solve it for you.\n\nIf anyone need any or help contact to our admin @Jamesalise")

def calculate(chat_id, expression):
    try:
        result = eval(expression)
        # Plain text result
        plain_text_result = f"{expression} = {result}"
        # Inline keyboard markup
        inline_keyboard = [[{"text": f"Result: {result}", "callback_data": "result"}]]
        # Combined message with both formats
        combined_message = f"     {plain_text_result}\n"
        # Send the combined message with inline keyboard
        send_message_with_inline_keyboard(chat_id, combined_message, inline_keyboard)
    except Exception as e:
        send_message(chat_id, "Sorry, I couldn't calculate that.")


def notify_all_users(chat_id, sender_id, message):
    if sender_id == admin_id:
        for user_id in user_details:
            send_message(user_id, message)
    else:
        send_message(chat_id, "You are not authorized to send notifications.\n\nOnly ADMIN can access this")

def get_user_details(chat_id, user_id):
    if user_id in user_details:
        details = user_details[user_id]
        reply_text = f"▪𝐘𝐨𝐮𝐫 𝐍𝐚𝐦𝐞 = {details['name']}\n▪𝐘𝐨𝐮𝐫 𝐔𝐬𝐞𝐫𝐧𝐚𝐦𝐞= {details['username']}\n▪𝐘𝐨𝐮𝐫 𝐮𝐬𝐞𝐫𝐢𝐝 = {user_id}\n\n𝐏𝐨𝐰𝐞𝐫𝐞𝐝 𝐁𝐘 𝐌𝐈𝐁 𝐭𝐞𝐚𝐦"
        send_message(chat_id, reply_text)
    else:
        send_message(chat_id, "You're not registered with the bot.Send /start to register")

def list_all_users(chat_id, sender_id):
    if sender_id == admin_id:
        users = ""
        for user_id, details in user_details.items():
            users += f"User ID: {user_id}, Username: {details['username']}\n"
        send_message(chat_id, "𝐥𝐢𝐬𝐭 𝐨𝐟 𝐛𝐨𝐭 𝐮𝐬𝐞𝐫𝐬:\n\n" + users)
    else:
        send_message(chat_id, "You are not authorized to access this command.Only admin can access this ")

# Admin command handlers
def admin_panel(chat_id, sender_id):
    if sender_id == admin_id:
        user_count = len(user_details)
        bot_token = TOKEN
        reply_text = f"Bot Token: {bot_token}\nTotal User: {user_count}"
        send_message(chat_id, reply_text)
    else:
        send_message(chat_id, "You are not authorized to access the admin panel.Only admin can access this")

# Handler for non-command messages
def process_message(chat_id, text, name=None, username=None, sender_id=None):
    if text.startswith("/start"):
        start(chat_id, name, username)
    elif text.startswith("/help"):
        help_command(chat_id)
    elif text.startswith("/ntf"):
        notify_all_users(chat_id, sender_id, text[4:].strip())
    elif text.startswith("/user"):
        get_user_details(chat_id, chat_id)
    elif text.startswith("/admin"):
        admin_panel(chat_id, sender_id)
    elif text.startswith("/list"):
        list_all_users(chat_id, sender_id)
    else:
        calculate(chat_id, text)

# Main function to handle updates
def main():
    update_id = None
    while True:
        url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
        if update_id:
            url += f"?offset={update_id + 1}"
        response = requests.get(url)
        updates = response.json()["result"]
        if updates:
            for update in updates:
                update_id = update["update_id"]
                if "message" in update:
                    message = update["message"]
                    chat_id = message["chat"]["id"]
                    text = message.get("text", "")
                    name = message["from"].get("first_name", "")
                    username = message["from"].get("username", "")
                    sender_id = message["from"]["id"]  # Added to get sender_id
                    process_message(chat_id, text, name, username, sender_id)  # Pass sender_id

if __name__ == "__main__":
    main()
