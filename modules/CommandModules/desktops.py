from .. import ini, var, irc

config = ini.Change()

def is_number (n):
    try:
        int(n)
        return True
    except:
        return False

class Desktops ():
    
    def __init__ (self, user, channel, word):
        
        if len(word) < 3:
            self.list(user, channel, word)
        elif word[1] in ['-a', '-add', '--add']:
            self.add(user, channel, word)
        elif word[1] in ['-rm', '--rm', '--remove']:
            self.delete(user, channel, word)
        elif word[1] in ['-re', '-replace', '--replace']:
            self.replace(user, channel, word)
        else:
            self.list(user, channel, word)

    def list (self, user, channel, word):
        
        got_number = False
        
        if len(word) == 1:
        
            target = user
        
        elif len(word) == 2:
            
            if not is_number(word[1]):
                target = word[1]
            else:
                target = user
                number = int(word[1]) - 1
                got_number = True
                
        elif len(word) >= 3:
            
            target = word[1]
            
            if is_number(word[2]):
                number = int(word[2]) - 1
                got_number = True
            else:
                irc.msg(channel, "{}: Invalid number.".format(user))
                return
            
        req = target == user
        
        if target not in var.desktops:
            if req:
                irc.msg(channel, "{}: You don't have any desktops saved.".format(target))
            else:
                irc.msg(channel, "{} doesn't have any desktops saved.".format(target))
        else:
            list = []
            
            for index, url in enumerate(var.desktops[target]):
                if '!' in url:
                    list.append("[\x034NSFW\x0f] {}".format(url.strip('!')))
                else:
                    list.append("[{}] {}".format(index + 1, url))
            
            if got_number and (number + 1):
                if number >= len(list) or number < 0:
                    irc.msg(channel, "{} doesn't have that many desktops.".format(target))
                else:
                    irc.msg(channel, "{} [{}]".format(list[number], target))
            else:
                irc.msg(channel, "{} [{}]".format(' '.join(list), target))

    def add (self, user, channel, word):
        
        list = [url for url in word[2:] if url.startswith("http://") or url.startswith("https://")]
        
        if not list:
            irc.msg(channel, "{}: Links have to start with http:// or https://.".format(user))
            return
        
        if user not in var.desktops:
            var.desktops[user] = []
        elif len(var.desktops[user]) == 5:
            irc.msg(channel, "{}: You already have 5 desktops saved.".format(user))
            return
        
        for url in list:
            if len(var.desktops[user]) < 5:
                var.desktops[user].append(url)
            else:
                break
        
        config.addToIni("Desktops", user, '\n'.join(var.desktops[user]), "desktops.ini")
        irc.msg(channel, "{}: Desktop(s) added.".format(user))

    def delete (self, user, channel, word):
        
        list = [int(x) - 1 for x in word[2].split(',') if (is_number(x) and int(x) > 0)]
        
        if word[2] == "*" and user in var.desktops:
            del var.desktops[user]
            config.removeFromIni("Desktops", user, "desktops.ini")
            irc.msg(channel, "{}: All of your desktops were removed successfully.".format(user))
            return
        
        if not list:
            irc.msg(channel, "{}: Invalid number(s).".format(user))
            return
        
        if user not in var.desktops:
            irc.msg(channel, "{}: You don't have any desktops saved.".format(user))
            return
        
        for index, number in enumerate(list):
            if len(var.desktops[user]) > number:
                list[index] = var.desktops[user][number]
        
        for entry in list:
            if entry in var.desktops[user]:
                var.desktops[user].remove(entry)
        
        if var.desktops[user]:
            config.addToIni("Desktops", user, '\n'.join(var.desktops[user]), "desktops.ini")
        else:
            config.removeFromIni("Desktops", user, "desktops.ini")
        
        irc.msg(channel, "{}: Desktop(s) deleted.".format(user))
    
    def replace (self, user, channel, word):
        
        if len(word) < 4:
            irc.msg(channel, "{}: Wrong syntax. Check .help".format(user))
            return
        
        if not is_number(word[2]):
            irc.msg(channel, "{}: Invalid number.".format(user))
            return
        
        number = int(word[2]) - 1
        
        if number > 4 or number < 0:
            irc.msg(channel, "{}: Invalid number.".format(user))
        
        try:
            var.desktops[user][number] = word[3]
            irc.msg(channel, "{}: Desktop replaced.".format(user))
        except:
            irc.msg(channel, "{}: Invalid number.".format(user))
