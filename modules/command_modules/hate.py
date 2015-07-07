from .. import irc, var
import random

# Fill command dictionary.
def ins_command ():
    var.commands["hate"] = type("command", (object,), {})()
    var.commands["hate"].method = hate
    var.commands["hate"].tags = ["fun"]
    var.commands["hate"].aliases = [".hate"]
    var.commands["hate"].usage = ["{} user - Send user some hateful message."]

# The hate list!
hate_list = [
    "slaps {} in the face.",
    "kicks {} in the balls/tits.",
    "pulls {}'s hair.",
    "spits on {}'s face.",
    "makes {} breathe fire with napalm.",
    "poisons {}'s food.",
    "staples {}'s ears.",
    "gives {} the middle finger.",
    "eviscerates {} in a non-loving manner.",
    "calls 911 and tells the cops {} raped her cousin."
]

# The hate function!
def hate (user, channel, word):
    # If nothing other than '.hate' is issued, make the user the target.
    if len(word) > 1:
        target = " ".join(word[1:])
    else:
        target = user
    
    if target == irc.botnick:
        irc.msg(channel, "{}: no u".format(user))
    else:
        irc.msg(channel, "\001ACTION " + random.choice(hate_list).format(target) + "\001")
