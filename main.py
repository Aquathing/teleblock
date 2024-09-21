from pyrogram import Client
from pyrogram.types import Message
from pyrogram.errors import FloodWait
from json import loads

config = loads(open("config.json", 'r').read())
app = Client("my_account", config["api_id"], config["api_hash"])


def check_for_interaction(client, user, n_message: int):
    """
    This method checks for the interaction with a user. If the last n messages are not from the self user,
     the chat is very likely from a spam account.

    :param client: Our client.
    :param user: The user that sent a message.
    :param n_message: The amount of messages to check back.
    :return: None
    """

    try:
        user_chat = client.get_chat(user.id)
    except FloodWait:
        return True

    msgs = client.get_chat_history(user_chat.id, n_message)

    for msg in msgs:
        if msg.from_user.is_self:

            # if we successfully checked for interaction once, we can store the user in memory
            # instead of checking the same user again (especially in case of rapid succession of messages)
            whitelist[user.id] = 1
            return True

    return False


def block_user(client, user):
    """
    Blocks the supplied user and logs the event.

    :param client: Our client.
    :param user: The user to block.
    :return: None
    """

    print(f"Blocking user @{user.username}")

    user.block()
    client.send_message("me", f"✨New blocked user✨\n"
                              f"Username:\t\t@{user.username}\n"
                              f"First name:\t\t{user.first_name}\n"
                              f"Last name:\t\t{user.last_name}\n")


@app.on_message()
def block_if_not_contacts(client: Client, message: Message):
    user = message.from_user

    # reduce overhead and errors
    if user is None:
        return

    # we don't want to block any person that sends a group message
    if not message.chat.type == ChatType.PRIVATE:
        return

    # if the user is a bot or in our contacts or whitelisted, it should be fine
    if user.is_contact or user.is_bot or whitelist.get(user.id):
        return

    if not check_for_interaction(client, user, 20):
        # womp womp
        block_user(app, user)


whitelist = {}

app.run()
