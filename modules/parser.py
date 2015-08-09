import irc

class ServerLine:
    event = ""

def parse (message):
    
    event = message.split(" ")[1]
    s_line = ServerLine()
    s_line.event = event
    
    if event == "JOIN":
        s_line.user = message.split("!")[0][1:]
        try:
            s_line.channel = message.split(" :")[1]
        except IndexError:
            s_line.channel = message.split(" ")[2]
    
    elif event == "PART":
        s_line.user = message.split("!")[0][1:]
        s_line.channel = message.split(" ")[2]
        try:
            s_line.reason = message.split(" :",1)[1]
        except IndexError:
            s_line.reason = ""
    
    elif event == "QUIT":
        s_line.user = message.split("!")[0][1:]
        try:
            s_line.reason = message.split(" :",1)[1]
        except IndexError:
            s_line.reason = ""
    
    elif event == "KICK":
        s_line.user = message.split("!")[0][1:]
        s_line.channel = message.split(" ")[2]
        s_line.target = message.split(" ")[3]
        try:
            s_line.reason = message.split(" :",1)[1]
        except IndexError:
            s_line.reason = ""
    
    elif event == "PRIVMSG":
        s_line.user = message.split("!")[0][1:]
        s_line.target = message.split(" ")[2]
        s_line.message = message.split(" :",1)[1]
    
    elif event == "NOTICE":
        s_line.user = message.split("!")[0][1:]
        s_line.target = message.split(" ")[2]
        s_line.message = message.split(" :",1)[1]
    
    elif event == "INVITE":
        s_line.user = message.split("!")[0][1:]
        s_line.channel = message.split(" :")[1]
        
    elif event == "NICK":
        s_line.user = message.split("!")[0][1:]
        s_line.new_nick = message.split(" :")[1]
    
    elif event == "MODE":
        s_line.user = message.split("!")[0][1:]
        s_line.target = message.split(" ")[2]
        s_line.mode = " ".join(message.split(" ")[3:])
    
    elif event.isdigit():
        s_line.code = int(event)
        s_line.message = message.split(event)[1]
        s_line.event = "NUMREP"
    
    return s_line
