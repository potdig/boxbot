import discord
from lottery import LotteryBox


client = discord.Client()
client.allowed_channels = []
client.boxes = {}


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
            await channel.send(":no_entry_sign: **ERROR! This channel is already registered!**")
            return
        client.allowed_channels.append(channel)
        await channel.send(f":tada: **I can speak in {channel.mention} from now! ;)**")
        return

    # メンバーのメンションを集めて箱を作る
    if channel.id not in client.boxes or client.boxes[channel.id].size() == 0:
        box = client.boxes[channel.id] = LotteryBox([ member.mention for member in channel.members if member.id != client.user.id])
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
                message += f":outbox_tray: **{removal} has removed from box**\n"
            message += f"**{box.size()} remains in the box**"
        else:
            # 引数指定がない場合はランダムに引く
            picked = box.pick()
            print(picked)
            message += f":point_right: **{picked}, it's your turn**"
            message += "\n" + f"**{box.size()} remains in the box**"
        await channel.send(message)
    elif args[0] == "/team":
        # '/team'が来たらチーム分け
        if len(args) <= 1:
            # デフォルト値は2にしとく
            count = 2
        else:
            if not args[1].isnumeric():
                await channel.send(":no_entry_sign: **ERROR! Non-numeric argument!!**")
                return
            count = int(args[1])

        if count > box.size():
            await channel.send(":no_entry_sign: **ERROR! Team count is larger than amount in the box!!**")
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
        await channel.send(":inbox_tray: **Box has reset.**")
    elif args[0] == "/help":
        help_message = '''```
/pick [@mention...] : Pick from the box randomly. Add @mention to specify content.
/team count : Make teams with contents in the box. Specify count.
/reset : Reset the box.
/help : Show this help.
```'''
        await channel.send(help_message)


with open('./token.txt') as f:
    token = f.read().strip()
    print(token)
    client.run(token)
