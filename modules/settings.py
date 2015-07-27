import ini

def init ():
    se_dict = ini.fill_dict("settings.ini", "Settings")
    
    se_dict = {
        key:
            True if se_dict[key][0] == "true"
            else False if se_dict[key][0] == "false"
            else se_dict[key][0]
        for key in se_dict.keys()
    }
    
    # Add default settings if necessary variables aren't present.
    add_default(se_dict)
    
    return se_dict

def add_default (se_dict):
    
    if "ircop.prefix" not in se_dict:
        se_dict["ircop.prefix"] = "!"
    
    if "owner.prefix" not in se_dict:
        se_dict["owner.prefix"] = "~"
    
    if "admin.prefix" not in se_dict:
        se_dict["admin.prefix"] = "&"
    
    if "op.prefix" not in se_dict:
        se_dict["op.prefix"] = "@"
    
    if "halfop.prefix" not in se_dict:
        se_dict["halfop.prefix"] = "%"
    
    if "voice.prefix" not in se_dict:
        se_dict["voice.prefix"] = "+"
