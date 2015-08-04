#!/usr/bin/env python

import os
import time
import argparse
from modules import ini, irc, var
from modules import handler, feed
from modules import settings

os.system("cls" if os.name == "nt" else "clear")
print("Starting deskbot.")
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
parser.add_argument("-t", "--timeout",
                    help="Ping timeout in seconds, default is 240 seconds.")
parser.add_argument("--log", action="store_true",
                    help="Save lines in log/server-address.log.")
parser.add_argument("--log-file",
                    help="Set a file on which the bot will save logs.")
args = parser.parse_args()

# Grabbing arguments given.
var.log = args.log
var.logfile = args.log_file
irc.server = args.server
irc.password = args.password
irc.botnick = args.botnick
irc.port = args.port
irc.admin = args.admin
irc.timeout = args.timeout if args.timeout > 0 else 240

# Require an admin nickname to go on.
while not irc.admin:
    irc.admin = raw_input("Please choose an admin nickname: ")

# Creating ini folder for network, if it doesn't exist.
if not os.path.isdir("ini"):
    os.mkdir("ini")
    print("Created ini folder.")
if not os.path.isdir("log"):
    os.mkdir("log")
    print("Created log folder.")
if not os.path.isdir("ini/{}".format(irc.server)):
    os.mkdir("ini/{}".format(irc.server))
    print("Created ini folder for {}.".format(irc.server))

# Reading the channels, ignored, ctcp and settings files.
var.channels = ini.fill_list("channels.ini")
var.ignored  = ini.fill_list("ignored.ini")
var.ctcp     = settings.ctcp()
var.settings = settings.settings()

handler.fill_commands()
feed.connect()

# Main loop. It's tiem.
while True:
    for message in feed.s_out():
        handler.read(message)
