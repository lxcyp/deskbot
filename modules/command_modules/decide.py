import random
from .. import irc, var

# Fill command dictionary.
def ins_command ():
    var.commands["decide"] = type("command", (object,), {})()
    var.commands["decide"].method = decide
    var.commands["decide"].tags = ["other"]
    var.commands["decide"].aliases = [".decide", ".choose"]
    var.commands["decide"].usage = [
        "{} a|b|c|d|... - Decide between a, b, c, ...",
        "{} a or b or c or ... - Decide between a, b, c, ...",
        "{} a,b,c,... - Decide between a, b, c, ...",
        "{} a - Decide between Yes and No.",
        "That is the order of preference. You can do {} a or b | c, which will decide between \"a or b\" and c."
    ]

# Command method.
def decide (user, channel, word):
    if len(word) == 1:
        irc.msg(channel, "{}: You have to give me some choices.".format(user))
    else:
        string = " ".join(word[1:])
        if "|" in string:
            choices = [choice.strip() for choice in string.split("|") if choice]
        elif " or " in string:
            choices = [choice.strip() for choice in string.split(" or ") if choice]
        elif "," in string:
            choices = [choice.strip() for choice in string.split(",") if choice]
        else:
            choices = ["Yes.", "No."]
        
        # Empty lists can't be taken.
        if not choices:
            irc.msg(channel, "{}: Give me some choices, man, come on.".format(user))
            return
        
        if random.random() < 0.05:
            if choices == ["Yes.", "No."]:
                irc.msg(channel, "{}: Maybe.".format(user))
            else:
                irc.msg(channel, "{}: Neither.".format(user))
        else:
            irc.msg(channel, "{}: {}".format(user, random.choice(choices)))
