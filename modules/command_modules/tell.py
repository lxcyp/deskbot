import re
from .. import irc, var, ini
from ..tools import is_identified

# Require identification with NickServ to send messages.
def ident (f):
    def check (user, channel, word):
        if is_identified(user):
            f(user, channel, word)
        else:
            irc.msg(channel, "{}: Identify with NickServ first.".format(user))
    return check

# Insert a message monitor to look for user activity.
def ins_monitor (message):
    user = message.split("!")[0][1:]
    try:
        event = message.split(' ')[1]
    except IndexError:
        event = ''
    
    if event in ["JOIN", "PRIVMSG"]:
        send_messages(user)

# Fill commands dictionary.
def ins_command ():
    var.commands["tell"] = type("command", (object,), {})()
    var.commands["tell"].method = leave_message
    var.commands["tell"].aliases = [".tell", ".msg"]
    var.commands["tell"].usage = ["{} user message - Leave a message to user."]
    
    var.commands["listtell"] = type("command", (object,), {})()
    var.commands["listtell"].method = list_messages
    var.commands["listtell"].aliases = [".listtell", ".ltell", ".listtells", ".showtells"]
    var.commands["listtell"].usage = ["{} - Check if you have any messages and show them."]

# Fill a space for the messages database.
def ins_db ():
    var.data["messages"] = ini.fill_dict("messages.ini", "Messages")
    
    # Turning list of strings into a list of tuples.
    for user in var.data["messages"]:
        msg_list = [(msg.split(" ~ ")[0], msg.split(" ~ ", 1)[1]) for msg in var.data["messages"][user]]
        var.data["messages"][user] = msg_list

# Leave a message to someone.
def leave_message (user, channel, word):
    # It needs a nickname and a message.
    if len(word) < 3:
        irc.msg(channel, "{}: Wrong syntax. Check .help".format(user))
        return
    
    target = word[1]
    message = " ".join(word[2:])
    
    # Check if target is a valid nickname.
    if not re.match("[a-zA-Z\[\]\\`_\^\{\|\}][a-zA-Z0-9\[\]\\`_\^\{\|\}]", target):
        irc.msg(channel, "{} is not a valid nickname.".format(target))
        return
    
    # Check for "hurr Imma tell myself something".
    if target.lower() == user.lower():
        irc.msg(channel, "{}: Do it yourself. I'm not .tell'ing you shit!".format(user))
        return
    
    # The bot won't tell itself something.
    if target.lower() == irc.botnick.lower():
        irc.msg(channel, "{}: I'm right here, say it to my face!".format(user))
        return
    
    # Check for repeated messages.
    if target in var.data["messages"]:
        if (user, message) in var.data["messages"][target]:
            irc.msg(channel, "{}: You already left this message.".format(user))
            return
    
    # Create an empty list for users not in the database.
    if target not in var.data["messages"]:
        var.data["messages"][target] = []
    
    # Append tuple and add to ini.
    var.data["messages"][target].append((user, message))
    message_list = ["{} ~ {}".format(pair[0], pair[1]) for pair in var.data["messages"][target]]
    ini.add_to_ini("Messages", target, "\n".join(message_list), "messages.ini")
    
    irc.msg(channel, "{}: Message stored.".format(user))

# Send a user stored messages.
def send_messages (user):
    # Be case insensitive, please.
    for nick in var.data["messages"]:
        if user.lower() == nick.lower():
            user = nick
    
    # There's no use going on if the user isn't in the messages database.
    if user not in var.data["messages"]:
        return
    
    if len(var.data["messages"][user]) > 4:
        # Send the first 4 messages.
        for pair in var.data["messages"][user][0:4]:
            irc.msg(user, "{} sent you: {}".format(pair[0], pair[1]))
            irc.msg(pair[0], "{} received your message.".format(user))
        
        # Remove the sent messages.
        st_messages = var.data["messages"][user][0:4]
        for pair in st_messages:
            var.data["messages"][user].remove(pair)
        new_messages = ["{} ~ {}".format(pair[0], pair[1]) for pair in var.data["messages"][user]]
        ini.add_to_ini("Messages", user, "\n".join(new_messages), "messages.ini")
        
        irc.msg(user, "To reply to them, use .tell user message")
        irc.msg(user, "You have more messages. Type \x034.showtells\x0f to view them.")
    else:
        # Send every message.
        for pair in var.data["messages"][user]:
            irc.msg(user, "{} sent you: {}".format(pair[0], pair[1]))
            irc.msg(pair[0], "{} received your message.".format(user))
        
        # Remove them.
        del var.data["messages"][user]
        ini.remove_from_ini("Messages", user, "messages.ini")
        
        irc.msg(user, "To reply to them, use .tell user message")

# Send the rest of the messages.
def list_messages (user, channel, word):
    # There's no use going on if the user isn't in the messages database.
    if user not in var.data["messages"]:
        irc.msg(channel, "{}: You don't have any messages.".format(user))
        return
    
    send_messages(user)
    irc.msg(channel, "{}: Sent ;)".format(user))
