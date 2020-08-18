import discord
from discord.utils import get
import asyncio
import os
import random
import collections
import datetime
import time
from random import randrange


randNum = random.random()
bot = discord.Client()
bot.suggestQueue = collections.deque()
###---------------------------------------------------------------------------- GAME STUFF
amazonlinks = ['https://www.amazon.com/Secret-Hitler/dp/B01JKD4HYC/ref=sr_1_4?dchild=1&keywords=weird+stuff&qid=1597776538&sr=8-4',
               'https://www.amazon.com/CASOFU-Tortilla-Comfortable-Burrito-60inches/dp/B07QTHK8K9/ref=sxin_7_ac_d_rm?ac_md=0-0-d2VpcmQgc3R1ZmY%3D-ac_d_rm&cv_ct_cx=weird+stuff&dchild=1&keywords=weird+stuff&pd_rd_i=B07QTHK8K9&pd_rd_r=5c084d14-ef4f-477f-870b-b7015b607c97&pd_rd_w=7PiKe&pd_rd_wg=oKTaU&pf_rd_p=e3dc9e0c-9eab-4c3e-b43a-ba36f8522e14&pf_rd_r=4YWMA6JTVJ3X7P1B8C1W&psc=1&qid=1597776538&sr=1-1-12d4272d-8adb-4121-8624-135149aa9081',
               'https://www.amazon.com/How-Talk-Your-About-Safety/dp/045149492X/ref=sr_1_10?dchild=1&keywords=weird+stuff&qid=1597776538&sr=8-10',
               'https://www.amazon.com/Cooking-Semen-Delicious-Recipes-Inappropriate/dp/1091069387/ref=sr_1_13?dchild=1&keywords=weird+stuff&qid=1597776538&sr=8-13',
               'https://www.amazon.com/Otamatone-Touch-Sensitive-Electronic-Musical-Instrument/dp/B00MRJ8GXK/ref=sr_1_14_sspa?dchild=1&keywords=weird+stuff&qid=1597776538&sr=8-14-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzNTQzTjdRTjNQNlU5JmVuY3J5cHRlZElkPUEwMTExNTM2MTNERlNHM1hFTjE4NSZlbmNyeXB0ZWRBZElkPUEwNDU1NjI1MTNWMTlYMlAzTzdZOSZ3aWRnZXROYW1lPXNwX210ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=',
               'https://www.amazon.com/Dodecagon-12-Side-Relieves-Depression-Children/dp/B071CFZ4BD/ref=sr_1_25?dchild=1&keywords=weird+stuff&qid=1597776538&sr=8-25',
               'https://www.amazon.com/CelebriDucks-Harry-Ponder-Wizard-RUBBER/dp/B01GSOTFMA/ref=sr_1_30_sspa?dchild=1&keywords=weird+stuff&qid=1597776538&sr=8-30-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzNTQzTjdRTjNQNlU5JmVuY3J5cHRlZElkPUEwMTExNTM2MTNERlNHM1hFTjE4NSZlbmNyeXB0ZWRBZElkPUEwMjE3OTcyVzEzNlFZVFZHUSZ3aWRnZXROYW1lPXNwX210ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=',
               'https://www.amazon.com/PIZOFF-Pullover-Drawstring-Sweatshirts-AM006-01-L/dp/B07HGYVM55/ref=sr_1_35?dchild=1&keywords=weird+stuff&qid=1597776538&sr=8-35',
               'https://www.amazon.com/Rubies-Conical-Alien-Skull-Flesh/dp/B001K3A45M/ref=sr_1_54?dchild=1&keywords=weird+stuff&qid=1597776538&sr=8-54',
               'https://www.amazon.com/Catholic-Hipster-Handbook-audiobook/dp/B07CVKHCLR/ref=sr_1_55?dchild=1&keywords=weird+stuff&qid=1597776538&sr=8-55',
               'https://www.amazon.com/Simulation-Pillow-Lumbar-Cushion-Stuffed/dp/B07SHP29DM/ref=sr_1_59_sspa?dchild=1&keywords=weird+stuff&qid=1597776538&sr=8-59-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzNTQzTjdRTjNQNlU5JmVuY3J5cHRlZElkPUEwMTExNTM2MTNERlNHM1hFTjE4NSZlbmNyeXB0ZWRBZElkPUEwOTYwNjU5MjRUMFFUSzQwNEhERyZ3aWRnZXROYW1lPXNwX2J0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=',
               'https://www.amazon.com/Bluetooth-BCELIFE-Hands-Free-Rechargeable-Gifts%C2%A3%C2%A8Gray%C2%A3/dp/B075KTTKXS/ref=sr_1_58_sspa?dchild=1&keywords=weird+stuff&qid=1597776538&sr=8-58-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEzNTQzTjdRTjNQNlU5JmVuY3J5cHRlZElkPUEwMTExNTM2MTNERlNHM1hFTjE4NSZlbmNyeXB0ZWRBZElkPUEwODA4OTYxMU1DQVRHSTlDVTZJVCZ3aWRnZXROYW1lPXNwX2J0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=',
               'https://www.amazon.com/Villager-News/dp/B01I2NXNE6/ref=sr_1_1?dchild=1&keywords=minecraft&qid=1597776724&sr=8-1',
               'https://www.amazon.com/Mattel-Games-FPD61-Minecraft-Card/dp/B074RCV4HQ/ref=sr_1_6?dchild=1&keywords=minecraft&qid=1597776733&sr=8-6',
               'https://www.amazon.com/Jay-Franco-Minecraft-Quilt-Piece/dp/B072L3GMZV/ref=sr_1_13_sspa?dchild=1&keywords=minecraft&qid=1597776743&sr=8-13-spons&psc=1&smid=A3G62KWEAWSGV9&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFLOTM3OVhFVEJEVk0mZW5jcnlwdGVkSWQ9QTAxMzkxMjUzR1VIMEpLTk81TEQyJmVuY3J5cHRlZEFkSWQ9QTA3MDAwOTM4MENMMkRPVTNVQ0gmd2lkZ2V0TmFtZT1zcF9tdGYmYWN0aW9uPWNsaWNrUmVkaXJlY3QmZG9Ob3RMb2dDbGljaz10cnVl',
               'https://www.amazon.com/Basics-Of-Fly-Fishing/dp/B07HKSTWBX/ref=sr_1_23?dchild=1&keywords=fishing&qid=1597776755&sr=8-23',
               'https://www.amazon.com/Clip-Roblox-Saving-Memes-Game/dp/B0837JN2FC/ref=sr_1_2?dchild=1&keywords=memes&qid=1597776791&sr=8-2']

