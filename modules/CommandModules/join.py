from .. import irc

def read (user, channel, word):
    
    if user != irc.admin:
        return
    
    try:
        irc.join(word[1])
    except:
        irc.msg(irc.admin, "Tell me some channel to join.")

def leave (user, channel, word):
    
    if user != irc.admin:
        return
    
    try:
        irc.part(word[1])
    except:
        irc.msg(irc.admin, "Tell me some channel to leave.")
