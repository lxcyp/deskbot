from .. import irc, var, ini
from ..tools import is_identified

# Only the admin can use these commands.
def ident (f):
    def check (user, channel, word):
        if user == irc.admin and is_identified(user):
            f(user, channel, word)
        else:
            irc.msg(channel, "{}: You don't have admin rights.".format(user))
    return check

# Fill commands dictionary.
def ins_command ():
    var.commands["set"] = type("command", (object,), {})()
    var.commands["set"].method = read
    var.commands["set"].aliases = [".set"]
    var.commands["set"].usage = [
        "{} property value - Change property value.",
        "{} del property - Delete property."
    ]

# Command method.
def read (user, channel, word):
    # This command always accepts two pieces of information.
    if len(word) < 3:
        irc.msg(channel, "{}: Wrong syntax. Check .help".format(user))
        return
    
    property = word[1]
    value = " ".join(word[2:])
    
    if property == "del":
        property = word[2]
        
        # Check if the property is set.
        if property not in var.settings:
            irc.msg(channel, "{}: {} doesn't exist.".format(user, property))
        else:
            del var.settings[property]
            ini.remove_from_ini("Settings", property, "settings.ini")
            irc.msg(channel, "{}: {} removed.".format(user, property))
    else:
        value = True if value == "true" else False if value == "false" else value
        var.settings[property] = value
        ini.add_to_ini("Settings", property, value, "settings.ini")
        irc.msg(channel, "{}: {} property set to {}.".format(user, property, value))
