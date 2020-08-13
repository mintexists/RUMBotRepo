import discord
from discord.utils import get
import asyncio
import os
import random
import collections
import datetime
import math

prefix = "r?"

randNum = random.random()
bot = discord.Client()
bot.suggestQueue=collections.deque()

# Activity
async def updateSuggestions():
    channel=bot.get_channel(737807052625412208)
    async for message in channel.history(oldest_first=True):
        if get(message.reactions, emoji="✅") and get(message.reactions, emoji="❌"):
            bot.suggestQueue.append(message)

async def checkSuggestions():
    await bot.wait_until_ready()
    while True:
        for message in bot.suggestQueue:
            approvalsObject=get(message.reactions, emoji="✅")
            denialsObject=get(message.reactions, emoji="❌")
            approvals=approvalsObject.count-(bot.user in set(await approvalsObject.users().flatten())) #gets # of yes reactions that isn't the bot
            denials=denialsObject.count-(bot.user in set(await denialsObject.users().flatten()))     #gets # of no reactions that isn't the bot
            timeLimit=datetime.timedelta(seconds=6*3600*(1-(approvals+denials)/bot.memberCount))            #math to figure out the time limit of the suggestion - 0 people reacted yet=6 hrs
            if (message.created_at.utcnow()-message.created_at)>timeLimit:
                bot.suggestQueue.remove(message)
                if approvals>denials:
                    embedVar = discord.Embed(title="✅ Approved", description = message.content , color=0x00FF04)
                    print("✅ Approved: \n" + message.content)
                else:
                    embedVar = discord.Embed(title="❌ Denied", description = message.content , color=0xFF0000)
                    print("❌ Denied: \n" + message.content)
                embedVar.add_field(name="Suggested by:", value = message.author.mention, inline=False)
                
                embedVar.add_field(name="Votes:", value = "✅ " + str(approvals) + " ❌ " + str(denials) , inline=False)
                files = []
                for attachments in message.attachments:
                    files.append(await attachments.to_file())
                await bot.get_channel(739172158948900925).send(embed=embedVar,files=files)
                await message.delete()
        await asyncio.sleep(5)


@bot.event
async def on_ready():
    # Set Status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Republic of United Members"))
    await updateSuggestions()
    bot.memberCount=len([m for m in bot.get_guild(736306540671271036).members if not m.bot])
    bot.loop.create_task(checkSuggestions())
    # Send bot online notices
    print("Bot is online. Instance ID is " + str(randNum))
    embedVar=discord.Embed(title=":green_circle: Bot is online", color=0x00ff62)
    embedVar.add_field(name="Instance ID:", value= randNum, inline=True)
    await bot.get_channel(740049560591925362).send(embed=embedVar)


        
#Bot commands
async def getLine(fileName,lineNum):
    fh=open(fileName)
    for i, row in enumerate(fh): 
        if i+1==lineNum: 
            return row

