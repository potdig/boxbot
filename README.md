# Lottery-chan
Discord bot that makes lottery box of channel member.

## !! WARNING !!
This bot sends a lot of mentions. Check the channel before launching!!

## Setup
### Launching bot
First, Make file named "token.txt" that Discord client token is written.
```
$ echo "Y0ur_R4qu35T-70KeN.C0mE5h3Re" > token.txt
```
After it, you can launch the bot.
```
$ python3 boxbot.py
```

If console says `I'm ready!`, bot has launched.

### Registering channel to bot
On Discord, bot account should be online in your server. Send `/register` on the channel you want to use the bot. **(Again, check the channel once more!!)** If you see the message with :tada: from the bot, you can use the bot ;) Send `/help` to check the usage.

## Configuration
### Message from Bot
You can configure message. Edit `message.json` and `help.txt`. (I made preset for English and Japanese. I recommend to make link like below)
```
$ ln -sf message_ja.json message.json
```
### Exclusive List
You can exclude members from the box. Write ID of the member you want to exclude to `exclusive.txt`.
```
$ echo 000000000000000000 >> exclusive.txt
```

