from .. import irc, var, ini
import time

# Fill commands dictionary.
def ins_command ():
    var.commands["seen"] = type("command", (object,), {})()
    var.commands["seen"].method = seen
    var.commands["seen"].tags = ["fun"]
    var.commands["seen"].aliases = [".seen"]
    var.commands["seen"].usage = ["{} user - Be notified of when user was last seen."]

# Make space for it in var.data.
def ins_db ():
    var.data["seen"] = ini.fill_dict("seen.ini", "Seen")

# Insert message monitor.
def ins_monitor (message):
    user = message.split("!")[0][1:]
    try:
        event = message.split(' ')[1]
    except IndexError:
        event = ''
    
    # The user joins a channel.
    if event == "JOIN":
        try:
            channel = message.split(" :")[1]
        except IndexError:
            channel = message.split(" JOIN ")[1]
        
        timestamp = " ".join(time.ctime().split(" ")[1:])
        last_seen = ["joining {}.".format(channel), "Time: {}. (GMT-3:00)".format(timestamp)]
        
        ini.add_to_ini("Seen", user, "\n".join(last_seen), "seen.ini")
        var.data["seen"][user] = last_seen
    
    # The user leaves a channel.
    if event == "PART":
        channel = message.split(" PART ")[1].split(" :")[0]
        
        timestamp = " ".join(time.ctime().split(" ")[1:])
        last_seen = ["parting {}.".format(channel), "Time: {}. (GMT-3:00)".format(timestamp)]
        
        ini.add_to_ini("Seen", user, "\n".join(last_seen), "seen.ini")
        var.data["seen"][user] = last_seen
        
    # A channel message is received.
    elif event == "PRIVMSG":
        channel = message.split(' ')[2] if message.split(' ')[2] != irc.botnick else user
        content = message.split(' :', 1)[1] if len(message.split(' :')) > 1 else ''
        
        timestamp = " ".join(time.ctime().split(" ")[1:])
        last_seen = [
            "in {} saying: {}".format(channel, content),
            "Time: {}. (GMT -3:00)".format(timestamp)
        ]
        
        ini.add_to_ini("Seen", user, "\n".join(last_seen), "seen.ini")
        var.data["seen"][user] = last_seen

# Commad method.
def seen (user, channel, word):
    if len(word) == 1:
        irc.msg(channel, "Seen who?")
        return
    
    # Fun addition.
    if channel == "#rice" and irc.server == "irc.rizon.net" and word[1].lower() in [
        "kori", "kore", "coring", "cori",
        "curry", "corey", "koring", "koritos"
    ]:
        irc.msg(channel, "{}: kori's right there, what are you talking about?".format(user))
        return
    
    for nick in var.data["seen"]:
        if nick.lower() == word[1].lower():
            word[1] = nick
    
    if word[1] not in var.data["seen"]:
        irc.msg(channel, "{}: Sorry, I have not seen {}.".format(user, word[1]))
    else:
        irc.msg(channel, "{} was last seen {}".format(word[1], var.data["seen"][word[1]][0]))
        irc.msg(channel, var.data["seen"][word[1]][1])
