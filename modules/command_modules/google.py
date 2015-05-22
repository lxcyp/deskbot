from .. import irc, var
import json, urllib

# Fill command dictionary.
def ins_command ():
    var.commands["google"] = type("command", (object,), {})()
    var.commands["google"].method = google
    var.commands["google"].aliases = [".google", ".g"]
    var.commands["google"].usage = ["{} query here - Look up \"query here\" and display first result."]

# Look up something on google.
def google (user, channel, word):
    # In case no input is given.
    if len(word) == 1:
        irc.msg(channel, "{}: Tell me something to google, come on.".format(user))
        return
    
    # Create query and google it.
    query = " ".join(word[1:])
    g = search(query)
    
    if g:
        irc.msg(channel, "Title: {}".format(g["title"]))
        irc.msg(channel, "URL: {}".format(g["url"]))
    else:
        irc.msg(channel, "{}: No results found.".format(user))

def search (query):
    q = urllib.urlencode({"q":query})
    url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&" + q
    search_results = urllib.urlopen(url).read()
    results = json.loads(search_results)
    data = results["responseData"]
    
    if not data["results"]:
        return {}
    
    else:
        return {
            "title":data["results"][0]["titleNoFormatting"],
            "url":data["results"][0]["url"]
        }
