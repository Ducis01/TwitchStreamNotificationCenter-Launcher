"""
    Fetch streams and display built-in notification that lanch stream on clic
    Author: Nicolas Van Wallendael <nicolas.vanwallendael@student.uclouvain.be>
    Antoine Van Malleghem  <antoine.vanmalleghem@student.uclouvain.be>
    Copyright (C) 2016, Université catholique de Louvain
"""

import sys, json, requests, subprocess, os, urllib, pickle

def save_obj(obj, name ):
    with open('obj/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    with open('obj/' + name + '.pkl', 'rb') as f:
        return pickle.load(f)


# Glob Var
STATUS = "status"
LOGO   = "logo"

# define user
user = "Duciis"
dir  =  os.getcwd()


# Request URL
url_follow = "https://api.twitch.tv/kraken/users/" + user + "/follows/channels"
url_online = "https://api.twitch.tv/kraken/streams?channel="


# GET list of streamer followed by #user
headers = {'Accept': 'application/vnd.twitchtv.v3+json'}

data    = requests.get(url_follow, headers=headers)

api     = data.json()["follows"];

streamers = [ap["channel"]["display_name"] for ap in api]

# Get currently online streams -> name, title and logo

url_online = url_online + ",".join(streamers)

data    = requests.get(url_online, headers=headers)

api     = data.json()["streams"];

stream  = [[ap["channel"]["display_name"], ap["channel"][STATUS], ap["channel"][LOGO]] for ap in api]
stream  = {streamer: {STATUS : status, LOGO : logo}  for [streamer, status, logo] in stream}



# Mac OS X Notifiactions


# Image in subprocess doesn't work, since it use a PRIVATE method feature
"""
notif = subprocess.Popen(["/usr/local/bin/terminal-notifier",\
                         "-group",        grp,\
                         "-title",        title,\
                         "-message",      msg,\
                         "-contentImage", img,\
                         "-appIcon",      twitch,\
                         "-execute",      script],
                         stdout=subprocess.PIPE)

output = notif.communicate()[0]
print(output)
"""

# load previous info
prev_stream = load_obj("prev_stream")

# For online streams
for streamer in stream.keys() :

    # if user already on and notified - dont show
    # if the status has changed - show
    
    if streamer not in prev_stream or stream[streamer][STATUS] != prev_stream[streamer][STATUS]:
        
        
        # Fetch the logo if we dont have it locally
        if not os.path.isfile(streamer) :
            urllib.request.urlretrieve(stream[streamer][LOGO], streamer)


        # NOTE <> INSIDE terminal-notifier :
        # Note that in some circumstances the first character of
        # a message has to be escaped in order to be recognized.
        # An example of this is when using an open bracket, which
        # has to be escaped like so: ‘\[’.

        msg   = '"\\' + stream[streamer][STATUS] + '"'
        grp   = "STREAM"    + streamer
        title = '"🍿 ' + streamer + ' is LIVE 🍿 "'
        img   =  os.path.join(dir, streamer)
        twitch=  os.path.join(dir, "twitch.png")
        script= '"' +  os.path.join(dir, "bash_script_twitch ") + streamer + '"'


        cmd = "terminal-notifier" + \
              " -group "   + grp + \
              " -message " + msg + \
              " -title "   + title + \
              " -contentImage " + img +\
              " -appIcon "      + twitch  +\
              " -execute "      + script


        # simple system call to override the img prob
        os.system(cmd)

for streamer in stream.keys() - prev_stream.keys() :
    cmd = "terminal-notifier -remove STREAM" + streamer
    os.system(cmd)
    print(streamer)

# save the streams that are online
save_obj(stream, "prev_stream")
