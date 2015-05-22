from .. import irc

# Functions that return booleans.

# Check for NickServ authentication.
def is_identified (user):
    irc.msg("NickServ", "STATUS {}".format(user))
    NickServ = False
    
    while not NickServ:
        irclist = [ x for x in irc.ircsock.recv(2048).split('\r\n') if x ]
        for msg in irclist:
            if msg.startswith(":NickServ"):
                NickServ = msg
            else:
                read(msg)
    
    if "STATUS {} 3".format(user) in NickServ:
        return True
    else:
        return False

# Check if a value is an integer.
def is_number (num):
    try:
        int(num)
        return True
    except ValueError:
        return False

# Functions that return values.

# We want to get rid of certain characters.
def trim (string):
    if "\x03" in string:
        string = string.split("\x03")[0]
    if "\x02" in string:
        str = string.split("\x02")[0]
    if "\x1d" in string:
        str = string.split("\x1d")[0]
    if "\x0f" in string:
        str = string.split("\x0f")[0]
    return string

# We want to tag NSFW urls as NSFW.
def nsfw_check (url_pair):
    if "!" in url_pair.split(" ")[1]:
        url_pair = "[\x034NSFW\x0f] {}".format(url_pair.split(" ")[1].strip("!"))
    return url_pair
