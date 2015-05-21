import sys
from .. import irc

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

# We want to get rid of certain characters.
def trim (str):
    if "\x03" in str:
        str = str.split("\x03")[0]
    if "\x02" in str:
        str = str.split("\x02")[0]
    if "\x1d" in str:
        str = str.split("\x1d")[0]
    if "\x0f" in str:
        str = str.split("\x0f")[0]
    return str
