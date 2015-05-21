from .. import irc, var

# Call needed function.
def read (user, channel, word):
    if len(word) == 1:
        list_commands(user)
    elif len(word) >= 2:
        command_help(user, word[1])

# List available commands.
def list_commands (user):
    line = "Available commands: " + " ".join(var.commands.keys())
    irc.notice(user, line)

# Show certain command usage.
def command_help (user, command):
    dict = {}
    
    # Fill dictionary of aliases. Link them to the command name.
    for cmd in var.commands:
        for alias in var.commands[cmd]["aliases"]:
            dict[alias] = cmd
    
    if command not in dict:
        irc.notice(user, "No usage info for {} available.".format(command))
    else:
        aliases = [alias for alias in dict if dict[alias] == dict[command]]
        usage = var.commands[dict[command]]["usage"]
        
        irc.notice(user, "Command aliases: " + " ".join(aliases))
        irc.notice(user, "Usage:")
        
        for line in usage:
            irc.notice(user, line.format(command))
