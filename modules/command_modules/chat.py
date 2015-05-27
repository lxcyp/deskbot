from .. import irc, var
from ..chatterbotapi import ChatterBotFactory, ChatterBotType

# Fill command dictionary.
def ins_command ():
    var.commands["chat"] = type("command", (object,), {})()
    var.commands["chat"].method = chat
    var.commands["chat"].aliases = [".chat"]
    var.commands["chat"].usage = [
        "{} msg - sends msg to cleverbot's api and says the reply in the chat"
    ]

# Command method.
def chat (user, channel, word):
    factory = ChatterBotFactory()
    bot1 = factory.create(ChatterBotType.CLEVERBOT)
    bot1session = bot1.create_session()
    if len(word) == 1:
        irc.msg(channel, "{}: You need to add a message.".format(user))
    else:
        text = " ".join(word[1:])
        think = bot1session.think(text)
        
        irc.msg(channel, "{}: {}".format(user, think))