@bot.event
async def on_message(message):
    command = message.content.lower()

    # Add reaction to the suggestions
    if message.channel.id == 737807052625412208:
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        bot.suggestQueue.append(message)
        print("New Suggestion: " + message.content)

    # General Commands
    if command.startswith(prefix + 'test'):
        print("Test Called")
        embedVar=discord.Embed(title="[ID]", description= str(randNum), color=0x00ff62)
        files = []
        for each in message.attachments:
            files.append(await each.to_file())
        await message.channel.send(embed=embedVar, files=files)
    
    if command.startswith(prefix + 'info'):
        print("Info Called")
        embedVar =discord.Embed(title="RUM Bot", description="Custom bot developed for the Republic of United Members discord server.", color=0xd400ff)
        embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/738951182969602078/740711482391658567/botpic_2.png")
        embedVar.add_field(name="Version -", value="1.1.3", inline=True)
        embedVar.add_field(name="Contributors -", value="evalyn#8883, pupo#0001, MrMeme#5096", inline=True)
        embedVar.set_footer(text="Any questions? DM one of the contributors!")
        await message.channel.send(embed=embedVar)
        
    if command.startswith(prefix + 'server'):
        print("Server Called")
        embedVar=discord.Embed(title="Republic of United Members", description="Casual server focused around fairness and democracy. ")
        embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/738951182969602078/740711351152017458/e20176f3cfe1fc2d0edc24005d749a8b_2.png")
        embedVar.add_field(name="Creation Date:", value= message.guild.created_at.strftime("%b") + " " + message.guild.created_at.strftime("%d") + ", " + message.guild.created_at.strftime("%Y"), inline=True)
        embedVar.add_field(name="Server Age:", value= str((message.channel.guild.created_at.utcnow() - message.channel.guild.created_at).days) + " Days", inline=True)
        embedVar.add_field(name="Member Count:", value= message.guild.member_count, inline=True)
        embedVar.add_field(name="Current Consuls:", value="RaccWillAttacc#3661, FlobbsterBisque#5674", inline=True)
        await message.channel.send(embed=embedVar)
 
    if command.startswith(prefix + 'help'):
        print("Help Called")
        embedVar=discord.Embed(title="RUM Bot Command List", description="List containing all bot commands.", color=0xfb00ff)
        embedVar.set_thumbnail(url="https://cdn.discordapp.com/attachments/738951182969602078/740711482391658567/botpic_2.png")
        embedVar.add_field(name="r?help", value="Displays this list.", inline=True)
        embedVar.add_field(name="r?info", value="Displays bot info.", inline=True)
        embedVar.add_field(name="r?coinflip or cf", value="Flips a coin.", inline=True)
        embedVar.add_field(name="r?bubblewrap or wb", value="Makes a bubblewrap with text or emote", inline=True)
        embedVar.add_field(name="r?test", value="Sends the bot instance IDs", inline=True)
        embedVar.set_footer(text="Any questions? Ask one of the contributors! Any Suggestions? Put them in #suggestions!")
        await message.channel.send(embed=embedVar)

    if command.startswith(prefix + 'coinflip') or command.startswith(prefix + 'cf'):
        flipside = bool(random.getrandbits(1))
        if (flipside):
            flipside = "Heads"
        else:
            flipside = "Tails"
        print("Coin Flipped and Landed on " + flipside)
        await message.channel.send("> The coin landed on " + flipside)

    if command.startswith(prefix + 'rule '):
        ruleNum = int(command.split(" ")[1])
        print("Rule " + ruleNum + " Called")
        if 1<=ruleNum<=9:
            embedVar = discord.Embed(title=await getLine("rules.txt",2*ruleNum-1), description=await getLine("rules.txt",2*ruleNum), color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        else:
            await message.channel.send("Invalid Rule Number")

    if command.startswith(prefix + 'bubblewrap ') or command.startswith(prefix + 'bw '):
        # Sends a 10 by 10 grid of individually spoilered emotes
        bubble = str("||" + str(command.split(" ")[1]) + "||")
        dimensions = math.floor(math.sqrt(2000/len(bubble)))
        if dimensions > 15:
            dimensions = 15
        sendything = ((bubble * (dimensions - 2)) + "\n") * (dimensions - 2)
        print(sendything)
        print(len(sendything))
        await message.channel.send(sendything)
    
    if command.startswith(prefix + "status ") and message.author.id == 369988289354006528:
        status = str(message.content.split("status ")[1])
        await message.channel.send("The status is now " + status)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))
            
    if command.startswith(prefix + "warn") or command.startswith(prefix + "strike"):
        warnmember = message.mentions[0]
        if message.guild.get_role(736316470098657342) in message.author.roles or message.author.id == 369988289354006528 or message.author.id == 317456004843438082:
            # If has 4 give 5 and warn
            if warnmember.guild.get_role(742954033115037807) in warnmember.roles:
                await warnmember.add_roles(warnmember.guild.get_role(742954067642548285))
                await message.channel.send(warnmember.mention + " now has 5 strikes")
            # If has 3 give 4
            elif warnmember.guild.get_role(742953961014689842) in warnmember.roles:
                await warnmember.add_roles(warnmember.guild.get_role(742954033115037807))
                await message.channel.send(warnmember.mention + " now has 4 strikes")
            # If has 2 give 3
            elif warnmember.guild.get_role(742953920225214584) in warnmember.roles:
                await warnmember.add_roles(warnmember.guild.get_role(742953961014689842))
                await message.channel.send(warnmember.mention + " now has 3 strikes")
            # If has 1 give 2
            elif warnmember.guild.get_role(742953865439215656) in warnmember.roles:
                await warnmember.add_roles(warnmember.guild.get_role(742953920225214584))
                await message.channel.send(warnmember.mention + " now has 2 strikes")
            # If none give one
            else:
                await warnmember.add_roles(warnmember.guild.get_role(743205924059086918))
                await warnmember.add_roles(warnmember.guild.get_role(742953865439215656))
                await message.channel.send(warnmember.mention + " now has 1 strike")
    
    if command.startswith(prefix + "removewarn") or command.startswith(prefix + "removestrike"):
        warnmember = message.mentions[0]
        if message.guild.get_role(736316470098657342) in message.author.roles or message.author.id == 369988289354006528 or message.author.id == 317456004843438082:
            # If has 5 remove 5
            if warnmember.guild.get_role(742954067642548285) in warnmember.roles:
                await warnmember.remove_roles(warnmember.guild.get_role(742954067642548285))
                await message.channel.send(warnmember.mention + " now has 4 strikes")
            # If has 4 remove 4
            elif warnmember.guild.get_role(742954033115037807) in warnmember.roles:
                await warnmember.remove_roles(warnmember.guild.get_role(742954033115037807))
                await message.channel.send(warnmember.mention + " now has 3 strikes")
            # If has 3 remove 3
            elif warnmember.guild.get_role(742953961014689842) in warnmember.roles:
                await warnmember.remove_roles(warnmember.guild.get_role(742953961014689842))
                await message.channel.send(warnmember.mention + " now has 2 strikes")
            # If has 2 remove 2
            elif warnmember.guild.get_role(742953920225214584) in warnmember.roles:
                await warnmember.remove_roles(warnmember.guild.get_role(742953920225214584))
                await message.channel.send(warnmember.mention + " now has 1 strikes")
            # If has 1 remove 1
            elif warnmember.guild.get_role(742953865439215656) in warnmember.roles:
                await warnmember.remove_roles(warnmember.guild.get_role(743205924059086918))
                await warnmember.remove_roles(warnmember.guild.get_role(742953865439215656))
                await message.channel.send(warnmember.mention + " now has no strikes")
            else:
                await message.channel.send(warnmember.mention + " had no strikes")

    if command.startswith(prefix + "addrole"):
        roles = message.role_mentions
        if message.guild.get_role(736316470098657342) in message.author.roles or message.author.id == 369988289354006528 or message.author.id == 317456004843438082:
            for role in roles:
                for member in message.guild.members:
                    await member.add_roles(role)




