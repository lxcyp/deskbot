deskbot
-------

Started as a desktop bot. I'm trying to make it as complete as spoonbot, then work from there.

**Note:** [pylast](https://github.com/pylast/pylast "pylast") needs to be installed for the last.fm command module to work. Delete `modules/command_modules/lastfm.py` if you don't want the command.

**Note 2:** In case you choose to use the last.fm command module, you'll need to make an account for your version of the bot on [last.fm](http://www.last.fm/api/account/create) to get an API key and secret. Store them in `api-keys/lastfm` in plain text. The API key should be the first line, while the API secret should be second, in the file. Example output of `more api-keys/lastfm`:

```
34hasd3498apikeyhereW00ew
oi3nosAPIsecretHeRe34sdad
```

To start the bot:
```
./deskbot.py [-P password] [-b botnick] [-a admin_nick] [-p port] [-t timeout] [--log] [--log-file filepath] server

Alternatively:
python deskbot.py [-P password] [-b botnick] [-a admin_nick] [-p port] [-t timeout] [--log] [--log-file filepath] server
```

Log files will go into the `log/` directory.

I'm using argparse for the flags. Check `python deskbot.py -h` to learn how to use them.

Default port is 6667.
Default botnick is deskbot.

**There is no default admin nickname or NickServ password.**
