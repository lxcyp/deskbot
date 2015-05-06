import ConfigParser, os.path, os
import var

def readFile ():
    
    var.desktops = Fill().fillDict("ini/desktops.ini", "Desktops")

class Fill:

    def fillDict (self, path, section):
        
        config = ConfigParser.RawConfigParser()
        config.optionxform = str
        config.read(path)
        
        dict = {}
        
        if config.has_section(section):
            for option in config.options(section):
                dict[option.replace('~', '[')] = config.get(section, option).split('\n')
        
        return dict

class Change:
    
    def addToIni (self, section, option, data, path):
        
        path = "ini/{}".format(path)
        option = option.replace('[', '~')
        
        config = ConfigParser.RawConfigParser()
        config.optionxform = str
        config.read(path)
        
        if config.has_section(section):
            if data:
                config.set(section, option, data)
            else:
                self.removeFromIni(section, option, path)
        else:
            print "Wrong section used."
            os._exit(0)
        
        with open(path, 'wb') as configfile:
            config.write(configfile)
            
    def removeFromIni (self, section, option, path):
        
        path = "ini/{}".format(path)
        option = option.replace('[', '~')
        
        config = ConfigParser.RawConfigParser()
        config.optionxform = str
        config.read(path)
        
        try:
            config.remove_option(section, option)
        except:
            print "Not in .ini file."
        
        with open(path, 'wb') as configfile:
            config.write(configfile)
