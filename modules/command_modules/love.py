from .. import irc, var
import random

# Fill command dictionary.
def ins_command ():
    var.commands["love"] = type("command", (object,), {})()
    var.commands["love"].method = love
    var.commands["love"].aliases = [".love"]
    var.commands["love"].usage = ["{} user - Send user some love."]

# The love list!
love_list = [
    "gives {} a bear hug.",
    "d-doesn't like {}, you b-baka!",
    "lovingly eviscerates {}.",
    "prepares a bento box for {}.",
    "cooks a romantic dinner for {}.",
    "watches the stars under the moonlight with {}.",
    "sits next to {}, making no eye contact whatsoever.",
    "shyly approaches {} and mutters: \"c-can I hold your hand?\"",
    "plays a lullaby for {}.",
    "sings {} a love ballad.",
    "dances a slow waltz with {}.",
    "gives {} a delicious steak.",
    "bakes a cake for {}.",
    "hugs {} in a loving manner."
]

# The love function!
def love (user, channel, word):
    # If nothing other than '.love' is issued, make the user the target.
    if len(word) > 1:
        target = " ".join(word[1:])
    else:
        target = user
    
    if target == irc.botnick:
        irc.msg(channel, "{}: y-you too!".format(user))
    else:
        irc.msg(channel, "\001ACTION " + random.choice(love_list).format(target) + "\001")