import discord
from discord.utils import get
import asyncio
import os
import random
import collections
import datetime
import math
import traceback
import inspect
from discord.ext import commands
from discord.ext import tasks
import ast
import requests

amazonlinks = ['https://www.amazon.com/dp/B01JKD4HYC/',
               'https://www.amazon.com/dp/B07QTHK8K9/',
               'https://www.amazon.com/dp/045149492X/',
               'https://www.amazon.com/dp/1091069387/',
               'https://www.amazon.com/dp/B00MRJ8GXK/',
               'https://www.amazon.com/dp/B071CFZ4BD/',
               'https://www.amazon.com/dp/B01GSOTFMA/',
               'https://www.amazon.com/dp/B07HGYVM55/',
               'https://www.amazon.com/dp/B001K3A45M/',
               'https://www.amazon.com/dp/B07CVKHCLR/',
               'https://www.amazon.com/dp/B07SHP29DM/',
               'https://www.amazon.com/dp/B075KTTKXS/',
               'https://www.amazon.com/dp/B01I2NXNE6/',
               'https://www.amazon.com/dp/B074RCV4HQ/',
               'https://www.amazon.com/dp/B072L3GMZV/',
               'https://www.amazon.com/dp/B07HKSTWBX/',
               'https://www.amazon.com/dp/B0837JN2FC/']
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

prefix = "c?"

randNum = random.random()
bot = commands.Bot(command_prefix=prefix, help_command=None, case_insensitive=True)

async def is_eva(ctx):
    return ctx.author.id == 369988289354006528

# Activity
@tasks.loop(seconds=10)
async def checkSuggestions():
    async for message in bot.get_channel(737807052625412208).history(oldest_first=True):
        if get(message.reactions, emoji="✅") and get(message.reactions, emoji="❌"):
            approvalsObject=get(message.reactions, emoji="✅")
            denialsObject=get(message.reactions, emoji="❌")
            approvals=approvalsObject.count-(bot.user in set(await approvalsObject.users().flatten()))      #gets # of yes reactions that isn't the bot
            denials=denialsObject.count-(bot.user in set(await denialsObject.users().flatten()))            #gets # of no reactions that isn't the bot
            timeLimit=datetime.timedelta(seconds=3600*(bot.memberCount)/abs(approvals**2-denials**2))       #complicated unnecessary math
            if (message.created_at.utcnow()-message.created_at)>timeLimit:
                files = []
                url = ""
                for each in message.attachments:
                    files.append(await each.to_file())
                if len(files) > 0:
                    fileMessage = await bot.get_guild(700359436203458581).get_channel(718277944153210961).send(files=files)
                    url = f"{fileMessage.attachments[0].url}\n"
                if approvals>denials:
                    print("✅ Approved: \n" + message.content)
                    try:
                        contents = message.clean_content.split("\n", 1)
                        await addCard("5f4d3b664357e92fc9968695", f"{contents[0]}", f"{contents[1]}\n{url}\nSuggested By: {message.author}", ["5f4d59315382c2827ea0d0a9"])
                    except:
                        await addCard("5f4d3b664357e92fc9968695", f"{message.clean_content}", f"{url}\nSuggested By: {message.author}", ["5f4d59315382c2827ea0d0a9"])
                else:
                    print("❌ Denied: \n" + message.content)
                    try:
                        contents = message.clean_content.split("\n", 1)
                        await addCard("5f4d577c418ce413102db964", f"{contents[0]}", f"{contents[1]}\n{url}\n\nSuggested By: {message.author}")
                    except:
                        await addCard("5f4d577c418ce413102db964", f"{message.clean_content}", f"{url}\nSuggested By: {message.author}")
                await message.delete()


@bot.event
async def on_ready():
    # Set Status
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="c?"))
    bot.memberCount=len([m for m in bot.get_guild(736306540671271036).members if not m.bot])
    checkSuggestions.start()
    # Send bot online notices
    print("Bot is online. Instance ID is " + str(randNum))
    embedVar=discord.Embed(title=":green_circle: Bot is online", color=0x00ff62)
    embedVar.add_field(name="Instance ID:", value= randNum, inline=True)
    await bot.get_channel(740049560591925362).send(embed=embedVar)

