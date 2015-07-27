import irc
import var
import tools
from socket import error as socket_error

# This module's variables.
split_line = ""

#######################################################
#    Will connect the bot to the server and deal      #
#    with nickname errors.                            #
#######################################################

def connect ():
    try:
        irc.connect(irc.server, irc.port)
    except socket_error:
        # If the bot can't connect to the server, we get a socket error.
        print("WARNING: Couldn't connect to {}... (Retrying in 15 seconds.)".format(irc.server))
        
        # Make irc.ircsock an object with recv and send methods.
        irc.ircsock = type("socket", (object,), {
            "recv": lambda *_: "",
            "send": lambda *_: ""
        })()
        
        # Wait for 15 seconds before attempting to reconnect.
        time.sleep(15)
        return
    
    # In case the connection to the server is successful...
    
    irc.display_info()
    irc.init()
    
    # In case the nickname throws errors.
    while tools.nick_check() and len(irc.botnick) < 20:
        # Append _ to botnick and try to reconnect.
        irc.botnick += "_"
        irc.nick(irc.botnick)
            
    # Check one last time for nick errors.
    if tools.nick_check():
        print("ERROR: deskbot tried her best, but couldn't get in with any nicknames.")
        raise SystemExit
    else:
        print("WARNING: Using nickname: {}".format(irc.botnick))
    
    print("Joining channels: {}".format(" ".join(var.channels)))
    
    for channel in var.channels:
        irc.join(channel)

#######################################################
#    Will return a list of complete lines received    #
#    by the server.                                   #
#######################################################

def s_out ():
    global split_line
        
    line = irc.ircsock.recv(512)
    s_arr = []
    
    # Check if the connection has been interrupted.
    if len(line) == 0:
        print("ERROR: The bot has been disconnected from the server.")
        print("Attempting to reconnect now...")
        connect()
    
    # Remove leftover '\n' from a not that split line.
    line = line.lstrip("\n")
    
    # Complete CR-LF.
    if line.endswith("\r"):
        line += "\n"
    
    # If there was a split line last time, complete it.
    if split_line:
        s_arr.append(split_line + line.split("\r\n")[0])
        s_arr += line.split("\r\n")[1:-1]
        split_line = ""
    else:
        s_arr += line.split("\r\n")[:-1]
    
    # Check for split lines.
    if not line.endswith("\r\n"):
        split_line = line.split("\r\n")[-1]
        
    return s_arr