@bot.event
async def on_reaction_add(reaction, user):
    # Remove reaction to make suggestion value accurate
    if reaction.message.channel.id == 737807052625412208 and user != bot.user:
        if reaction.emoji == "✅":
            await reaction.message.remove_reaction("✅", bot.user)
        elif reaction.emoji == "❌":
            await reaction.message.remove_reaction("❌", bot.user)

@bot.event
async def on_reaction_remove(reaction, user):
    # Re-add reaction if there is none
    if reaction.message.channel.id == 737807052625412208:
        if get(reaction.message.reactions, emoji="✅") is None:
            await reaction.message.add_reaction("✅")
        elif get(reaction.message.reactions, emoji="❌") is None:
            await reaction.message.add_reaction("❌")


@bot.event
async def on_member_join(member):
    # Ping welcomer and consulate when a new member joins the server
    if member.bot == False:
        await member.guild.get_channel(739647916905332846).send(member.mention + " has joined.\n" + member.guild.get_role(736316470098657342).mention)
        await member.add_roles(member.guild.get_role(743206825176072345), member.guild.get_role(743206597387485324))
        bot.memberCount+=1
    print(member.nick + " Joined")

@bot.event
async def on_member_leave(member):
    # Ping welcomer and consulate when a new member joins the server
    if member.bot == False:
        await member.guild.get_channel(739647916905332846).send(member.mention + " has left.\n" + member.guild.get_role(736316470098657342).mention)
        bot.memberCount-=1
    print(member.nick + " Left")



# Reads the enviorment variable token for the token value
# To set it on windows do set TOKEN=token
# U can also make that permanent by using Windows search and searching for environment variables and adding it as one
# linux u can set it with export TOKEN=token
# Macos is probs the same as linux

token = str(os.getenv('TOKEN'))
bot.run(token)
