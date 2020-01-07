import discord
import json
import enum
import commandDriver

with open('taigaBot.token', 'r') as f:
    token = f.read()

class TaigaClient(discord.Client):
    commandList = dict()
    sysCommandList = dict()
    async def refreshCommands(self):
        with open('commands.json', 'r') as f:
            self.commandList = json.load(f)
        with open('sysCmds.json', 'r') as f:
            self.sysCommandList = json.load(f)
        self.commandList.update(self.sysCommandList)
        
    async def on_ready(self):
        print(f'{self.user} has connected to Discord')

    async def mentions(self, message):
        #@mention handling
        for u in message.mentions:
            author = message.author.name if message.author.nick == None else message.author.nick
            user = u.name if u.nick == None else u.nick
            await message.channel.send(content=f'UwU {author} needs your bulgy wolgy {user}', tts=True)
       
        #@role handling
        for r in message.role_mentions:
            author = message.author.name if message.author.nick == None else message.author.nick
            await message.channel.send(content=f'UwU {author} needs your bulgy wolgy {r.name}', tts=True)


    async def on_message(self, message):
        await self.refreshCommands()
        await self.mentions(message)

        if len(message.content) > 0 and message.content[0] == '.':
            c = message.content[1:].split(' ', 1)
            if c[0] == '':
                return
            command = self.commandList[c[0].casefold()]

            if command["type"] == 0:
                await message.channel.send(command["text"])
            elif command["type"] == 1:
                e = discord.Embed()
                e.set_image(url=command["url"])
                await message.channel.send(content=None, embed=e)
            elif command["type"] == 10:
                await getattr(commandDriver, c[0].casefold())(message)
            else:
                await message.channel.send('Unrecognized Command')

client = TaigaClient()
client.run(token)