import socket, time, os

ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = ""
botnick = "deskbot"         # Default bot nick.
password = ""               # Default NickServ password.
admin = "spoonm"            # Default admin nickname.

def display_info ():
    print "Nickname: {}".format(botnick)
    print "Password: {}".format(password)
    print "Admin: {}".format(admin)
    print "\nServer: {}".format(server)
    time.sleep(1)

def connect (server, port):
    ircsock.connect((server, port))

def pong (ping):
    ircsock.send("PONG :{}\n".format(ping))

def init ():
    ircsock.send("USER {} {} {} :I am {}'s bot.\n".format(botnick, botnick, botnick, admin))
    ircsock.send("NICK {}\n".format(botnick))
    time.sleep(2)

def nick (username):
    global botnick
    ircsock.send("NICK :{}\r\n".format(username))
    botnick = username

def identify ():
    ircsock.send("PRIVMSG NickServ :IDENTIFY {}\r\n".format(password))
    print("Trying to identify with NickServ.")
    time.sleep(1)

def msg (target, string):
    ircsock.send("PRIVMSG {} :{}\r\n".format(target, string))

def notice (target, string):
    ircsock.send("NOTICE {} :{}\r\n".format(target, string))

def join (target):
    ircsock.send("JOIN {}\r\n".format(target))
    time.sleep(0.5)

def part (target, message):
    ircsock.send("PART {} :{}\r\n".format(target, message))

def quit (reason):
    ircsock.send("QUIT :{}\r\n".format(reason))
    os._exit(0)

def kick (channel, target, reason):
    ircsock.send("KICK {} {} :{}\r\n".format(channel, target, reason))

def ban (channel, target, reason):
    ircsock.send("MODE {} +b {} :{}\r\n".format(channel, target, reason))

def mode (target, target_channel, mode):
    ircsock.send("MODE {} {} {}\r\n".format(target_channel, mode, target))
