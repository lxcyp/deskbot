import os
import sys
import argparse
import time
from modules import ini, irc, commands, var, tools
from socket import error as socket_error

os.system("cls" if os.name == "nt" else "clear")
print "Starting deskbot."

parser = argparse.ArgumentParser()
parser.add_argument("server", help="Server address to connect the bot to.")
parser.add_argument("-p", "--port", default=6667, type=int,
                    help="Port through which the bot will connect to the server.")
parser.add_argument("-b", "--botnick", default="deskbot",
                    help="Nickname the bot will use on IRC.")
parser.add_argument("-a", "--admin", help="Nickname of the admin(supposed to be you).")
parser.add_argument("-P", "--password",
                    help="NickServ password, if the bot needs authentication.")
args = parser.parse_args()

# Grabbing arguments given.
irc.server = args.server
irc.password = args.password
irc.admin = args.admin if args.admin else raw_input("Please choose an admin nickname: ")
irc.botnick = args.botnick
irc.port = args.port

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
def connect ():
    try:
        irc.connect(irc.server, irc.port)
    except socket_error:
        print "Couldn't connect to {}... (Retrying in 15 seconds.)".format(irc.server)
        
        # Make irc.ircsock an object with a recv() function.
        irc.ircsock = type("socket", (object,), {
            "recv": lambda *x: ""
        })()
        
        # Wait for 15 seconds before attempting to reconnect.
        time.sleep(15)
        return
    
    irc.display_info()
    irc.init()
    
    # In case there was an error during initial info exchange.
    if tools.nick_check():
        # Append _ to botnick and try to reconnect.
        irc.nick(irc.botnick + "_")
        
        # Checking for an error again.
        if tools.nick_check():
            irc.quit()
            print "Probably erroneous nickname. ({}_ didn't work.)".format(irc.botnick)
            raise SystemExit
        else:
            irc.botnick += "_"
            print "Nick was already in use. Using {} now.".format(irc.botnick)

irc.display_info()
connect()

# Joining predetermined channels.
for channel in var.channels:
    irc.join(channel)

# Main loop. It's tiem.
while True:
    line = irc.ircsock.recv(512)
    
    # Check if the connection has been interrupted.
    if len(line) == 0:
        print "The bot has been disconnected from the server."
        print "Attempting to reconnect now..."
        connect()
    
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