async def addCard(listID, name, desc, labels=None):
    query = {
        'key': '56e5e4a9cc439b5d1eb95c16bcc67a13',
        'token': 'e13a723dc94eacf48918fdf7f0c9910b6dd54f319d18d84af4678e364af6e669',
        'idList': listID,
        'name': name,
        'desc': desc,
        "idLabels": labels,
    }

    requests.request(
        "POST",
        "https://api.trello.com/1/cards",
        params=query
    )

async def getLine(fileName,lineNum):
    fh=open(fileName)
    for i, row in enumerate(fh): 
        if i+1==lineNum: 
            return row

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


@bot.command(name="eval")
@commands.check(is_eva)
async def eval_fn(ctx, *, cmd):
    """Evaluates input.
    Input is interpreted as newline seperated statements.
    If the last statement is an expression, that is the return value.
    Usable globals:
      - `bot`: the bot instance
      - `discord`: the discord module
      - `commands`: the discord.ext.commands module
      - `ctx`: the invokation context
      - `__import__`: the builtin `__import__` function
    Such that `>eval 1 + 1` gives `2` as the result.
    The following invokation will cause the bot to send the text '9'
    to the channel of invokation and return '3' as the result of evaluating
    >eval ```
    a = 1 + 2
    b = a * 2
    await ctx.send(a + b)
    a
    ```
    """
    fn_name = "_eval_expr"

    cmd = cmd.strip("` ")

    # add a layer of indentation
    cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

    # wrap in async def body
    body = f"async def {fn_name}():\n{cmd}"

    parsed = ast.parse(body)
    body = parsed.body[0].body

    insert_returns(body)

    env = {
        'bot': ctx.bot,
        'discord': discord,
        'commands': commands,
        'ctx': ctx,
        '__import__': __import__
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)

    result = (await eval(f"{fn_name}()", env))
    await ctx.send(f"```{result}```")

@bot.command(name='test')
async def test(ctx):
    print("Test Called")
    embedVar=discord.Embed(title="[ID]", description= str(randNum), color=0xd42027)
    await ctx.send(embed=embedVar)

@bot.command(name='info')
async def info(ctx):
    print("Info Called")
    embedVar =discord.Embed(title="Cranberry", description="Custom bot developed for a wide variety of servers.", color=0xd42027)
    embedVar.set_thumbnail(url="https://media.discordapp.net/attachments/738951182969602078/755560640076185671/logo640.png")
    embedVar.add_field(name="Version -", value="2.0.1", inline=True)
    embedVar.add_field(name="Contributors -", value="evalyn#8883, pupo#0001, MrMeme#5096", inline=True)
    embedVar.set_footer(text="Any questions? DM one of the contributors!")
    await ctx.send(embed=embedVar)

@bot.command(name="servers")
async def server(ctx):    
    print("Server Called")
    embedVar=discord.Embed(title="List of current servers.", description="Displaying the list of servers that Cranberry is in. ") #DONT CHANGE
    embedVar.set_thumbnail(url="https://media.discordapp.net/attachments/738951182969602078/755560640076185671/logo640.png") #DONT CHANGE
    for guild in bot.guilds:
        embedVar.add_field(name=guild.name, value= guild.created_at.strftime("%b %d, %Y"), inline=False)
    await ctx.send(embed=embedVar)

