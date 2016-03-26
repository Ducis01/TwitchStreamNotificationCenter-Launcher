# TwitchStreamNotificationCenter-Launcher

This python script produces Mac OS X built-in notifications for any live stream followed by a user on twitch.
A notification is produce for a new live or title change.
Each notification has the title of the stream and the stream logo.

This script suppose the use of mpv, livestreamer and terminal-notifier.

User name and mpv & livestreamer location need to be set in [bash_script_twitch].

This script must be set with "crontab -e" to be executed every e.g. min 
>> * * * * * python3 ~/.stream/growlerStreams.py (run every minutes)

