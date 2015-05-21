import os.path, os
import ConfigParser
import var

def read_files ():
    var.desktops = fill_dict("desktops.ini", "Desktops")
    var.hscreens = fill_dict("hscreens.ini", "Homescreens")
    var.channels = fill_list("channels.ini")

# Reading from ini files.

def fill_dict (path, section):
    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    config.read("ini/" + path)
    
    dict = {}
    
    if config.has_section(section):
        for option in config.options(section):
            dict[option.replace('~', '[')] = config.get(section, option).split('\n')
    
    return dict

def fill_list (path):
    with open("ini/{}".format(path)) as file:
        list = [line.strip() for line in file]
    return list

# Making changes to ini files.

def add_to_ini (section, option, data, path):
    option = option.replace('[', '~')
    path = path if path.startswith("ini/") else "ini/{}".format(path)
    
    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    config.read(path)
    
    if config.has_section(section):
        if data:
            config.set(section, option, data)
        else:
            remove_from_ini(section, option, path)
            return
    else:
        print "Wrong section used."
        os._exit(0)
    
    with open(path, 'wb') as iniFile:
        config.write(iniFile)

def remove_from_ini (section, option, path):
    option = option.replace('[', '~')
    path = path if path.startswith("ini/") else "ini/{}".format(path)
    
    config = ConfigParser.RawConfigParser()
    config.optionxform = str
    config.read(path)
    
    try:
        config.remove_option(section, option)
    except:
        print "Not in .ini file."
    
    with open(path, 'wb') as iniFile:
        config.write(iniFile)
