# TwitchStreamNotificationCenter-Launcher

This python script produces Mac OS X built-in notifications for any live stream followed by a user on twitch.
A notification is produce for a new live or title change.
Each notification has the title of the stream and the stream logo.

This script suppose the use of python3, mpv, livestreamer and terminal-notifier.

TO MAKE IT WORK - Change in [_.plist] under "ProgramArguments" :

* [0] = Python3 bin location ;
* [1] = [_.py] location  ;
* [2] = Twitch User name ;
* [3] = [_.bash] and [_.py] and [_.png] (This Git) directory location  ;
* [4] = terminal-notifier bin location  ;
* [5] = livestreamer bin location  ;
* [6] = MPV  bin location  ;


This script must be set with launchD to work every minute :
> mv be.ducis01.notiftwitch.agent.plist $HOME/Library/LaunchAgents/
> launchctl load $HOME/Library/LaunchAgents/be.ducis01.notiftwitch.agent.plist

ATM : live notification can only be replaced (eg the title changes) but not removed if the stream goes off in the Notification Center.

Screenshots :

![Image of a Notification](https://raw.githubusercontent.com/Ducis01/TwitchStreamNotificationCenter-Launcher/master/screenshot/notification.png)

![Image of Notification Center](https://raw.githubusercontent.com/Ducis01/TwitchStreamNotificationCenter-Launcher/master/screenshot/notification_center.png)

