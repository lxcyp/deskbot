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

irc.port = 6667

try:
    for i, arg in enumerate(sys.argv):
        if arg in ["-p", "--pass"]:
            irc.password = sys.argv[i+1].strip("'")
        elif arg in ["-a", "--admin"]:
            irc.admin = sys.argv[i+1].strip("'")
        elif arg in ["-b", "--botnick"]:
            irc.botnick = sys.argv[i+1].strip("'")
	elif arg in ["-o", "--port"]:
            irc.port = int(sys.argv[i+1].strip("'"))

except IndexError:
    print "Incorrect use of one of the flags."
    os._exit(0)

# Creating ini folder for network, if it doesn't exist.
if not os.path.isdir("ini"):
    os.mkdir("ini")
    print "Creating ini folder."
if not os.path.isdir("ini/{}".format(irc.server)):
    os.mkdir("ini/{}".format(irc.server))
    print "Creating ini folder for {}.".format(irc.server)

# Reading the channels and ctcp file.
var.channels = ini.fill_list("channels.ini")
var.ctcp = ini.fill_dict("ctcp.ini", "CTCP")
var.ctcp = {key:var.ctcp[key][0] for key in var.ctcp}

# Filling commands.
commands.fill_commands()

# Connecting and display info.
irc.connect(irc.server, irc.port)
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
