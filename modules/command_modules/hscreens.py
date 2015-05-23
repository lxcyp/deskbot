from .. import ini, var, irc
from ..tools import is_identified, is_number
from ..tools import trim, nsfw_check

# Fill command dictionary.
def ins_command ():
    var.commands["hscreen"] = type("command", (object,), {})()
    var.commands["hscreen"].method = read
    var.commands["hscreen"].aliases = [
        ".hscreen",
        ".hscr",
        ".homescreen"
    ]
    var.commands["hscreen"].usage = [
        "{} - See your homescreen list.",
        "{} n - See nth homescreen in your list.",
        "{} user - See user's homescreen list.",
        "{} user n - See user's nth homescreen.",
        " ",
        "{} -add url1 url2 ... - Add a list of urls to your homescreen list.",
        "You can also use -a instead of -add.",
        " ",
        "{} -remove n1,n2,... - Remove a list of indexes from your list.",
        "You can also use -rm instead of -remove.",
        "{} -rm * will remove all of your saved homescreens.",
        " ",
        "{} -replace n url - Replace your nth homescreen with url.",
        "You can also use -re instead of -replace."
    ]

# This command will need NickServ auth sometimes.
def ident (f):
    def check (user, channel, word):
        try:
            if word[1] in [
                "-a", "-add",
                "-rm", "-remove",
                "-re", "-replace"
            ] and not is_identified(user):
                irc.msg(channel, "{}: Identify with NickServ first.".format(user))
            else:
                f(user, channel, word)
        except IndexError:
            f(user, channel, word)
    return check

# Parsing the content received.
def read (user, channel, word):
    
    if len(word) < 3:
        list_urls(user, channel, word)
    elif word[1] in ["-a", "-add"]:
        add_url(user, channel, word)
    elif word[1] in ["-rm", "--rm"]:
        delete_url(user, channel, word)
    elif word[1] in ["-re", "-replace"]:
        replace_url(user, channel, word)
    else:
        list_urls(user, channel, word)

# List saved homescreens. Can accept username and/or a number as parameter.
def list_urls (user, channel, word):
    target, number = False, False
    
    if len(word) == 1:
        target = user
    elif len(word) == 2:
        target = word[1] if not is_number(word[1]) else user
        number = word[1] if is_number(word[1]) else False
    elif len(word) >= 3:
        target = word[1]
        number = word[2]
    
    for nick in var.hscreens:
        if target.lower() == nick.lower():
            target = nick
    
    # Throw a message if the target isn't in the homescreen database.
    if target not in var.hscreens:
        err_msg = "You don't" if target == user else "{} doesn't".format(target)
        irc.msg(channel, "{} have any homescreens saved.".format(err_msg))
        return
    
    # Check if the received number is a valid integer.
    if (not is_number(number)) or ((int(number) if number else 1) < 1):
        irc.msg(channel, "{}: Invalid number.".format(user))
        return
        
    if number:
        # Turning number into a numeric value.
        number = int(number) - 1
        
        if number >= len(var.hscreens[target]):
            err_msg = "You don't" if target == user else "{} doesn't".format(target)
            irc.msg(channel, "{} have that many homescreens.".format(err_msg))
        else:
            line = "[{}] ".format("\x034NSFW\x0f" if "!" in var.hscreens[target][number] else number+1)
            line += "{} [{}]".format(var.hscreens[target][number].strip("!"), target)
            irc.msg(channel, line)
    else:
        url_list = ["[{}] {}".format(ind+1, url) for ind, url in enumerate(var.hscreens[target])]
        
        # Looking for NSFW URLs. (as indicated by '!')
        url_list = map(nsfw_check, url_list)
        
        line = ' '.join(url_list) + " [{}]".format(target)
        irc.msg(channel, line)

