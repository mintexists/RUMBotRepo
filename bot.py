import discord
from discord.ext    import commands
from discord.ext.commands   import Bot
import asyncio
import os
import random

bot = commands.Bot(command_prefix='<')

#Activity

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Republic of United Members"))
    print("Bot is online.")

#Bot commands 

@bot.event
async def on_message(message):
    if message.channel.id == 737807052625412208:
        await message.add_reaction("✅")
        await message.add_reaction("❌")

#General Commands    

    if message.content.startswith('r?info'):
        embedVar = discord.Embed(title="RUM Bot", description="Custom bot developed for the Republic of United Members discord server.", color=0xEC00FF)
        embedVar.add_field(name="Version", value="1.0.1", inline=False)
        embedVar.add_field(name="Contributors:", value="evalyn#8883, pupo#0001", inline=False)
        await message.channel.send(embed=embedVar)
 
    if message.content.startswith('r?help'):
        embedVar = discord.Embed(title="Help List", description="Command list. Prefix = r? ", color=0xEC00FF)
        embedVar.add_field(name="help", value="Displays this list.", inline=False)
        embedVar.add_field(name="info", value="Displays bot information.", inline=False)
        await message.channel.send(embed=embedVar)
    if message.content.startswith('r?coinflip') or message.content.startswith('r?cf'):
        flipside = bool(random.getrandbits(1))
        if (flipside):
            flipside = "Heads"
        else:
            flipside = "Tails"
        await message.channel.send("The coin landed on " + flipside)

#Rule commands

    if message.content.startswith('r?rule '):
        ruleNum = int(message.content.split(" ")[1])
        if ruleNum == 1:
            embedVar = discord.Embed(title="- 1 - Keep things civil:", description="Don't make the server too crazy. By all means, have fun and crack some jokes, but we want to make this a safe environment. Swearing is allowed, but don't use words that would be offensive to a person or group.", color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        elif ruleNum == 2:
            embedVar = discord.Embed(title="- 2 - Don't post NSFW content:", description="Inappropriate images/media will not be tolerated. Any blood, gore, nudity, etc. or with excessive implications to such topics will probably lead to punishment. As a rule of thumb - if you're not fine with your grandma seeing it, don't post it here.", color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        elif ruleNum == 3:
            embedVar = discord.Embed(title="- 3 - Maintain chat quality:", description="This means no intentional spamming or shitposting in channels that aren't made for it. In addition, be considerate of other people's ears in voice chats.", color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        elif ruleNum == 4:
            embedVar = discord.Embed(title="- 4 - Keep Content to its Appropriate Channels:", description="Some content doesn't belong in #general, so we ask that you please keep such content in their designated channels. Media and images are allowed in #general unless spammed or otherwise high in number. Keep pictures or art in  #media for the most part though.  We also have a #bots channel, to not clog up our general channel. Generally, memes should go in #memes, but we like to be lenient if it doesn't cause a huge issue. Just know that we have a #memes channel for a reason.  We also have a #serious which are made for specific discussion content, so if you wish to have a prolonged discussion about serious stuff, do it in there.", color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        elif ruleNum == 5:
            embedVar = discord.Embed(title="- 5 - No Advertising:", description="Advertising is promoting a Discord server, YouTube channel or some other site without our consent. Under no circumstances may Discord invite links be posted in our server (minus our own invite link). You may promote your own YouTube channel or other form of media if you get the permission of the people and leaders beforehand. Advertising via DMs is also unallowed unless the person you are DMing the content to has consented beforehand.", color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        elif ruleNum == 6:
            embedVar = discord.Embed(title="- 6 - No Cold / Ghost Pinging:", description="Cold pinging is pinging somebody for no reason. Ghost pinging is pinging somebody and then deleting the message, which is also annoying. Both of these actions may result in a punishment if repeated. Know that deleted messages in this server are logged and you cannot hide ghost pings from other people.", color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        elif ruleNum == 7:
            embedVar = discord.Embed(title="- 7 - Take drama with members to DMs:", description="We are fine with gossip as this is a friends server, however if you have direct drama with another server member please dont bring it up in this server. Please bring your arguments to DMs as we dont want to make the situation worse with the inclusion of other members.", color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        elif ruleNum == 8:
            embedVar = discord.Embed(title="- 8 - No Sensitive or Disturbing Content:", description="This includes politics and religion, if you think a discussion may be violating this rule please make sure to ask a consul. If you really want to talk about sensitive content please keep it limited to #serious . This also includes Hate Speech. It will not be tolerated at all. Any hate speech will get you banned and could be reported to real authorities.", color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        elif ruleNum == 9:
            embedVar = discord.Embed(title="- 9 - Alts are not Allowed:", description="Do not invite alternate accounts, they are forbidden as they can be used to rig elections. If you REALLY want to invite an alt for any purpose than DM a consul with a valid reason and you may be allowed.", color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        elif ruleNum == 10:
            embedVar = discord.Embed(title="- 10 - Use Common Sense:", description="If you think it can get you banned, don't do it. Just because something isn't in the rules doesn't mean you can't get in trouble for it. Don't post illegal stuff, don't doxx people, don't be annoying. Make this server safe and friendly.", color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        else:
            await message.channel.send("Invalid Rule Number")


#Bot Token

token = open(os.path.join(os.environ['USERPROFILE'], 'My Documents\\token.txt')).read()
bot.run(token)
