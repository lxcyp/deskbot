import os, sys
from modules import var, ini, irc, commands

os.system("clear")
print "Starting deskbot."

try:
    irc.server = sys.argv[1]
    irc.connect(irc.server, 6667)
except:
    print "No server to connect to was given."
    os._exit(0)

try:
    irc.botnick = sys.argv[2]
    irc.admin = sys.argv[3]
    irc.password = sys.argv[4]
except:
    pass

if not os.path.isfile("ini/desktops.ini"):
    print "There is no desktops.ini file."

ini.readFile()
irc.displayInfo()
irc.init()
irc.identify()

for channel in var.chanList:
    irc.join(channel)

while True:
    msgList = [msg for msg in irc.ircsock.recv(2048).split('\r\n') if msg]
    
    for msg in msgList:
        commands.read(msg)
