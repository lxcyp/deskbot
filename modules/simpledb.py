import ini, var, irc
from tools import is_identified

# Strings used for specific actions.
mod_strings = ["-s", "-set", "--set"]
del_strings = ["-rm", "-remove", "--remove", "-del", "-delete", "--delete"]

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


# Functions


# Return namespace with functions prepared.
def namespace (string_dictionary, dictionary_name, 
                section_name, filename):
    
    f_namespace = type("namespace", (object,), {})()
    f_namespace.access_function = access_function(
        string_dictionary = string_dictionary,
        dictionary_name   = dictionary_name
    )
    f_namespace.modify_function = mod_function(
        string_dictionary = string_dictionary,
        dictionary_name   = dictionary_name,
        section_name      = section_name,
        filename          = filename
    )
    f_namespace.remove_function = rm_function(
        string_dictionary = string_dictionary,
        dictionary_name   = dictionary_name,
        section_name      = section_name,
        filename          = filename
    )
    
    return f_namespace

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
def access_function (string_dictionary, dictionary_name):
    
    # The function in question.
    def access_db (user, channel, word):
        target = user if len(word) == 1 else word[1]
        
        # Ignore case.
        for nick in string_dictionary:
            if target.lower() == nick.lower():
                target = nick
        
        if target not in string_dictionary:
            err_msg = "You don't" if target == user else "\x0f{} doesn't".format(target)
            irc.msg(channel, "{} have any {} saved.".format(err_msg,
                                dictionary_name))
        else:
            irc.msg(channel, "\x0f{} \x0f[{}]".format(
                        string_dictionary[target], target))
    
    return access_db

# Returns the function to modify an entry in the database.
def mod_function (string_dictionary, dictionary_name, filename, section_name):
    
    # The function in question.
    def mod_entry (user, channel, word):
        data = " ".join(word[2:])
        
        # Ignore case.
        for nick in string_dictionary:
            if user.lower() == nick.lower():
                user = nick
        
        string_dictionary[user] = data
        ini.add_to_ini(section = section_name, option = user, 
                        data = data, filename = filename)
        irc.msg(channel, "{}: Your {} was added successfully.".format(
                        user, dictionary_name))
    
    return mod_entry

# Returns the function to remove an entry from the database.
def rm_function (string_dictionary, dictionary_name, filename, section_name):
    
    # The function in question.
    def rm_entry (user, channel, word):
        # Ignore case.
        for nick in string_dictionary:
            if user.lower() == nick.lower():
                user = nick
        
        if user not in string_dictionary:
            irc.msg(channel, "{}: You have no {} saved.".format(user, dictionary_name))
        else:
            del string_dictionary[user]
            ini.remove_from_ini(section = section_name, option = user,
                                    filename = filename)
            irc.msg(channel, "{}: Your {} was removed successfully.".format(
                            user, dictionary_name))
    
    return rm_entry