# Add a list of homescreens to the saved ones. Will require NickServ authentication.
def add_url (user, channel, word):
    a_list = [url for url in word[2:] if url.startswith("http://") or url.startswith("https://")]
    
    if not a_list:
        irc.msg(channel, "{}: Links have to start with \"http://\" or \"https://\".".format(user))
        return
    
    for nick in var.hscreens:
        if user.lower() == nick.lower():
            user = nick
    
    # Create an empty list for a new user.
    if user not in var.hscreens:
        var.hscreens[user] = []
    
    # Or check if existing user already has 5 homescreens saved.
    elif len(var.hscreens[user]) == 5:
        irc.msg(channel, "{}: You already have 5 homescreens saved.".format(user))
        return
    
    # Fill saved list until it reaches 5 homescreens.
    for url in a_list:
        if len(var.hscreens[user]) < 5:
            var.hscreens[user].append(trim(url))
        else:
            break
    
    ini.add_to_ini("Homescreens", user, '\n'.join(var.hscreens[user]), "hscreens.ini")
    irc.msg(channel, "{}: Homescreen(s) added.".format(user))

# Removes homescreens from the user's list. Will require NickServ authentication.
def delete_url (user, channel, word):
    del_list = [int(x) - 1 for x in word[2].split(',') if (is_number(x) and int(x) > 0)]
    
    # Wildcard removes everything saved for that user from the database.
    if word[2] == "*" and user in var.hscreens:
        del var.hscreens[user]
        ini.remove_from_ini("Homescreens", user, "hscreens.ini")
        irc.msg(channel, "{}: All of your homescreens were removed successfully.".format(user))
        return
    
    # The list only needs numbers.
    if not del_list:
        irc.msg(channel, "{}: Invalid number(s).".format(user))
        return
    
    # The user must be in the database to be able to remove homescreens.
    if user not in var.hscreens:
        irc.msg(channel, "{}: You don't have any homescreens saved.".format(user))
        return
    
    # Copy contents of indexed list in database to deletion list.
    for index, number in enumerate(del_list):
        if len(var.hscreens[user]) > number:
            del_list[index] = var.hscreens[user][number]
    
    # Proceed to remove them one by one.
    for entry in del_list:
        if entry in var.hscreens[user]:
            var.hscreens[user].remove(entry)
    
    # Delete entry in database for empty list.
    if not var.hscreens[user]:
        del var.hscreens[user]
        ini.remove_from_ini("Homescreens", user, "hscreens.ini")
        irc.msg(channel, "{}: All of your homescreens were removed successfully.".format(user))
        return
    
    ini.add_to_ini("Homescreens", user, '\n'.join(var.hscreens[user]), "hscreens.ini")
    irc.msg(channel, "{}: Homescreen(s) deleted.".format(user))

# Replace a homescreen in the user's list. Will require NickServ authentication.
def replace_url (user, channel, word):
    
    # This command receives two pieces of information.
    if len(word) < 4:
        irc.msg(channel, "{}: Wrong syntax. Check .help .hscreen".format(user))
        return
    
    # The first must be a number.
    if not is_number(word[2]):
        irc.msg(channel, "{}: Invalid number.".format(user))
        return
    
    # The second must be a URL.
    if not (word[3].startswith("http://") or word[3].startswith("https://")):
        irc.msg(channel, "{}: Invalid URL.".format(user))
        return
    
    # Turn it into a numeric value.
    number = int(word[2]) - 1
    
    # The list only goes up to 5 elements, and no negative indexes will be accepted.
    if number > 4 or number < 0:
        irc.msg(channel, "{}: Invalid number.".format(user))
        return
    
    # Try to replace homescreen using received number.
    try:
        var.hscreens[user][number] = trim(word[3])
        ini.add_to_ini("Homescreens", user, '\n'.join(var.hscreens[user]), "hscreens.ini")
        irc.msg(channel, "{}: Homescreen replaced.".format(user))
    
    # It might not work, if the list isn't long enough.
    except IndexError:
        irc.msg(channel, "{}: Invalid number.".format(user))
