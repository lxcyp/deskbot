from .. import irc, var
from ..tools import ctcp_req

# Fill commands dictionary.
def ins_command ():
    var.commands["version"] = type("command", (object,), {})()
    var.commands["version"].method = version
    var.commands["version"].aliases = [".version", ".ver"]
    var.commands["version"].usage = [
        "{} - Display your version CTCP reply.",
        "{} user - Display user's version CTCP reply."
    ]

# Command method.
def version (user, channel, word):
    if len(word) == 1:
        target = user
    else:
        target = word[1]
    
    # Make the request.
    ver = ctcp_req(target, "VERSION")
    
    # Only show a message if a reply is received.
    if ver:
        irc.msg(channel, "{} [{}]".format(ver, target))
