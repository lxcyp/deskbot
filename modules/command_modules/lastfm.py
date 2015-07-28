import pylast
import thread
from pylast import WSError as err
from .. import irc, var, ini

# Grabbing API keys from file.
with open("api-keys/lastfm", "r") as keys_file:
    pair = keys_file.readlines()
    KEY = pair[0].strip()
    SECRET = pair[1].strip()

network = pylast.LastFMNetwork(api_key = KEY, api_secret = SECRET)

# Fill command dictionary.
def ins_command ():
    var.commands["lastfm"] = type("command", (object,), {})()
    var.commands["lastfm"].method = lastfm
    var.commands["lastfm"].aliases = [".lfm", ".np", ".lastfm"]
    var.commands["lastfm"].tags = ["other", "fun", "web"]
    var.commands["lastfm"].usage = [
        "{} - Show the world what you're listening to right now.",
        "{} user - Check user's last.fm now playing data.",
        "{} -u username - Check username's last.fm now playing data. Actual username.",
        "{} -s your_user - Save your last.fm username."
    ]

# Insert a username database.
def ins_db ():
    var.data["lastfm"] = ini.fill_dict("lastfm.ini", "lastfm")
    var.data["lastfm"] = {
        user:var.data["lastfm"][user][0]
        for user in var.data["lastfm"]
    }

# Command method.
def lastfm (user, channel, word):
    if len(word) == 1:
        thread.start_new_thread(display_track, (user, channel))
    elif word[1] in ["-s", "-setusername", "-set"] and len(word) > 2:
        save_username(user, channel, word[2])
    elif word[1] in ["-u", "-username", "-user"] and len(word) > 2:
        thread.start_new_thread(display_track, (word[2], channel))
    else:
        thread.start_new_thread(display_track, (word[1], channel))

# Misc functions.

def save_username (user, channel, username):
    var.data["lastfm"][user] = username
    ini.add_to_ini("lastfm", user, username, "lastfm.ini")
    
    irc.msg(channel, "{}: Your last.fm username was saved.".format(user))

def display_track (user, channel):
    # Case insensitive for user in username database.
    for nick in var.data["lastfm"]:
        if user.lower() == nick.lower():
            user = nick
    
    # Username to use for track grabbin'.
    if user in var.data["lastfm"]:
        acc = network.get_user(var.data["lastfm"][user])
    else:
        acc = network.get_user(user)
    
    # There will be an error if the user doesn't exist.
    try:
        track = acc.get_now_playing()
    except err:
        irc.msg(channel, "User not found: {}.".format(acc))
        return
    
    # If nothing is playing, track is None.
    if not track:
        irc.msg(channel, "\x0f{} isn't listening to anything right now.".format(user))
        return
    
    # Grab values.
    title = track.title
    artist = track.artist

    line = "\x0f{} by {}\x0f".format(title, artist)
    irc.msg(channel, "{} [{}]".format(line, user))