@bot.command(name="help")
async def serverHelp(ctx):
    print("Help Called")
    embedVar=discord.Embed(title="Cranberry Command List", description="List containing all bot commands.", color=0xd42027)
    embedVar.set_thumbnail(url="https://media.discordapp.net/attachments/738951182969602078/755560640076185671/logo640.png")
    num_lines = sum(1 for line in open('help.txt'))
    for helpNum in range((num_lines//2)):
        embedVar.add_field(name=await getLine('help.txt',2*helpNum+1), value=await getLine('help.txt',2*helpNum+2), inline=False)
    embedVar.set_footer(text="Any questions? Ask one of the contributors!")
    await ctx.send(embed=embedVar)

@bot.command(name="coinflip", aliases=['cf'])
async def coinflip(ctx):
    flipside = bool(random.getrandbits(1))
    if (flipside):
        flipside = "Heads"
    else:
        flipside = "Tails"
    print("Coin Flipped and Landed on {}".format(flipside))
    await ctx.send("> The coin flipped and landed on {}".format(flipside))

@bot.command(name="rule")
async def rule(ctx, ruleNum : int):
    print("Rule {} Called".format(str(ruleNum)))
    if 1<=ruleNum<=9:
        embedVar = discord.Embed(title=await getLine("rules.txt",2*ruleNum-1), description=await getLine("rules.txt",2*ruleNum), color=0xd42027)
        await ctx.send(embed=embedVar)
    else:
        await ctx.send("Invalid Rule Number")

@bot.command(name="bubblewrap", aliases=['bw'])
async def bubbbleWrap(ctx, bubbleContents):
    bubble = f"||{bubbleContents}||"
    maxSize = 12
    dimensions = math.floor(math.sqrt(2000/len(bubble))) - 2
    if dimensions > maxSize:
        dimensions = maxSize
    bubbleGrid = ((bubble * dimensions) + "\n") * (dimensions)
    await ctx.send(bubbleGrid, allowed_mentions=discord.AllowedMentions(everyone=False, users=False, roles=False))

@bot.command(name="warn", aliases=["strike", "addwarn", "addstrike"])
@commands.has_any_role(736316576126468097) 
async def warn(ctx):
    warnmember = ctx.message.mentions[0]
    # If has 4 give 5 and warn
    if warnmember.guild.get_role(742954033115037807) in warnmember.roles:
        await warnmember.add_roles(warnmember.guild.get_role(742954067642548285))
        await ctx.send("{} now has 5 strikes".format(warnmember.mention))
    # If has 3 give 4
    elif warnmember.guild.get_role(742953961014689842) in warnmember.roles:
        await warnmember.add_roles(warnmember.guild.get_role(742954033115037807))
        await ctx.send("{} now has 4 strikes".format(warnmember.mention))
        # If has 2 give 3
    elif warnmember.guild.get_role(742953920225214584) in warnmember.roles:
        await warnmember.add_roles(warnmember.guild.get_role(742953961014689842))
        await ctx.send("{} now has 3 strikes".format(warnmember.mention))
    # If has 1 give 2
    elif warnmember.guild.get_role(742953865439215656) in warnmember.roles:
        await warnmember.add_roles(warnmember.guild.get_role(742953920225214584))
        await ctx.send("{} now has 2 strikes".format(warnmember.mention))
    # If none give one
    else:
        await warnmember.add_roles(warnmember.guild.get_role(743205924059086918))
        await warnmember.add_roles(warnmember.guild.get_role(742953865439215656))
        await ctx.send("{} now has 1 strike".format(warnmember.mention))

@bot.command(name="removewarn", aliases=["removestrike"])
@commands.has_any_role(736316576126468097) 
async def removewarn(ctx):
    warnmember = ctx.message.mentions[0]
    # If has 5 remove 5
    if warnmember.guild.get_role(742954067642548285) in warnmember.roles:
        await warnmember.remove_roles(warnmember.guild.get_role(742954067642548285))
        await ctx.send("{} now has 4 strikes".format(warnmember.mention))
    # If has 4 remove 4
    elif warnmember.guild.get_role(742954033115037807) in warnmember.roles:
        await warnmember.remove_roles(warnmember.guild.get_role(742954033115037807))
        await ctx.send("{} now has 3 strikes".format(warnmember.mention))
    # If has 3 remove 3
    elif warnmember.guild.get_role(742953961014689842) in warnmember.roles:
        await warnmember.remove_roles(warnmember.guild.get_role(742953961014689842))
        await ctx.send("{} now has 2 strikes".format(warnmember.mention))
    # If has 2 remove 2
    elif warnmember.guild.get_role(742953920225214584) in warnmember.roles:
        await warnmember.remove_roles(warnmember.guild.get_role(742953920225214584))
        await ctx.send("{} now has 1 strikes".format(warnmember.mention))
    # If has 1 remove 1
    elif warnmember.guild.get_role(742953865439215656) in warnmember.roles:
        await warnmember.remove_roles(warnmember.guild.get_role(743205924059086918))
        await warnmember.remove_roles(warnmember.guild.get_role(742953865439215656))
        await ctx.send("{} now has no strikes".format(warnmember.mention))
    else:
        await ctx.send("{} had no strikes".format(warnmember.mention))

@bot.command(name="addrole")
@commands.has_any_role(736316576126468097)
async def addrole(ctx, *roles):
    await ctx.send("Starting...")
    for role in roles:
        for member in ctx.guild.members:
            if not member.bot and not role in member.roles:
                await member.add_roles(ctx.guild.get_role(int(role)))
    await ctx.send("Done!")

@bot.command(name="rockpaperscissors", aliases=["rps"])
async def rps(ctx):
    if len(ctx.message.mentions) > 0:
        opponent=ctx.message.mentions[0]
        msg = await ctx.author.send("Choose Rock, Paper, Or Scissors")
        await msg.add_reaction("✊")
        await msg.add_reaction("🖐️")
        await msg.add_reaction("✌️")
        msg = await opponent.send("Choose Rock, Paper, Or Scissors")
        await msg.add_reaction("✊")
        await msg.add_reaction("🖐️")
        await msg.add_reaction("✌️")
        notResponded = [ctx.author, opponent]
        responses={ctx.author: "", opponent: ""}
        def check(reaction, user):
            if (reaction.emoji in ["✊", "🖐️", "✌️"]): return (user in notResponded)
        while notResponded:
            reaction, user = await bot.wait_for("reaction_add",timeout=60,check=check)
            notResponded.remove(user)
            responses[user] = reaction.emoji
        outcome = {"✊": {"🖐️": True, "✌️": False, "✊": "Tie"}, "🖐️": {"🖐️": "Tie", "✌️": True, "✊": False}, "✌️": {"🖐️": False, "✌️": "Tie", "✊": True}}
        result = outcome[responses[ctx.author]][responses[opponent]]
        print(result)
        if result == True:
            await ctx.send(f"{ctx.author.mention} Won!")
            return
        if result == False:
            await ctx.send(f"{opponent.mention} Won!")
            return
        else:
            await ctx.send("Its a tie")
            return
    else:
        msg = await ctx.send("Choose Rock, Paper, Or Scissors")
        await msg.add_reaction("✊")
        await msg.add_reaction("🖐️")
        await msg.add_reaction("✌️")
        def check(reaction, user):
            return (reaction.emoji in ["✊", "🖐️", "✌️"]) and (user == ctx.author)
        reaction, user = await bot.wait_for('reaction_add', timeout=60.0, check=check)
        rand = random.randint(0,2)
        if rand == 1:
            await ctx.send("You Win!")
        elif rand == 2:
            await ctx.send("You Lose!")
        else:
            await ctx.send("You Tied!")

@bot.command(name="guess")
async def guess(ctx):
    await ctx.send("Guess the number between 0-10 by typing it! (it will end once you guess correctly)")
    number = str(random.randint(1,10))
    def check(m):
        return m.content == number and m.channel == ctx.channel
    msg = await bot.wait_for('message', check=check)
    await ctx.send("Correct answer {.author}!".format(msg))

@bot.command(name="amazon")
async def amazon(ctx):
    await ctx.send(random.choice(amazonlinks))

@bot.command(name="embarrasme", aliases=["embarras"])
async def embarrasMe(ctx):
    await ctx.send(f"{random.choice(embarrass)} from {ctx.author.mention}")

@bot.command(name="vote")
@commands.has_role(736316576126468097) 
async def vote(ctx, url):
    ids = random.sample(range(1000,9999), bot.memberCount)
    await ctx.author.send('\n'.join(map(str, ids)))
    for member in ctx.guild.members:
        if not member.bot:
            id = ids.pop(0)
            #print(f"Please Vote on {url}, your token is {id}")
            await member.send(f"Please Vote on {url}, your token is `{id}`, please enter it in the form.")

@bot.command(name="connect4", aliases=["c4"])
async def connect4(ctx, opponent : discord.Member):
    print(opponent.display_name)
    board = [[0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,],
            [0,0,0,0,0,0,0,]]
    turnID = {
        0: ctx.author.id,
        1: opponent.id,
    }
    getcol = {
        753090179467706448: 0,
        753090179547398254: 1,
        753090179497066516: 2,
        753090179056795720: 3,
        753090179178299476: 4,
        753090179643867156: 5,
        753090179484352573: 6,
    }
    turns = 1
    msg = await ctx.send(draw(board, ctx.author.id, opponent.id))
    for emote in [753090179467706448,753090179547398254,753090179497066516,753090179056795720,753090179178299476,753090179643867156,753090179484352573]:
        await msg.add_reaction(bot.get_emoji(emote))
    turnMsg = await ctx.send(f"{bot.get_user(turnID[turns % 2]).mention}, it's your turn!")
    while True:
        try:
            def check(reaction, user):
                return user.id == turnID[turns % 2] and reaction.custom_emoji
            reaction, user = await bot.wait_for('reaction_add', timeout=300, check=check)
        except asyncio.TimeoutError:
            await ctx.send('Game Timed Out')
            break
        else:
            try:
                await turnMsg.delete()
            except:
                pass
            await reaction.remove(user)
            col = getcol[reaction.emoji.id]
            if 0 not in board[0]:
                await ctx.send("The Board is full, Game Over")
                break
            if not board[0][col] == 0:
                await ctx.send("The slot is full, drop in a different one")
                continue
            board = fall(board, col, user)
            await msg.edit(content=f"{draw(board, ctx.author.id, opponent.id)}")
            if checkWin(board, user.id):
                await ctx.send(f"{user.mention} Won!")
                break
            turns+=1
            turnMsg = await ctx.send(f"{bot.get_user(turnID[turns % 2]).mention} it's your turn!")

def fall(board, col, user):
    row = 0
    while True:
        if board[row][col] == 0:
            try:
                if board[row+1][col] == 0:
                    row+=1
                else:
                    board[row][col] = user.id
                    return board
            except:
                board[row][col] = user.id
                return board

def draw(board, challenger, opponent):
    colors = {
        challenger: "<:red:753090683220394114>",
        opponent: "<:blue:753090615784505404>",
        0: "<:blank:752272555259461692>",
    }
    output = ""
    for a in range(6):
        for b in range(7):
            output = f"{output}{colors[board[a][b]]}"
        output = f"{output}\n"
    output = f"<:red:753090683220394114> {bot.get_user(challenger).mention} -vs- <:blue:753090615784505404> {bot.get_user(opponent).mention}\n\n{output}<:c41:753090178842886175><:c42:753090178750611528><:c43:753090178448490538><:c44:753090178868052028><:c45:753090178779840512><:c46:753090178796486738><:c47:753090178775646208>"
    return output

def checkWin(board, piece):
    for c in range(7-3):
        for r in range(6):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                print("horozinatl")
                return True

    # Check vertical locations for win
    for c in range(7):
        for r in range(6-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                print("vertical")
                return True

    # Check positively sloped diaganols
    for c in range(7-3):
        for r in range(6-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                print("pos slotpe")
                return True

    # Check negatively sloped diaganols
    for c in range(7-3):
        for r in range(3, 6):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                print("negativ slops")
                return True

@bot.event
async def on_message(message):
    # Add reaction to the suggestions
    if message.channel.id == 737807052625412208:
        await message.add_reaction("✅")
        await message.add_reaction("❌")
        print("New Suggestion: " + message.content)

    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)

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
        with open("roles.txt") as file_in:
            for line in file_in:
                await member.add_roles(member.guild.get_role(int(line)))
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
