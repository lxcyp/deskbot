import ConfigParser
import var
import irc

# Reading from ini files.

# Return dictionary of option:data.
def fill_dict (filename, section, raw_path = False):
    
    if filename.startswith("ini/") or raw_path:
        filepath = filename
    else:
        filepath = "ini/{}/{}".format(irc.server, filename)
    
    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    config.read(filepath)
    
    rd_dict = {}
    
    if config.has_section(section):
        for option in config.options(section):
            rd_dict[option.replace("~", "[")] = config.get(section, option).split("\n")
    
    return rd_dict

# Return list of lines in a file without "\n" at the end.
def fill_list (filename, raw_path = False):
    
    if filename.startswith("ini/") or raw_path:
        filepath = filename
    else:
        filepath = "ini/{}/{}".format(irc.server, filename)
    
    with open(filepath, "a+") as list_file:
        rd_list = [line.strip() for line in list_file]
    
    return rd_list

# Making changes to ini files.

# Set an option inside a section on a config(ini) file.
def add_to_ini (section, option, data, filename, raw_path = False):
    
    if filename.startswith("ini/") or raw_path:
        filepath = filename
    else:
        filepath = "ini/{}/{}".format(irc.server, filename)
    
    option = option.replace("[", "~")
    
    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    config.read(filepath)
    
    # Check if the section is present and if not, create it.
    if not config.has_section(section):
        config.add_section(section)
    
    if data:
        config.set(section, option, data)
    else:
        remove_from_ini(section, option, filepath, raw_path = raw_path)
        return
    
    with open(filepath, "wb") as ini_file:
        config.write(ini_file)

# Remove option from a config(ini) file.
def remove_from_ini (section, option, filename, raw_path = False):
    
    if filename.startswith("ini/") or raw_path:
        filepath = filename
    else:
        filepath = "ini/{}/{}".format(irc.server, filename)
    
    option = option.replace("[", "~")
    
    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    config.read(filepath)
    
    try:
        config.remove_option(section, option)
    except:
        print "Not in .ini file: [{}] {}".format(section, option)
    
    with open(filepath, "wb") as ini_file:
        config.write(ini_file)

# Add line to a list file.
def add_to_list (line, filename, raw_path = False):
    
    if raw_path or filename.startswith("ini/"):
        filepath = filename
    else:
        filepath = "ini/{}/{}".format(irc.server, filename)
    
    # Write line to file if it isn't already in it.
    with open(filepath, "a+") as list_file:
        if line + "\n" not in list_file.readlines():
            list_file.write(line + "\n")

# Remove line from a list file.
def remove_from_list (line, filename, raw_path = False):
    
    if raw_path or filename.startswith("ini/"):
        filepath = filename
    else:
        filepath = "ini/{}/{}".format(irc.server, filename)
    
    with open(filepath, "r+") as list_file:
        
        # List every line in the file and return to the beginning.
        lines = list_file.readlines()
        list_file.seek(0)
        
        # Write everything on the file except line.
        for curr_line in lines:
            if curr_line != (line + "\n"):
                list_file.write(curr_line)
        
        list_file.truncate()
