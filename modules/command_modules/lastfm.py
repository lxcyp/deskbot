###################################################
#                                                 #
# Originally, part of this was in a hexchat addon #
# by TingPing. I went so far as to steal the key  #
# used to communicate with the API. There wasn't  #
# any credit where I got the plugin from, and I   #
# even tweaked it a bit to make it more usable.   #
# Either way, here's to TingPing. Cheers, mate.   #
#                                                 #
###################################################

from __future__ import print_function

import sys
import json
import thread

if sys.version_info[0] == 2:
        import urllib2 as urllib_error
        import urllib as urllib_request
else:
        import urllib.error as urllib_error
        import urllib.request as urllib_request

from .. import irc, var, ini

# API key.
KEY = '4847f738e6b34c0dc20b13fe42ea008e'

# Fill command dictionary.
def ins_command ():
    var.commands["lastfm"] = type("command", (object,), {})()
    var.commands["lastfm"].method = lastfm
    var.commands["lastfm"].aliases = [".lfm", ".np", ".lastfm"]
    var.commands["lastfm"].tags = ["other", "fun"]
    var.commands["lastfm"].usage = [
        "{} - Show the world what you're listening to right now.",
        "{} user - Check user's last.fm now playing data.",
        "{} -u username - Check username's last.fm now playing data. Actual username.",
        "{} -s your_user - Save your last.fm username."
    ]

# Insert a username database.
def ins_db ():
    var.data["lastfm"] = ini.fill_dict("lastfm", "lastfm.ini")
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
        track = get_track(var.data["lastfm"][user])
    else:
        track = get_track(user)
    
    # If nothing is playing.
    if not track:
        irc.msg(channel, "{} isn't listening to anything right now.".format(user))
        return
    
    # Grab le values.
    try:
        title = track['name']
        artist = track['artist']['#text']
        album = track['album']['#text']
        title = title.encode('utf-8')
        artist = artist.encode('utf-8')
        album = album.encode('utf-8')
    except KeyError:
        irc.msg(channel, "last.fm song info not found.")
        return

    line = "\x0f{} by {}".format(title, artist)
    line += " on {}\x0f".format(album) if album else ""
    
    irc.msg(channel, "{} [{}]".format(line, user))

def get_track(username):
    url = 'http://ws.audioscrobbler.com/2.0/?method=user.getrecentTracks&user={}&api_key={}&format=json'.format(username, KEY)
    try:
        response = urllib_request.urlopen(url)
        text = response.read().decode('utf-8')
        response.close()
    except urllib_error.HTTPError:
        return

    data = json.loads(text)

    try:
        track = data['recenttracks']['track'][0]
        if track['@attr']['nowplaying']:
            return track
    except (IndexError, KeyError):
        return
