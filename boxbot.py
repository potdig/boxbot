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
            await channel.send("This channel is already registered!")
            return
        client.allowed_channels.append(channel)
        await channel.send(f"I can speak in {channel.mention} from now! ;)")
        return

    # メッセージを送れるチャンネルかチェック
    if channel not in client.allowed_channels:
        await channel.send("This channel is not allowed to send message for me!")

    # メンバーのメンションを集めて箱を作る
    if channel.id not in client.boxes or client.boxes[channel.id].size() == 0:
        box = client.boxes[channel.id] = LotteryBox([ member.mention for member in channel.members if member.id != client.user.id])
    else:
        box = client.boxes[channel.id]

    args = content.split(' ')
    if args[0] == "/pick":
        # '/pick'が来たらくじ引き
        if len(args) > 1:
            # 引数指定がある場合は指定して引く
            for removal in args[1:]:
                print(removal)
                box.remove(removal)
                await channel.send(f"{removal} has removed from box")
            await channel.send(f"{box.size()} remains in the box")
        else:
            # 引数指定がない場合はランダムに引く
            picked = box.pick()
            print(picked)
            await channel.send(f"{picked}, it's your turn")
            await channel.send(f"{box.size()} remains in the box")
    elif args[0] == "/team":
        # '/team'が来たらチーム分け
        if len(args) <= 1:
            # デフォルト値は2にしとく
            count = 2
        else:
            if not args[1].isnumeric():
                await channel.send("**ERROR!** Non-numeric argument!!")
                return
            count = int(args[1])
        teams = box.team(count)
        for cnt in range(len(teams)):
            message = str(cnt + 1) + ": "
            message += " / ".join(teams[cnt])
            await channel.send(message)
    elif args[0] == "/help":
        help_message = '''```
/pick [@mention...] : Pick from the box randomly. Add @mention to specify content.
/team count : Make teams with contents in the box. Specify count.
/help : Show this help.
```'''
        await channel.send("")


with open('./token.txt') as f:
    token = f.read().strip()
    print(token)
    client.run(token)
