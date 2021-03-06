import time
import random
from .. import irc, var
from ..tools import ctcp_req

# Fill command dictionary.
def ins_command ():
    var.commands["ping"] = type("command", (object,), {})()
    var.commands["ping"].method = ping
    var.commands["ping"].tags = ["other", "ctcp"]
    var.commands["ping"].aliases = [".ping", ".pingme"]
    var.commands["ping"].usage = ["{} - Get ping'd."]

# Command method.
def ping (user, channel, word):
    request = int(time.time())
    
    start = time.time()
    response = ctcp_req(user, "PING", request)
    end = time.time()
    
    if str(request) == response:
        irc.msg(channel, "{}: {} seconds.".format(user, round(end-start, 3)))
    else:
        irc.msg(channel, "{}: Ping over 20 seconds or no reply.".format(user))
