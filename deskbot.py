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

# Reading the channels, ignored, ctcp and settings files.
var.channels = ini.fill_list("channels.ini")
var.ignored = ini.fill_list("ignored.ini")
var.ctcp = ini.fill_dict("ctcp.ini", "CTCP")
var.ctcp = {key:var.ctcp[key][0] for key in var.ctcp}
var.settings = ini.fill_dict("settings.ini", "Settings")
var.settings = {
    key:
        True if var.settings[key][0] == "true"
        else False if var.settings[key][0] == "false"
        else var.settings[key][0]
    for key in var.settings
}

# Filling commands.
commands.fill_commands()

# Connecting and display info.
irc.connect(irc.server, irc.port)
irc.display_info()
irc.init()

# Joining predetermined channels.
for channel in var.channels:
    irc.join(channel)

# Main loop. It's tiem.
while True:
    line = irc.ircsock.recv(512)
    
    # Securi-tea...? Iunno, I'm trying to avoid timing attacks.
    
    # If there was a split line last time, append to it.
    if commands.split_line:
        commands.split_line += line.split("\r\n")[0]            # Complete the split line.
        line = "\r\n".join(line.split("\r\n")[1:]) + "\r\n"     # Remove it from line.
        commands.read(commands.split_line, "")                  # Read split line.
    
    # Check for split lines.
    if not (line.endswith("\r\n") or line.endswith("\r")):
        commands.split_line = line.split("\r\n")[-1]            # Store beginning of split line.
        line = "\r\n".join(line.split("\r\n")[:-1])             # Remove it from line.
    
    if line.endswith("\r"):
        line = line.rstrip("\r")
    
    if line.startswith("\n"):
        line = line.lstrip("\n")
    
    msg_list = [message for message in line.split('\r\n') if message]
    
    # Read messages.
    for message in msg_list:
        commands.read(message)
