import os, sys
from modules import ini, irc, commands, var

os.system("clear")
print "Starting deskbot."

# Grabbing arguments given.

try:
    irc.server = sys.argv[1]
except IndexError:
    print "No server to connect to was given."
    irc.server = raw_input("Server to connect to: ")

try:
    for i, arg in enumerate(sys.argv):
        if arg in ["-p", "--pass"]:
            irc.password = sys.argv[i+1].strip("'")
        elif arg in ["-a", "--admin"]:
            irc.admin = sys.argv[i+1].strip("'")
        elif arg in ["-b", "--botnick"]:
            irc.botnick = sys.argv[i+1].strip("'")
except IndexError:
    print "Incorrect use of one of the flags."
    os._exit(0)

# Looking for ini files.

for file in ["desktops.ini", "channels.ini", "hscreens.ini"]:
    if not os.path.isfile("ini/{}".format(file)):
        print "There is no {} file.".format(file)
        os._exit(0)

# Reading the file (if it exists) and displaying information onscreen.

irc.connect(irc.server, 6667)
ini.read_files()
commands.fill_commands()
irc.display_info()
irc.init()
irc.identify()

# Joining predetermined channels.

for channel in var.channels:
    irc.join(channel)

# Main loop. It's tiem.

while True:
    msgList = [msg for msg in irc.ircsock.recv(2048).split('\r\n') if msg]
    
    for message in msgList:
        commands.read(message)
