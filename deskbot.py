import os
import time
import argparse
from modules import ini, irc, handler, yvar
from socket import error as socket_error

os.system("cls" if os.name == "nt" else "clear")
print "Starting deskbot."
var.start_point = time.time()   # Store time when the bot starts.

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

handler.fill_commands()
feed.connect()

# Main loop. It's tiem.
while True:
    for message in feed.s_out():
        handler.read(message)
