#!/usr/bin/env python3

"""
    Fetch streams and display built-in notification that lanch stream on clic
    Author: Nicolas Van Wallendael <nicolas.vanwallendael@student.uclouvain.be>
    Copyright (C) 2016, Nicolas Van Wallendael
"""

import sys, json, requests, os, urllib, pickle
from subprocess import check_output, PIPE, call

# Glob Var
STATUS = "status"
LOGO   = "logo"
BOX    = "box"
GAME   = "game"

POPUL  = "popularity"
LARGE  = "large"

USER   = sys.argv[1]
DIR    = sys.argv[2]
PLAYER = sys.argv[5]
TERMINAL_NOTIFIER = sys.argv[3]
LIVESTREAMER      = sys.argv[4]

TWITCH =  os.path.join(DIR, "twitch.png")
FOLLOWING = "https://www.twitch.tv/directory/following"

# define tmp directory
tmp  = "/tmp/twitchNotif/"

def save_obj(obj, name ):
    if not os.path.exists(tmp):
        os.makedirs(tmp)
    
    with open(tmp + name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
    if not os.path.isfile(tmp + name + '.pkl') :
        if not os.path.exists(tmp):
            os.makedirs(tmp)
        return {}
    else :
        with open(tmp + name + '.pkl', 'rb') as f:
            return pickle.load(f)


# Request URL
url_follow = "https://api.twitch.tv/kraken/users/" + USER + "/follows/channels?direction=DESC&limit=500&offset=0&sortby=created_at"
url_online = "https://api.twitch.tv/kraken/streams?channel="
url_game_0 = "https://api.twitch.tv/kraken/search/games?query="
url_game_1 = "&type=suggest"


# GET list of streamer followed by #user
headers = {'Accept': 'application/vnd.twitchtv.v3+json'}

data    = requests.get(url_follow, headers=headers)

api     = data.json()["follows"];

streamers = [ap["channel"]["display_name"] for ap in api]

# Get currently online streams -> name, title, logo and game.

url_online = url_online + ",".join(streamers)

data    = requests.get(url_online, headers=headers)

api     = data.json()["streams"];

stream  = [[ap["channel"]["display_name"], ap["channel"][STATUS], ap["channel"][LOGO], ap["channel"][GAME]] for ap in api]
stream  = {streamer: {STATUS : status, LOGO : logo, GAME : game.replace(" ","+")}  for [streamer, status, logo, game] in stream}


# Mac OS X Notifiactions

# load previous info
prev_stream = load_obj("prev_stream")

# Get current notifications
process = check_output([TERMINAL_NOTIFIER, '-list', 'ALL'])

current_notif = str(process).split("\\n")
current_notif = [ notif.split("\\t")[0].replace("STREAM", "") for notif in current_notif][1:-1]

# For online streams
for streamer in stream.keys() :

    # if user already on and notified - dont show
    # if new stream - show
    # if the user has clicked the notification - reshow it
    # if the status has changed - show
    # if the game   has changed - show
    
    if streamer not in prev_stream or streamer not in current_notif or \
        stream[streamer][STATUS] != prev_stream[streamer][STATUS] or \
        stream[streamer][GAME]   != prev_stream[streamer][GAME]:
        
        # Fetch the logo if we dont have it locally
        if not os.path.isfile(tmp + streamer) :
            urllib.request.urlretrieve(stream[streamer][LOGO], tmp + streamer)

        # Fetch the game BOX image if we dont have it locally
        if not os.path.isfile(tmp + stream[streamer][GAME]):
            
            url_game = url_game_0 + stream[streamer][GAME] + url_game_1
            data     = requests.get(url_game, headers=headers)
            api      = data.json()["games"];
            
            # take the logo which is the more popular among all available.
            games = max([[game[POPUL], game[BOX][LARGE]] for game in api])
            
            urllib.request.urlretrieve(games[1], tmp + stream[streamer][GAME])


        # NOTE <> INSIDE terminal-notifier :
        # Note that in some circumstances the first character of
        # a message has to be escaped in order to be recognized.
        # An example of this is when using an open bracket, which
        # has to be escaped like so: ‘\[’ (cfr. msg var.).

        msg   = '"\\' + stream[streamer][STATUS] + '"'
        grp   = "STREAM"    + streamer
        title = '"🍿 ' + streamer + ' is LIVE 🍿 "'
        img   = os.path.join(tmp, streamer)
        gameI = os.path.join(tmp, stream[streamer][GAME])
        script= '"' +  os.path.join(DIR, "bash_script_twitch.bash ") + streamer + \
                " " + LIVESTREAMER + " " + PLAYER + " '" + stream[streamer][STATUS] + "' " +\
                '& sleep 10; killAll terminal-notifier"'


        cmd = TERMINAL_NOTIFIER + \
              " -group "   + grp + \
              " -message " + msg + \
              " -title "   + title + \
              " -contentImage " + img +\
              " -appIcon "      + gameI  +\
              " -execute "      + script

        # Image/Icon in "subprocess.Popen" doesn't work, since it use a PRIVATE method feature
        # simple system call to override the img prob
        #print(cmd.encode('utf-8'))
        
        # We can only launch a stream every 10 sec
        # its the time for livestreamer to be ready on average
        # so we can kill the parent
        call(cmd, shell=True)

# To remove a notification we have to create a new one
# Therefore, we assign each DC to a group called STREAM
# so we dont have a new notification for each offline stream
# that stack in the Notification Center
for streamer in prev_stream.keys() - stream.keys():
    
    msg   = '"is now offline."'
    title = streamer
    img   = os.path.join(tmp, streamer)
    
    cmd = TERMINAL_NOTIFIER + \
        " -remove STREAM" + streamer + \
        " -group STREAM" + \
        " -message " + msg + \
        " -title "   + title + \
        " -contentImage " + img +\
        " -appIcon "      + TWITCH +\
        " -open " + FOLLOWING
    
    call(cmd, shell=True)

# save the streams that are online
save_obj(stream, "prev_stream")
