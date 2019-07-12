import discord
import json
from lottery import LotteryBox


# SETUP CODE
client = discord.Client()


@client.event
async def on_ready():
    print("I'm ready!")


@client.event
async def on_message(mes):
    content = mes.content
    channel = mes.channel

    # '/register'が来たらチャンネル登録
    if content.startswith("/register"):
        if channel in client.allowed_channels:
            await channel.send(system_messages["ERR_REG"])
            return
        client.allowed_channels.append(channel)
        await channel.send(system_messages["CAN_SPEAK"].format(channel_name=channel.mention))
        return

    print(client.allowed_channels)
    if channel.id not in [ c.id for c in client.allowed_channels ]:
        return

    # メンバーのメンションを集めて箱を作る
    if channel.id not in client.boxes or client.boxes[channel.id].size() == 0:
        box = client.boxes[channel.id] = LotteryBox([ member.mention for member in channel.members if member.id != client.user.id and member.id not in exclusive_ids])
    else:
        box = client.boxes[channel.id]

    args = content.split(' ')
    if args[0] == "/pick":
        # '/pick'が来たらくじ引き
        message = ""
        if len(args) > 1:
            # 引数指定がある場合は指定して引く
            for removal in args[1:]:
                print(removal)
                box.remove(removal)
                message += system_messages["REMOVED"].format(removal=removal)
            message += system_messages["REMAINS"].format(size=box.size())
        else:
            # 引数指定がない場合はランダムに引く
            picked = box.pick()
            print(picked)
            message += system_messages["PICKED"].format(picked=picked)
            message += system_messages["REMAINS"].format(size=box.size())
        await channel.send(message)
    elif args[0] == "/team":
        # '/team'が来たらチーム分け
        if len(args) <= 1:
            # デフォルト値は2にしとく
            count = 2
        else:
            if not args[1].isnumeric():
                await channel.send(system_messages["ERR_NUM"])
                return
            count = int(args[1])

        if count > box.size():
            await channel.send(system_messages["ERR_CNT"])
            return

        messages = {}
        teams = box.team(count)
        for cnt in range(len(teams)):
            messages[cnt] = str(cnt + 1) + ": "
            messages[cnt] += " / ".join(teams[cnt])
        await channel.send("\n".join(messages.values()))
    elif args[0] == "/reset":
        # '/reset'が来たら箱を作り直す
        client.boxes[channel.id] = LotteryBox([ member.mention for member in channel.members if member.id != client.user.id])
        await channel.send(system_messages["RESET"])
    elif args[0] == "/help":
        await channel.send("```" + help_message + "```")


# MAIN CODE
with open("./message.json", encoding="UTF-8") as f:
    system_messages = json.load(f)

with open("./help.txt") as f:
    help_message = f.read()

exclusive_ids = []
try:
    f = open("./exclusive.txt")
    exclusive_ids = [ int(id.strip()) for id in f.readlines() ]
except:
    print("cannot open exclusive.txt")

with open('./token.txt') as f:
    client.allowed_channels = []
    client.boxes = {}
    token = f.read().strip()
    print(token)
    client.run(token)
