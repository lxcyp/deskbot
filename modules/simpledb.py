import ini, var, irc
from tools import is_identified

"""
Stores strings on given key in given dictionary.
Is done this way so there is absolutely no need to rewrite it ever again.

Doesn't necessarily need a user to be a key.
"""

# Simple database command usage. Fills the command's entry in .help.
command_usage = [
    "{} - Check your {n} entry.",
    "{} user - Check user's {n} entry.",
    " ",
    "{} -set content - Set your {n} entry as content.",
    "You can also use \x034-s\x0f.",
    " ",
    "{} -rm - Remove your {n} entry.",
    "You can also use \x034-remove\x0f."
]

# This kind of command requires NickServ authentication.
def ident (f):
    def check (user, channel, word):
        try:
            if word[1] in [] and not is_identified(user):
                irc.msg(channel, "{}: Identify with NickServ first.".format(user))
            else:
                f(user, channel, word)
        except IndexError:
            f(user, channel, word)
    return check

# Returns the function to access keys.
def access_function (str_dict, dict_name):
    
    # The function in question.
    def access_db (user, channel, word):
        target = user if len(word) == 1 else word[1]
        
        # Ignore case.
        for nick in str_dict:
            if target.lower() == nick.lower():
                target = nick
        
        if target not in str_dict:
            err_msg = "You don't" if target == user else "\x0f{} doesn't".format(target)
            irc.msg(channel, "{} have any {} saved.".format(err_msg, dict_name))
        else:
            irc.msg(channel, "\x0f{} \x0f[{}]".format(str_dict[target], target))
    
    return access_db

# Returns the function to modify an entry in the database.
def mod_function (str_dict, dict_name, filename, section):
    
    # The function in question.
    def mod_entry (user, channel, word):
        data = " ".join(word[2:])
        
        # Ignore case.
        for nick in str_dict:
            if user.lower() == nick.lower():
                user = nick
        
        str_dict[user] = data
        ini.add_to_ini(section, user, data, filename)
        irc.msg(channel, "{}: Your {} was added successfully.".format(user, dict_name))
    
    return mod_entry

# Returns the function to remove an entry from the database.
def rm_function (str_dict, dict_name, filename, section):
    
    # The function in question.
    def rm_entry (user, channel, word):
        # Ignore case.
        for nick in str_dict:
            if user.lower() == nick.lower():
                user = nick
        
        if user not in str_dict:
            irc.msg(channel, "{}: You have no {} saved.".format(user, dict_name))
        else:
            del str_dict[user]
            ini.remove_from_ini(section, user, filename)
            irc.msg(channel, "{}: Your {} was removed successfully.".format(user, dict_name))
    
    return rm_entry