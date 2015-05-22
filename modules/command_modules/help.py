from .. import irc, var

# Fill commands dictionary.
def ins_command ():
    var.commands["help"] = type("command", (object,), {})()
    var.commands["help"].method = read
    var.commands["help"].aliases = [
        ".help",
        "!help",
    ]
    var.commands["help"].usage = [
        "{} - Display list of commands.",
        "{} .command - Get additional help for that command."
    ]

# Call needed function.
def read (user, channel, word):
    if len(word) == 1:
        list_commands(user)
    elif len(word) >= 2:
        command_help(user, word[1])

# List available commands.
def list_commands (user):
    line = "Available commands: " + " ".join(["." + cmd for cmd in var.commands.keys()])
    irc.notice(user, line)

# Show certain command usage.
def command_help (user, command):
    alias_dict = {}
    
    # Fill dictionary of aliases. Link them to the command name.
    for cmd_name in var.commands:
        for alias in var.commands[cmd_name].aliases:
            alias_dict[alias] = cmd_name
    
    if command not in alias_dict:
        irc.notice(user, "No usage info for {} available.".format(command))
    else:
        aliases = var.commands[alias_dict[command]].aliases
        usage = var.commands[alias_dict[command]].usage
        
        irc.notice(user, "Command aliases: " + " ".join(aliases))
        irc.notice(user, "Usage:")
        
        for line in usage:
            irc.notice(user, line.format(command))
