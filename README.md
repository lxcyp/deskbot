deskbot
-------

Started as a desktop bot. I'm trying to make it as complete as spoonbot, then work from there.

Check the wiki for a list of commands and how to make your own.

To start the bot:
```
python deskbot.py server [-P password] [-b botnick] [-a admin_nick] [-p port]
```

I'm using argparse for the flags. Check `python deskbot.py -h` to learn how to use them.

Default port is 6667.
Default botnick is deskbot.

**There is no default admin nickname or NickServ password.**
