# TwitchStreamNotificationCenter-Launcher

This python script produces Mac OS X (>10.9) built-in notifications for any live stream followed by a user on twitch.
A notification is produce for a new live or title change or a stream going offline.
Each notification has the title of the stream and the stream logo.
Each notification is also click-able and launch the stream in mpv.
Offline notification open 'Twitch following' on default browser.

This script suppose the use of python3 + requests, mpv (https://github.com/mpv-player/mpv), livestreamer (https://github.com/chrippa/livestreamer) and terminal-notifier (https://github.com/julienXX/terminal-notifier). (All available throygh brew or pip3)


## TO MAKE IT WORK

Change in [_.plist] under "ProgramArguments" :

* [0] = Python3 bin location ;
* [1] = [_.py] location  ;
* [2] = Twitch User name ;
* [3] = [_.bash] and [_.py] and [_.png] -This Git- directory location  ;
* [4] = terminal-notifier bin location  ;
* [5] = livestreamer bin location  ;
* [6] = mpv  bin location  ;


This script must be set with launchD to work every minute :
> mv be.ducis01.notiftwitch.agent.plist $HOME/Library/LaunchAgents/  
> launchctl load $HOME/Library/LaunchAgents/be.ducis01.notiftwitch.agent.plist  
> chmod +x *.bash 

> Also dont forget to create a Twitch Authenticate token to make request :
> This as to be added under .livestreamerrc 
>> \# Authenticate with Twitch
>> twitch-oauth-token= ***********************

twitch-oauth-token=
## Screenshots :

![Image of a Notification](https://raw.githubusercontent.com/Ducis01/TwitchStreamNotificationCenter-Launcher/master/screenshot/notification.png)

![Image of Notification Center](https://raw.githubusercontent.com/Ducis01/TwitchStreamNotificationCenter-Launcher/master/screenshot/notification_center.png)

