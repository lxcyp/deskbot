import os.path, os
import ConfigParser
import var, irc

# Reading from ini files.

def fill_dict (file, section):
    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    config.read("ini/{}/{}".format(irc.server, file))
    
    rd_dict = {}
    
    if config.has_section(section):
        for option in config.options(section):
            rd_dict[option.replace('~', '[')] = config.get(section, option).split('\n')
    
    return rd_dict

def fill_list (file):
    with open("ini/{}/{}".format(irc.server, file), "a+") as file:
        rd_list = [line.strip() for line in file]
    return rd_list

# Making changes to ini files.

def add_to_ini (section, option, data, path):
    option = option.replace('[', '~')
    path = path if path.startswith("ini/") else "ini/{}/{}".format(irc.server, path)
    
    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    config.read(path)
    
    # Check if the section is valid and if not, create it.
    if not config.has_section(section):
        config.add_section(section)
        
    if data:
        config.set(section, option, data)
    else:
        remove_from_ini(section, option, path)
        return
    
    with open(path, 'wb') as iniFile:
        config.write(iniFile)

def remove_from_ini (section, option, path):
    option = option.replace('[', '~')
    path = path if path.startswith("ini/") else "ini/{}/{}".format(irc.server, path)
    
    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    config.read(path)
    
    try:
        config.remove_option(section, option)
    except:
        print "Not in .ini file."
    
    with open(path, 'wb') as iniFile:
        config.write(iniFile)
