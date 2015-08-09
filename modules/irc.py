import socket
import time
import hlfilter

ircsock = None

server   = ""
botnick  = "deskbot"        # Default bot nick.
password = ""               # Default NickServ password.
admin    = ""               # Default admin nickname.
port     = 6667             # Default server port.
timeout  = 240              # Default ping timeout.

def display_info ():
    print("Nickname:    {}".format(botnick))
    print("Password:    {}".format(password))
    print("Admin:       {}".format(admin))
    print("Server:      {}".format(server))
    print("Port:        {}".format(port))
    time.sleep(1)

def connect (server, port):
    global ircsock
    print("\nAttempting to connect to server using this data...")
    ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ircsock.connect((server, port))

def pong (ping):
    ircsock.send("PONG :{}\n".format(ping))

def init ():
    ircsock.send("USER {} {} {} :I am {}'s bot.\n".format(botnick, botnick, botnick, admin))
    ircsock.send("NICK {}\n".format(botnick))
    time.sleep(2)

def nick (username):
    ircsock.send("NICK :{}\r\n".format(username))

def identify ():
    ircsock.send("PRIVMSG NickServ :IDENTIFY {}\r\n".format(password))
    print("\nTrying to identify with NickServ.\n")
    time.sleep(1)

def msg (target, string, raw = False):
    if not raw:
        string = hlfilter.filter(string)
    
    line = "PRIVMSG {} :{}".format(target, string)
    
    # Lines that make more than 1.2 messages are just mean.
    if len(line) > (612 - 2*len("PRIVMSG {} :".format(target))):
        ircsock.send("PRIVMSG {} :<text was too long>\r\n".format(target))
    elif len(line) > 510:
        ircsock.send(line[:511] + "\r\n")
        msg(target, line[512:])
    else:
        ircsock.send(line + "\r\n")
    
    print("{} -> PRIVMSG {} -> {}".format(botnick, target, string))

def notice (target, string):
    ircsock.send("NOTICE {} :{}\r\n".format(target, string))
    print("{} -> NOTICE {} -> {}".format(botnick, target, string))

def join (target):
    ircsock.send("JOIN {}\r\n".format(target))
    time.sleep(0.5)

def part (target, message):
    ircsock.send("PART {} :{}\r\n".format(target, message))

def quit (reason):
    ircsock.send("QUIT :{}\r\n".format(reason))

def kick (channel, target, reason):
    ircsock.send("KICK {} {} :{}\r\n".format(channel, target, reason))

def ban (channel, target, reason):
    ircsock.send("MODE {} +b {} :{}\r\n".format(channel, target, reason))

def mode (channel, target, mode):
    ircsock.send("MODE {} {} {}\r\n".format(channel, mode, target))
