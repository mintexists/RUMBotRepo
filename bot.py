import discord
from discord.utils import get
import asyncio
import os
import random
import collections
import datetime

randNum = random.random()
bot = discord.Client()
bot.suggestQueue=collections.deque()
#Activity

async def checkSuggestions():
    await bot.wait_until_ready()
    while True:
        if bot.suggestQueue:
            message=bot.suggestQueue[0]
            if (message.created_at.utcnow()-message.created_at).seconds>(6)*5 or (message.created_at.utcnow()-message.created_at).days>0:
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
    bot.loop.create_task(checkSuggestions())
    print("Bot is online. Instance ID is " + str(randNum))
    await bot.get_channel(738951182969602078).send("Bot is online. Instance ID is " + str(randNum))


        
#Bot commands
def getLine(fileName,lineNum):
    fh=open(fileName)
    for i, row in enumerate(fh): 
        if i+1==lineNum: 
            return row

@bot.event
async def on_message(message):
    print("someone done sent a message")
    if message.channel.id == 737807052625412208:
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        bot.suggestQueue.append(message)
#General Commands

    command = message.content.lower()
    if command.startswith('r?test'):
        await message.channel.send(randNum)
    
    if command.startswith('r?info'):
        embedVar = discord.Embed(title="RUM Bot", description="Custom bot developed for the Republic of United Members discord server.", color=0xEC00FF)
        embedVar.add_field(name="Version", value="1.0.1", inline=False)
        embedVar.add_field(name="Contributors:", value="evalyn#8883, pupo#0001", inline=False)
        await message.channel.send(embed=embedVar)
 
    if command.startswith('r?help'):
        embedVar = discord.Embed(title="Help List", description="Command list. Prefix = r? ", color=0xEC00FF)
        embedVar.add_field(name="help", value="Displays this list.", inline=False)
        embedVar.add_field(name="info", value="Displays bot information.", inline=False)
        embedVar.add_field(name="coinflip or cf", value="flip a coin", inline=False)
        await message.channel.send(embed=embedVar)
    if command.startswith('r?coinflip') or command.startswith('r?cf'):
        flipside = bool(random.getrandbits(1))
        if (flipside):
            flipside = "Heads"
        else:
            flipside = "Tails"
        await message.channel.send("The coin landed on " + flipside)

#Rule commands

    if command.startswith('r?rule '):
        ruleNum = int(command.split(" ")[1])
        if 1<=ruleNum<=9:
            embedVar = discord.Embed(title=getLine("rules.txt",2*ruleNum-1), description=getLine("rules.txt",2*ruleNum), color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        else:
            await message.channel.send("Invalid Rule Number")

@bot.event
async def on_raw_reaction_add(payload):
    pass

@bot.event
async def on_member_join(member):
    if member.bot == False:
        await bot.get_channel(736310120199225365).send(member.guild.get_role(736316470098657342).mention + " " + member.guild.get_role(739197317537726475).mention + " A new member has joined")




#Bot Token

token = open(os.path.join(os.environ['USERPROFILE'], 'Documents\\token.txt')).read()
bot.run(token)
