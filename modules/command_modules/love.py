import random
from .. import irc, var

# Fill command dictionary.
def ins_command ():
    var.commands["love"] = type("command", (object,), {})()
    var.commands["love"].method = love
    var.commands["love"].tags = ["fun"]
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
    "hugs {} in a loving manner.",
    "nibbles on {}'s left ear.",
    "reads {}'s future."
]

# spoonm's anime list!
anime_list = [
    "Shigatsu wa Kimi no Uso",
    "Clannad",
    "Clannad ~After Story~",
    "Barakamon",
    "Gosick",
    "Bokura wa Minna Kawaisou",
    "Zankyou no Terror",
    "So Ra No Wo To",
    "Angel Beats!",
    "White Album 2",
    "The Garden of Words",
    "Golden Time",
    "Gekkan Shoujo Nozaki-kun",
    "Love Hina",
    "Hanasaku Iroha",
    "Dantalian no Shoka",
    "Plastic Memories"
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
    elif target == "spoonm":
        irc.msg(channel, "\001ACTION watches {} with spoonm.\001".format(random.choice(anime_list)))
    else:
        irc.msg(channel, "\001ACTION " + random.choice(love_list).format(target) + "\001")
