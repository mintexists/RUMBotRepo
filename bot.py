import discord
from discord.utils import get
import asyncio
import os
import random
import collections
import datetime

prefix = "r?"

randNum = random.random()
bot = discord.Client()
bot.suggestQueue=collections.deque()
#Activity
async def updateSuggestions():
    channel=bot.get_channel(737807052625412208)
    async for message in channel.history(oldest_first=True):
        if get(message.reactions, emoji="✅") and get(message.reactions, emoji="❌"):
            bot.suggestQueue.append(message)

async def checkSuggestions():
    await bot.wait_until_ready()
    while True:
        if bot.suggestQueue:
            message=bot.suggestQueue[0]
            if (message.created_at.utcnow()-message.created_at).seconds>(6)*3600 or (message.created_at.utcnow()-message.created_at).days>0:
                message=bot.suggestQueue.popleft()
                approvals = get(message.reactions, emoji="✅")
                denials = get(message.reactions, emoji="❌")
                if approvals.count>denials.count:
                    embedVar = discord.Embed(title="✅ Approved", description = message.content , color=0xEC00FF)
                else:
                    embedVar = discord.Embed(title="❌ Denied", description = message.content , color=0xEC00FF)
                embedVar.add_field(name="Suggested by:", value = message.author.mention, inline=False)
                await bot.get_channel(739172158948900925).send(embed=embedVar)
                await message.delete()
        await asyncio.sleep(5)

@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Republic of United Members"))
    await updateSuggestions()
    bot.loop.create_task(checkSuggestions())
    print("Bot is online. Instance ID is " + str(randNum))
    await bot.get_channel(740049560591925362).send("Bot is online. Instance ID is " + str(randNum))


        
#Bot commands
async def getLine(fileName,lineNum):
    fh=open(fileName)
    for i, row in enumerate(fh): 
        if i+1==lineNum: 
            return row

@bot.event
async def on_message(message):
    if message.channel.id == 737807052625412208:
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        bot.suggestQueue.append(message)
#General Commands

    command = message.content.lower()
    if command.startswith(prefix + 'test'):
        await message.channel.send(randNum)
    
    if command.startswith(prefix + 'info'):
        embedVar = discord.Embed(title="RUM Bot", description="Custom bot developed for the Republic of United Members discord server.", color=0xEC00FF)
        embedVar.add_field(name="Version", value="1.0.1", inline=False)
        embedVar.add_field(name="Contributors:", value="evalyn#8883, pupo#0001", inline=False)
        await message.channel.send(embed=embedVar)
 
    if command.startswith(prefix + 'help'):
        embedVar = discord.Embed(title="Help List", description="Command list. Prefix = r? ", color=0xEC00FF)
        embedVar.add_field(name="help", value="Displays this list.", inline=False)
        embedVar.add_field(name="info", value="Displays bot information.", inline=False)
        embedVar.add_field(name="coinflip or cf", value="flip a coin", inline=False)
        await message.channel.send(embed=embedVar)
    if command.startswith(prefix + 'coinflip') or command.startswith(prefix + 'cf'):
        flipside = bool(random.getrandbits(1))
        if (flipside):
            flipside = "Heads"
        else:
            flipside = "Tails"
        await message.channel.send("> The coin landed on " + flipside)

#Rule commands

    if command.startswith(prefix + 'rule '):
        ruleNum = int(command.split(" ")[1])
        if 1<=ruleNum<=9:
            embedVar = discord.Embed(title=getLine("rules.txt",2*ruleNum-1), description=getLine("rules.txt",2*ruleNum), color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        else:
            await message.channel.send("Invalid Rule Number")

@bot.event
async def on_reaction_add(reaction, user):
    if reaction.message.channel.id == 737807052625412208 and user != bot.user:
        if reaction.emoji == "✅":
            await reaction.message.remove_reaction("✅", bot.user)
        elif reaction.emoji == "❌":
            await reaction.message.remove_reaction("❌", bot.user)

@bot.event
async def on_reaction_remove(reaction, user):
    if reaction.message.channel.id == 737807052625412208:
        if get(reaction.message.reactions, emoji="✅") is None:
            await reaction.message.add_reaction("✅")
        elif get(reaction.message.reactions, emoji="❌") is None:
            await reaction.message.add_reaction("❌")


@bot.event
async def on_member_join(member):
    if member.bot == False:
        await bot.get_channel(736310120199225365).send(member.guild.get_role(736316470098657342).mention + " " + member.guild.get_role(739197317537726475).mention + " A new member has joined")




# Bot Token
# SET THE ENVIORMENT VARIABLE TOKEN TO EQUAL THE TOKEN
# To set it on windows do set TOKEN=token
# linux u can set it with export TOKEN=token
# im watchging the simpsons rn and flanders seems like a bad dad
# is flanders supposed to be seen as a bad dad or is he supposed to be seen as a good dad
# im boredddddddd

token = str(os.getenv('TOKEN'))
bot.run(token)
