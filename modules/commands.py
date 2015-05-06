import irc, var, ini
from CommandModules import desktops, join

def read (message):
    
    print message
    
    if message.startswith("PING"):
        return ping(message)
    
    user = message.split("@")[0].split("!")[0][1:]
    try:
        event = message.split(" ")[1]
    except:
        event = ""
    
    if event == "PRIVMSG":
        channel = message.split(" ")[2]
        
        if channel == irc.botnick:
            channel = user
        
        try:
            content = message.split(" :", 1)[1]
        except IndexError:
            return
        
        word = [w for w in content.split(" ") if w]
        privmsg(user, channel, word)
    elif event == "INVITE":
        channel = message.split(" :", 1)[1]
        irc.join(channel)
        irc.msg(channel, "{} called.".format(user))

def privmsg (user, channel, word):
    
    if not word:
        return
    
    if user == irc.admin and word[0] == "join":
	if len(word) > 1:
		irc.join(word[1])
    
    if word[0] in commands:
        commands[word[0]](user, channel, word)

def ping (message):
    data = message.split(" :")[1]
    irc.pong(data)

def _reload (user, channel, word):
    
    if user != irc.admin:
        return
    
    reload(desktops)
    ini.readFile()

def help (user, channel, word):
    irc.notice(user, ".desktop - View your desktop list.")
    irc.notice(user, ".desktop -a url1 url2 ... - Add a list of urls to your list.")
    irc.notice(user, "--add and -add work as well.")
    irc.notice(user, ".desktop -rm n1,n2,n3,... - Remove an url from your list.")
    irc.notice(user, "--remove and -remove work as well. * will remove everything.")
    irc.notice(user, ".desktop -re n url - Replace a url from your list.")
    irc.notice(user, "--replace and -replace work as well.")
    irc.notice(user, ".desktop user - View user's desktop list.")
    irc.notice(user, ".desktop user n - View user's nth desktop url.")

def identify (user, channel, word):
    
    if user != irc.admin:
        return
    
    irc.identify()

commands = {
    ".desktop":desktops.Desktops,
    ".dtop":desktops.Desktops,
    ".dekstop":desktops.Desktops,
    ".join":join.read,
    ".leave":join.leave,
    
    ".reload":_reload,
    ".help":help,
    ".identify":identify
}
