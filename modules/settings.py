import os.path
import ini

# Create settings dictionary.
def settings ():
    se_dict = ini.fill_dict("settings.ini", "Settings")
    
    se_dict = {
        key:
            True if se_dict[key][0] == "true"
            else False if se_dict[key][0] == "false"
            else se_dict[key][0]
        for key in se_dict.keys()
    }
    
    # Add default settings.
    se_dict = add_default_se(se_dict)
    
    return se_dict

# Create CTCP dictionary.
def ctcp ():
    ctcp_dict = ini.fill_dict("ctcp.ini", "CTCP")
    
    ctcp_dict = {
        key : ctcp_dict[key][0] for key in ctcp_dict.keys()
    }
    
    # Add default replies.
    ctcp_dict = add_default_ctcp(ctcp_dict)
    
    return ctcp_dict

# Default settings.
def add_default_se (se_dict):
    
    # Check for default settings file.
    if os.path.isfile("ini/default/settings.ini"):
        default_dict = ini.fill_dict("ini/default/settings.ini", "Settings")
        default_dict = {
            key:
                True if default_dict[key][0] == "true"
                else False if default_dict[key][0] == "false"
                else deafult_dict[key][0]
            for key in default_dict.keys()
        }
    else:
        print("WARNING: No default settings.ini found.")
        default_dict = {
            "ircop.prefix":"!", "owner.prefix":"~",
            "admin.prefix":"&", "op.prefix":"@",
            "halfop.prefix":"%", "voice.prefix":"+"
        }
    
    # Add each if not set.
    for option in default_dict.keys():
        if option not in se_dict:
            se_dict[option] = default_dict[option]
    
    return se_dict

# Default CTCP replies.
def add_default_ctcp (ctcp_dict):
    
    # Check for default CTCP replies file.
    if os.path.isfile("ini/default/ctcp.ini"):
        default_dict = ini.fill_dict("ini/default/ctcp.ini", "CTCP")
        default_dict = {
            key : default_dict[key][0] for key in default_dict.keys()
        }
    else:
        print("WARNING: No default ctcp.ini found.")
        default_dict = {}
    
    # Add each if not set.
    for option in default_dict.keys():
        if option not in ctcp_dict:
            ctcp_dict[option] = default_dict[option]
    
    return ctcp_dict
