import json

SAVED_DATA = "id.json"
def save_data(filepath, data):
    with open(filepath, "w") as f:
        json.dump(data, f)

def load_data(filepath):
    try:
        with open(filepath, "r") as f:
            data = json.load(f)
            return data
    except:
        return {}

data = load_data(SAVED_DATA)

save_data(SAVED_DATA, "hssgha")
print("Data saved!")


# def get_chat_id(bot_token):
#     updater = Updater(token=bot_token, use_context=True)
#     bot = updater.bot
#     chat_id = bot.get_updates()[-1].message.chat_id
#     return chat_id

# chat_id = get_chat_id(token)
# print(chat_id)

# Ethereum address to track
