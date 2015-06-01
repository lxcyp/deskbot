import ini, var, irc
from tools import is_identified, is_number
from tools import trim, nsfw_check

# URL database command usage. Gets passed to command module
# to fill the command dictionary with their respective usage.
command_usage = [
    "{} - See your {n} list.",
    "{} n - See nth {n} in your list.",
    "{} user - See user's {n} list.",
    "{} user n - See user's nth {n}.",
    " ",
    "{} -add url1 url2 ... - Add a list of urls to your {n} list.",
    "You can also use \x034-a\x0f instead of \x034-add\x0f.",
    " ",
    "{} -remove n1,n2,... - Remove a list of indexes from your list.",
    "You can also use \x034-rm\x0f instead of \x034-remove\x0f.",
    "{} -rm * will remove all of your saved {n}s.",
    " ",
    "{} -replace n url - Replace your nth {n} with url.",
    "You can also use \x034-re\x0f instead of \x034-replace\x0f."
]

# Syntax for providing help.
syntax = {
    ("-a", "-add", "--add"):"{} {} url1 url2 ...",
    ("-rm", "-remove", "--remove"):"{} {} n1,n2 n3 ...",
    ("-re", "-replace", "--replace"):"{} {} n url"
}

# Functions

# User-URL database can only be altered by identified users.
def ident (f):
    def check (user, channel, word):
        try:
            if word[1] in [
                "-a", "-add", "--add",
                "-rm", "-remove", "--remove",
                "-re", "-replace", "--replace"
            ] and not is_identified(user):
                irc.msg(channel, "{}: Identify with NickServ first.".format(user))
            else:
                f(user, channel, word)
        except IndexError:
            f(user, channel, word)
    return check

# Returns the function we'll need for the URL database listing command.
def list_function (url_dict, dict_name):
    
    # Responsible for listing URLs. Can accept username and/or a number as parameter.
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
        
        # Check if it's a URL or a number.
        if target.startswith("http://") or target.startswith("https://"):
            irc.msg(channel, "Did you mean to use -a {}?".format(target))
            return
        elif number and target.isdigit():
            irc.msg(channel, "Did you mean to use -re {} {}?".format(target, number))
            return
        
        # Check if a flag was misused.
        if target.startswith("-"):
            
            # Grab tuple containing flag.
            commands = ()
            for flags in syntax:
                if target in flags:
                    commands = flags
                    break
            
            if commands in syntax:
                line = syntax[commands].format(word[0], target)
                irc.msg(channel, "Syntax for {}: {}".format(target, line))
            else:
                irc.msg(channel, "{}: Unknown command.".format(user))
            
            return
        
        for nick in url_dict:
            if target.lower() == nick.lower():
                target = nick
                break
        
        # Throw a message if the target isn't in the URL database.
        if target not in url_dict:
            err_msg = "You don't" if target == user else "{} doesn't".format(target)
            irc.msg(channel, "{} have any {} saved.".format(err_msg, dict_name))
            return
        
        # Check if the received number is a valid integer.
        if (not is_number(number)) or ((int(number) if number else 1) < 1):
            irc.msg(channel, "{}: Invalid number.".format(user))
            return
            
        if number:
            # Turning number into a numeric value.
            number = int(number) - 1
            
            if number >= len(url_dict[target]):
                err_msg = "You don't" if target == user else "{} doesn't".format(target)
                irc.msg(channel, "{} have that many {}.".format(err_msg, dict_name))
            else:
                line = "[{}] ".format("\x034NSFW\x0f" if "!" in url_dict[target][number] else number+1)
                line += "{} [{}]".format(url_dict[target][number].strip("!"), target)
                irc.msg(channel, line)
        else:
            url_list = ["[{}] {}".format(ind+1, url) for ind, url in enumerate(url_dict[target])]
            
            # Looking for NSFW URLs. (as indicated by '!')
            url_list = map(nsfw_check, url_list)
            
            line = " ".join(url_list) + " [{}]".format(target)
            irc.msg(channel, line)
    
    return list_urls

