from .. import irc, var, ini
from ..tools import is_identified
from .. import simpledb

# The user needs to be registered and identified.
def ident (f):
    def check (user, channel, word):
        if is_identified(user):
            f(user, channel, word)
        else:
            irc.msg(channel, "{}: Identify with NickServ first.".format(user))
    return check

# Insert a message monitor.
def ins_monitor (line_obj):
    if line_obj.event == "JOIN":
        greet(line_obj.user, line_obj.channel)

# Insert command to set intros.
def ins_command ():
    var.commands["intro"] = type("command", (object,), {})()
    var.commands["intro"].method = read
    var.commands["intro"].tags = ["databases", "simpledb"]
    var.commands["intro"].aliases = [".intro", ".introduction"]
    var.commands["intro"].usage = [line.format("{}", n="intro") \
                                    for line in simpledb.command_usage]

# This command uses a database.
def ins_db ():
    global access_db, rm_entry
    global mod_entry
    
    var.data["intros"] = ini.fill_dict("intros.ini", "Introductions")
    var.data["intros"] = {
        user:var.data["intros"][user][0] for user in var.data["intros"]
    }
    
    namespace = simpledb.namespace(
        string_dictionary = var.data["intros"],
        dictionary_name   = "intro",
        section_name      = "Introductions",
        filename          = "intros.ini"
    )
    
    access_db = namespace.access_function
    mod_entry = namespace.modify_function
    rm_entry  = namespace.remove_function

# Command method.
def read (user, channel, word):
    if len(word) > 2 and word[1] in simpledb.mod_strings:
        mod_entry(user, channel, word)
    elif len(word) > 1 and word[1] in simpledb.del_strings:
        rm_entry(user, channel, word)
    else:
        access_db(user, channel, word)

# Greet the user, if possible.
def greet (user, channel):
    # Add entry for channel in settings if it isn't present.
    # Stop this madness if intros are disabled.
    if "intro.{}".format(channel) in var.settings:
        if not var.settings["intro.{}".format(channel)]:
            return
    else:
        var.settings["intro.{}".format(channel)] = True
        ini.add_to_ini("Settings", "intro.{}".format(channel), "true", "settings.ini")
    
    if user in var.data["intros"]:
        irc.msg(channel, "\x0f{}".format(var.data["intros"][user]))

# Functions filled by ins_db(). Start as None.
access_db = None
mod_entry = None
rm_entry = None