embarrass = ['I pissed the bed last night!',
             'I listen to 100 gecs!',
             'I have a iphone 5s!',
             'I love Sword Art Online!',
             'I play sexual vr games!',
             'I Googled myself!',
             'I said you too when a staff worker told me to enjoy the movie!',
             'I take rewear filthy clothes from my hamper',
             'I do not brush my teeth!',
             'I think that big chungus is funny!',
             'I like to pretend that I am apart of a different culture to make myself look cool!',
             'I say pog irl unironically!',
             'I still say cringy unironically!',
             'I say and type XD unironically']
###---------------------------------------------------------------------------- END OF GAME STUFF



# Activity
async def updateSuggestions():
    channel = bot.get_channel(737807052625412208)
    async for message in channel.history(oldest_first=True):
        if get(message.reactions, emoji="✅") and get(message.reactions, emoji="❌"):
            bot.suggestQueue.append(message)


async def checkSuggestions():
    await bot.wait_until_ready()
    while True:
        if bot.suggestQueue:
            message = bot.suggestQueue[0]
            if (message.created_at.utcnow() - message.created_at).seconds > (6) * 3600 or (
                    message.created_at.utcnow() - message.created_at).days > 0:
                message = bot.suggestQueue.popleft()
                approvals = get(message.reactions, emoji="✅")
                denials = get(message.reactions, emoji="❌")
                if approvals.count > denials.count:
                    embedVar = discord.Embed(title="✅ Approved", description=message.content, color=0xEC00FF)
                else:
                    embedVar = discord.Embed(title="❌ Denied", description=message.content, color=0xEC00FF)
                embedVar.add_field(name="Suggested by:", value=message.author.mention, inline=False)
                await bot.get_channel(739172158948900925).send(embed=embedVar)
                await message.delete()
        await asyncio.sleep(5)


@bot.event
async def on_ready():
    await bot.change_presence(
        activity=discord.Activity(type=discord.ActivityType.watching, name="Republic of United Members"))
    await updateSuggestions()
    bot.loop.create_task(checkSuggestions())
    print("Bot is online. Instance ID is " + str(randNum))
    await bot.get_channel(740049560591925362).send("Bot is online. Instance ID is " + str(randNum))


# Bot commands
async def getLine(fileName, lineNum):
    fh = open(fileName)
    for i, row in enumerate(fh):
        if i + 1 == lineNum:
            return row


@bot.event
async def on_message(message):
    if message.channel.id == 737807052625412208:
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        bot.suggestQueue.append(message)
    # General Commands

    command = message.content.lower()
    if command.startswith('r?test'):
        await message.channel.send(randNum)

    if command.startswith('r?info'):
        embedVar = discord.Embed(title="RUM Bot",
                                 description="Custom bot developed for the Republic of United Members discord server.",
                                 color=0xEC00FF)
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

    # Rule commands

    if command.startswith('r?rule '):
        ruleNum = int(command.split(" ")[1])
        if 1 <= ruleNum <= 9:
            embedVar = discord.Embed(title=getLine("rules.txt", 2 * ruleNum - 1),
                                     description=getLine("rules.txt", 2 * ruleNum), color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        else:
            await message.channel.send("Invalid Rule Number")

##GAMES
    #guessing
    if message.content.startswith("r?guess"):
        channel = message.channel
        await channel.send("Guess the number between 0-10 by typing it! (it will end once you guess correctly)")
        number1 = random.randint(1,10)
        print(number1)

        number2 = str(number1)

        def check(m):
            return m.content == number2 and m.channel == channel

        msg = await bot.wait_for('message', check=check)
        await channel.send("Correct answer {.author}!". format(msg))


    #amazon
    if message.content.startswith("r?amazon"):
        funkylinks = random.choice(amazonlinks)
        await message.channel.send(funkylinks)



    #embarrass me

    if message.content.startswith('r?embarrassme'):
        embar = random.choice(embarrass)
        await message.channel.send(embar + ' from {}!'. format(message.author.mention))
























































@bot.event
async def on_raw_reaction_add(payload):
    pass


@bot.event
async def on_member_join(member):
    if member.bot == False:
        await bot.get_channel(736310120199225365).send(
            member.guild.get_role(736316470098657342).mention + " " + member.guild.get_role(
                739197317537726475).mention + " A new member has joined")











# Bot Token
# Reads from token.txt in users documents folder

token = open(os.path.join(os.environ['USERPROFILE'], 'Documents\\token.txt')).read()
bot.run(token)
