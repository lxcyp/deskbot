import re
import var

re_m = re.compile("[a-zA-Z\[\]\\`_\^\{\|\}][a-zA-Z0-9\[\]\\`_\^\{\|\}]+")

def filter (string):
    
    # Check for nicknames in the string.
    matches = re_m.findall(string)
    
    # Check for hlignore'd nicknames in the string.
    for nick in matches:
        if nick.lower() in var.data["hlignore"]:
            string = string.replace(nick, "[{}]".format(nick))
    
    return string
