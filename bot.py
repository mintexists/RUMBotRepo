import discord
from discord.utils import get
import asyncio
import os
import random
import collections
import datetime
import math
import traceback
 

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
        for message in list(bot.suggestQueue):
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
                embedVar.set_footer(text="Suggested at " + str(message.created_at.strftime("%b %d %Y %H:%M:%S")))
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

async def getLine(fileName,lineNum):
    fh=open(fileName)
    for i, row in enumerate(fh): 
        if i+1==lineNum: 
            return row

@bot.event
async def on_message(message):
    command = message.content.lower()
    
    ##GAMES
    # guessing
    if message.content.startswith("r?guess"):
        channel = message.channel
        await channel.send("Guess the number between 0-10 by typing it! (it will end once you guess correctly)")
        number1 = random.randint(1, 10)
        print(number1)

        number2 = str(number1)

        def check(m):
            return m.content == number2 and m.channel == channel

        msg = await bot.wait_for('message', check=check)
        await channel.send("Correct answer {.author}!".format(msg))
        
        # amazon
    if message.content.startswith("r?amazon"):
        funkylinks = random.choice(amazonlinks)
        await message.channel.send(funkylinks)
        
        # embarrass me
    if message.content.startswith('r?embarrassme'):
        embar = random.choice(embarrass)
        await message.channel.send(embar + ' from {}!'.format(message.author.mention))

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
    
    # Eval command 
    if command.startswith(prefix + 'eval ') and message.author.id == 369988289354006528:
        try:
            msg = await eval(command.split(' ', 1)[1])
            await message.channel.send("```{}```".format(str(msg)))
        except:
            try:
                msg = eval(command.split('eval ')[1])
                await message.channel.send("```{}```".format(str(msg)))
            except:
                e = traceback.format_exc()
                await message.channel.send("```{}```".format(str(e)))

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
        num_lines = sum(1 for line in open('help.txt'))
        for helpNum in range((num_lines//2)):
            embedVar.add_field(name=await getLine('help.txt',2*helpNum+1), value=await getLine('help.txt',2*helpNum+2), inline=True)
        embedVar.set_footer(text="Any questions? Ask one of the contributors! Any Suggestions? Put them in #suggestions!")
        await message.channel.send(embed=embedVar)

    if command.startswith(prefix + 'coinflip') or command.startswith(prefix + 'cf'):
        flipside = bool(random.getrandbits(1))
        if (flipside):
            flipside = "Heads"
        else:
            flipside = "Tails"
        print("Coin Flipped and Landed on {}".format(flipside))
        await message.channel.send("> The coin flipped and landed on {}".format(flipside))

    if command.startswith(prefix + 'rule '):
        ruleNum = int(command.split(" ", 1)[1])
        print("Rule {} Called".format(str(ruleNum)))
        if 1<=ruleNum<=9:
            embedVar = discord.Embed(title=await getLine("rules.txt",2*ruleNum-1), description=await getLine("rules.txt",2*ruleNum), color=0xEC00FF)
            await message.channel.send(embed=embedVar)
        else:
            await message.channel.send("Invalid Rule Number")

    if (command.startswith(prefix + 'bubblewrap ') or command.startswith(prefix + 'bw ')):
        if not command.find("@") == -1:
            await message.channel.send("You cant ping people with this")
        else:
            # Sends the biggest grid smaller then 15 of individually spoilered emotes
            maxSize = 10
            bubble = str("||" + str(command.split(" ", 1)[1]).replace("\n", "") + "||")
            dimensions = math.floor(math.sqrt(2000/len(bubble)))
            if dimensions > maxSize:
                dimensions = maxSize
            sendything = ((bubble * (dimensions - 2)) + "\n") * (dimensions - 2)
            await message.channel.send(sendything)

    if command.startswith(prefix + "status ") and message.author.id == 369988289354006528:
        status = str(message.content.split(" ", 1)[1])
        await message.channel.send("The status is now {}".format(status))
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=status))

    if command.startswith(prefix + "warn") or command.startswith(prefix + "strike"):
        warnmember = message.mentions[0]
        if message.guild.get_role(736316470098657342) in message.author.roles or message.author.id == 369988289354006528:
            # If has 4 give 5 and warn
            if warnmember.guild.get_role(742954033115037807) in warnmember.roles:
                await warnmember.add_roles(warnmember.guild.get_role(742954067642548285))
                await message.channel.send("{} now has 5 strikes".format(warnmember.mention))
            # If has 3 give 4
            elif warnmember.guild.get_role(742953961014689842) in warnmember.roles:
                await warnmember.add_roles(warnmember.guild.get_role(742954033115037807))
                await message.channel.send("{} now has 4 strikes".format(warnmember.mention))
            # If has 2 give 3
            elif warnmember.guild.get_role(742953920225214584) in warnmember.roles:
                await warnmember.add_roles(warnmember.guild.get_role(742953961014689842))
                await message.channel.send("{} now has 3 strikes".format(warnmember.mention))
            # If has 1 give 2
            elif warnmember.guild.get_role(742953865439215656) in warnmember.roles:
                await warnmember.add_roles(warnmember.guild.get_role(742953920225214584))
                await message.channel.send("{} now has 2 strikes".format(warnmember.mention))
            # If none give one
            else:
                await warnmember.add_roles(warnmember.guild.get_role(743205924059086918))
                await warnmember.add_roles(warnmember.guild.get_role(742953865439215656))
                await message.channel.send("{} now has 1 strike".format(warnmember.mention))

    if command.startswith(prefix + "removewarn") or command.startswith(prefix + "removestrike"):
        warnmember = message.mentions[0]
        if message.guild.get_role(736316470098657342) in message.author.roles or message.author.id == 369988289354006528:
            # If has 5 remove 5
            if warnmember.guild.get_role(742954067642548285) in warnmember.roles:
                await warnmember.remove_roles(warnmember.guild.get_role(742954067642548285))
                await message.channel.send("{} now has 4 strikes".format(warnmember.mention))
            # If has 4 remove 4
            elif warnmember.guild.get_role(742954033115037807) in warnmember.roles:
                await warnmember.remove_roles(warnmember.guild.get_role(742954033115037807))
                await message.channel.send("{} now has 3 strikes".format(warnmember.mention))
            # If has 3 remove 3
            elif warnmember.guild.get_role(742953961014689842) in warnmember.roles:
                await warnmember.remove_roles(warnmember.guild.get_role(742953961014689842))
                await message.channel.send("{} now has 2 strikes".format(warnmember.mention))
            # If has 2 remove 2
            elif warnmember.guild.get_role(742953920225214584) in warnmember.roles:
                await warnmember.remove_roles(warnmember.guild.get_role(742953920225214584))
                await message.channel.send("{} now has 1 strikes".format(warnmember.mention))
            # If has 1 remove 1
            elif warnmember.guild.get_role(742953865439215656) in warnmember.roles:
                await warnmember.remove_roles(warnmember.guild.get_role(743205924059086918))
                await warnmember.remove_roles(warnmember.guild.get_role(742953865439215656))
                await message.channel.send("{} now has no strikes".format(warnmember.mention))
            else:
                await message.channel.send("{} had no strikes".format(warnmember.mention))

    if command.startswith(prefix + "addrole"):
        roles = message.role_mentions
        if message.guild.get_role(736316470098657342) in message.author.roles or message.author.id == 369988289354006528 or message.author.id == 317456004843438082:
            for role in roles:
                for member in message.guild.members:
                    if not member.bot:
                        await member.add_roles(role)

    if command.startswith(prefix + "rockpaperscissors") or command.startswith(prefix + "rps"):
        challenger = message.author
        opponent = message.mentions[0]
        msg = await message.channel.send("Do you accept the challenge?")
        await msg.add_reaction("✅")
        def acceptsChallenge(reaction, user):
            return user == opponent and str(reaction.emoji) == '✅' and reaction.message.id == msg.id
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=300.0, check=acceptsChallenge)
        except asyncio.TimeoutError:
            await message.channel.send('Not accepted')
        else:
            await message.channel.send('Accepted')
            challengerMsg = await challenger.send("Choose Rock, Paper, or Scissors")
            await challengerMsg.add_reaction("✊")
            await challengerMsg.add_reaction("🖐️")
            await challengerMsg.add_reaction("✌️")
            def challengerCheck(reaction, user):
                return reaction.message.id == challengerMsg.id and user == challenger and (str(reaction.emoji) == '✊' or str(reaction.emoji) == '🖐️' or str(reaction.emoji) == '✌️')
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=challengerCheck)
            except asyncio.TimeoutError:
                await challengerMsg.channel.send('Timed out')
            else:
                await challengerMsg.channel.send('Done')
                challengerEmote = str(reaction.emoji)
            opponentMsg = await opponent.send("Choose Rock, Paper, or Scissors")
            await opponentMsg.add_reaction("✊")
            await opponentMsg.add_reaction("🖐️")
            await opponentMsg.add_reaction("✌️")
            def opponentCheck(reaction, user):
                return reaction.message.id == opponentMsg.id and user == opponent and (str(reaction.emoji) == '✊' or str(reaction.emoji) == '🖐️' or str(reaction.emoji) == '✌️')
            try:
                reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=opponentCheck)
            except asyncio.TimeoutError:
                await opponentMsg.channel.send('Timed out')
            else:
                await opponentMsg.channel.send('Done')
                opponentEmote = str(reaction.emoji)
            if challengerEmote == "✊":
                if opponentEmote == "✊":
                    await message.channel.send("Its a tie")
                if opponentEmote == "🖐️":
                    await message.channel.send("{} won".format(opponent.mention))
                if opponentEmote == "✌️":
                    await message.channel.send("{} won".format(challenger.mention))
            elif challengerEmote == "🖐️":
                if opponentEmote == "✊":
                    await message.channel.send("{} won".format(challenger.mention))
                if opponentEmote == "🖐️":
                    await message.channel.send("Its a tie")
                if opponentEmote == "✌️":
                    await message.channel.send("{} won".format(opponent.mention))
            elif challengerEmote == "✌️":
                if opponentEmote == "✊":
                    await message.channel.send("{} won".format(opponent.mention))
                if opponentEmote == "🖐️":
                    await message.channel.send("{} won".format(challenger.mention))
                if opponentEmote == "✌️":
                    await message.channel.send("Its a tie")

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
        await member.guild.get_channel(739647916905332846).send("{} has joined.\n{}".format(member.mention, member.guild.get_role(736316470098657342).mention))
        await member.add_roles(member.guild.get_role(743206825176072345), member.guild.get_role(743206597387485324))
        bot.memberCount+=1
    print(member.name + " Joined")

@bot.event
async def on_member_leave(member):
    # Ping welcomer and consulate when a new member joins the server
    if member.bot == False:
        bot.memberCount-=1
    print(member.nick + " Left")



# Reads the enviorment variable token for the token value
# To set it on windows do set TOKEN=token
# U can also make that permanent by using Windows search and searching for environment variables and adding it as one
# linux u can set it with export TOKEN=token
# Macos is probs the same as linux

token = str(os.getenv('TOKEN'))
bot.run(token)
