import random
from .. import irc, var

def ins_command ():
    var.commands["mio"] = type("command", (object,), {})()
    var.commands["mio"].method = mio
    var.commands["mio"].tags = ["fun"]
    var.commands["mio"].aliases = [".mio"]
    var.commands["mio"].usage = ["{} - Get a random picture of Mio."]

def mio (user, channel, word):
    f = open("misc/mio.txt", "r")
    p_list = [l.strip() for l in f.readlines()]
    f.close()
    
    irc.msg(channel, "Random picture of Mio: {}".format(random.choice(p_list)))