# Return the add_url function. Can receive a different max number.
def add_function (url_dict, dict_name, filename, sect_name, *args):
    
    # This is the max number of URLs to save.
    max = args[0] if args and args[0] > 0 else 5
    
    # Add a list of URLs to the database. Will require NickServ authentication.
    def add_url (user, channel, word):
        a_list = [url for url in word[2:] if url.startswith("http://") or url.startswith("https://")]
        
        if not a_list:
            irc.msg(channel, "{}: Links have to start with \"http://\" or \"https://\".".format(user))
            return
        
        for nick in url_dict:
            if user.lower() == nick.lower():
                user = nick
                break
        
        # Create an empty list for a new user.
        if user not in url_dict:
            url_dict[user] = []
        
        # Or check if existing user already has max URLs saved.
        elif len(url_dict[user]) == max:
            irc.msg(channel, "{}: You already have {} {} saved.".format(user, max, dict_name))
            return
        
        # Fill saved list until it reaches max URLs.
        for url in a_list:
            if len(url_dict[user]) < max:
                url_dict[user].append(trim(url))
            else:
                break
        
        ini.add_to_ini(sect_name, user, '\n'.join(url_dict[user]), filename)
        irc.msg(channel, "{}: {} added.".format(user, sect_name))
    
    return add_url

# Returns the delete function.
def delete_function (url_dict, dict_name, filename, sect_name):

    # Removes URLs from the user's list. Will require NickServ authentication.
    def delete_url (user, channel, word):
        del_list = [int(x) - 1 for x in word[2].split(',') if (is_number(x) and int(x) > 0)]
        del_list += [int(x) - 1 for x in word[2:] if (is_number(x) and int(x) > 0)]
        
        for nick in url_dict:
            if user.lower() == nick.lower():
                user = nick
                break
        
        # Wildcard removes everything saved for that user from the database.
        if word[2] == "*" and user in url_dict:
            del url_dict[user]
            ini.remove_from_ini(sect_name, user, filename)
            irc.msg(channel, "{}: All of your {} were removed successfully.".format(user, dict_name))
            return
        
        # The list only needs numbers.
        if not del_list:
            irc.msg(channel, "{}: Invalid number(s).".format(user))
            return
        
        # The user must be in the database to be able to remove URLs.
        if user not in url_dict:
            irc.msg(channel, "{}: You don't have any {} saved.".format(user, dict_name))
            return
        
        # Copy contents of indexed list in database to deletion list.
        for index, number in enumerate(del_list):
            if len(url_dict[user]) > number:
                del_list[index] = url_dict[user][number]
        
        # Proceed to remove them one by one.
        for entry in del_list:
            if entry in url_dict[user]:
                url_dict[user].remove(entry)
        
        # Delete entry in database for an empty list and remove user from ini file.
        if not url_dict[user]:
            del url_dict[user]
            ini.remove_from_ini(sect_name, user, filename)
            irc.msg(channel, "{}: All of your {} were removed successfully.".format(user, dict_name))
            return
        
        ini.add_to_ini(sect_name, user, '\n'.join(url_dict[user]), filename)
        irc.msg(channel, "{}: {} deleted.".format(user, sect_name))
    
    return delete_url

# Return the replace function for the URL database command.
# Can also accept a different max number.
def replace_function (url_dict, dict_name, filename, sect_name, *args):
    
    # This is the max number of URLs to save.
    max = args[0] if args and args[0] > 0 else 5
    
    # Replace a URL in the user's list. Will require NickServ authentication.
    def replace_url (user, channel, word):
        
        # This command receives two pieces of information.
        if len(word) < 4:
            irc.msg(channel, "{}: Wrong syntax. Check .help".format(user))
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
        
        # Check if it's in the max range, and no negative indexes will be accepted.
        if number > max-1 or number < 0:
            irc.msg(channel, "{}: Invalid number.".format(user))
            return
        
        # Ignore case.
        for nick in url_dict:
            if user.lower() == nick.lower():
                user = nick
                break
        
        # Try to replace URL using received number.
        try:
            url_dict[user][number] = trim(word[3])
            ini.add_to_ini(sect_name, user, '\n'.join(url_dict[user]), filename)
            irc.msg(channel, "{}: {} replaced.".format(user, sect_name.rstrip("s")))
        
        # It might not work, if the list isn't long enough.
        except IndexError:
            irc.msg(channel, "{}: Invalid number.".format(user))
        # And it won't work if the user isn't in the URL database.
        except KeyError:
            irc.msg(channel, "{}: You don't have any {} saved.".format(user, dict_name))
    
    return replace_url
