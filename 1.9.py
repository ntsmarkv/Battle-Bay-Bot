import discord
from discord.ext import commands
import youtube_dl
import json
import time
import aiohttp
import asyncio
import async_timeout
from threading import Timer
import random
import timeit
import traceback
import logging


TOKEN = ''
CLIENT_ID = 'e3te3c43l83eqjeojupne0se5t681s'
cooldowns = {}
description = '''Battle Bay Bot
You can visit us Online @: http://battlebaydiscord.xyz/'''
startup_extensions = ["Music"]
#startup_extensions = ["run"]
#startup_extensions = ["config"]

bot = commands.Bot(command_prefix='!', description=description)

chat_filter = ["SHIT", "FUCK", "ASS", "pineapple"]
bypass_list = []

class EventMod():
    def __init__(self, channel, timeout, text, isEmbed=False):
        self.channel = channel
        self.timeout = timeout
        self.text = text
        self.thread = None
        self.isEmbed = isEmbed

    def handle_function(self):
        if self.text is not None:
            if self.isEmbed:
                asyncio.run_coroutine_threadsafe(bot.send_message(self.channel, embed=discord.Embed(colour=discord.Colour(0xFAA61A), description="**" + self.text + "**")), bot.loop)
            else:
                asyncio.run_coroutine_threadsafe(bot.send_message(self.channel, self.text), bot.loop)

        self.thread = Timer(self.timeout, self.handle_function)
        self.thread.start()

    def start(self):
        self.handle_function()

    def cancel(self):
        self.thread.cancel()

async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


async def backgroundStream(loop):
    await bot.wait_until_ready()
    while not bot.is_closed:
        async with aiohttp.ClientSession(loop=loop) as session:
            upStreams = []

            with open('streams.json') as f:
                streams = json.load(f)
            for x in streams:
                if streams[x][2] == "T":
                    url = 'https://api.twitch.tv/kraken/streams/' + streams[x][0] + '?client_id=e3te3c43l83eqjeojupne0se5t681s'
                    contents = await fetch(session, url)
                    data = json.loads(contents)
                    if data["stream"] == None:
                        pass
                    else:
                        upStreams.append(x)
                        personId = x
                        with open('userdata.json') as f:
                            data = json.load(f)
                            if personId in data:
                                olddata = data[personId]
                                newdata = olddata + 15
                                newformatted = {personId: newdata}
                                data.update(newformatted)
                                with open('userdata.json', 'w') as f:
                                    json.dump(data, f)
                if streams[x][2] == "Y":
                    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=' + streams[x][1] + '&type=video&eventType=live&key=AIzaSyBRAFpLN6lhv20hXvg-U-EjVqJ_XUmuIIA'

                    contents = await fetch(session, url)
                    data = json.loads(contents)

                    if len(data["items"]) > 0:
                        upStreams.append(x)
                        personId = x
                        with open('userdata.json') as f:
                            data = json.load(f)
                            if personId in data:
                                olddata = data[personId]
                                newdata = olddata + 15
                                newformatted = {personId: newdata}
                                data.update(newformatted)
                                with open('userdata.json', 'w') as f:
                                    json.dump(data, f)
            finalMessage = ":red_circle: Current Live Streams:red_circle: \n"
            counter = 1
            for x in upStreams:
                if streams[x][2] == "T":
                    finalMessage = finalMessage + str(counter) + ") <@" + x + "> is live at: " + streams[x][1] + "\n"
                    counter += 1
                if streams[x][2] == "Y":
                    finalMessage = finalMessage + str(counter) + ") <@" + x + "> is live at: " + "https://www.youtube.com/channel/" + streams[x][1] + "\n"
                    counter += 1
            if len(upStreams) >= 1:
                for x in bot.servers:
                    embed = discord.Embed(colour=discord.Colour(0xFAA61A), description=finalMessage)
                    await bot.send_message(discord.utils.get(x.channels, position=0, type=discord.ChannelType.text), embed=embed)

        await asyncio.sleep(900)


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.get_cog("Moderator").setmessageofdayEventMod()

    await bot.change_presence(game=discord.Game(name='Waiting for Event', type=1))

#TODO
#Create !restart cmd


@bot.event
async def on_member_join(member):
    with open('userdata.json') as f:
        data = json.load(f)
    if member.id not in data:
        data.update({member.id: 1000})
        with open('userdata.json', 'w') as f:
            json.dump(data, f)

#    with open('users.json', 'r') as f:
 #       users = json.load(f)

  #  await update_data(users, member)

#    with open('users.json', 'w') as f:
 #       json.dump(users, f)
#    await bot.send_message(discord.utils.get(member.server.channels, type=discord.ChannelType.text), embed=discord.Embed(colour=discord.Colour(0xFAA61A), description="If you need help use; !help."))


@bot.event
async def on_command_error(error, ctx):
    if isinstance(error, commands.CommandOnCooldown):
        bot.send_message(ctx.message.channel, content='You get bbps every 24 hours!!! You have; %.2fs left! | Tip; You can donate your dailies to another member!' % error.retry_after)
    raise error  # re-raise the error so all the errors will still show up in console


@bot.event
async def on_message(message):
    if message.author.id not in cooldowns:
        newPerson = {message.author.id: time.time()}
        cooldowns.update(newPerson)
    else:
        oldTime = cooldowns[message.author.id]
        newTime = time.time()
        if newTime - oldTime > 60:
            newPerson = {message.author.id: time.time()}
            cooldowns.update(newPerson)
            location = str(message.channel)
            if location == "general" or location == "general-chat-room":
                with open('userdata.json') as f:
                    data = json.load(f)
                if message.author.id in data:
                    old = data[message.author.id]
                    new = old + 1
                    newPoints = {message.author.id: new}
                    data.update(newPoints)
                    with open('userdata.json', 'w') as f:
                        json.dump(data, f)

 #       with open('users.json', 'r') as f:
 #           users = json.load(f)
#
#        await update_data(users, message.author)
 #       await add_experience(users, message.author, 5)
  #      await level_up(users, message.author, message.channel)
   #     await add_bbp(users, message.author, 1)

#        with open('users.json', 'w') as f:
  #          json.dump(users, f)

    if message.content.startswith('!create'):
        writing = message.content
        splitUp = writing.split()
        with open('profiles.json') as f:
            profiles = json.load(f)
        splitUp.remove("!create")
        if splitUp[0].startswith('#'):
            newProfile = {message.author.id: splitUp}
            profiles.update(newProfile)
            with open('profiles.json', 'w') as f:
                json.dump(profiles, f)
        else:
            await bot.send_message(message.channel, "Please input a valid Battle Bay Tag! (with a #)")

    await bot.process_commands(message)

    if message.content.startswith('!background'):
        writing = message.content
        splitUp = writing.split()
        with open('background.json') as f:
            profiles = json.load(f)
        splitUp.remove("!background")
        if splitUp[0].startswith(':'):
            newProfile = {message.author.id: splitUp}
            profiles.update(newProfile)
            with open('background.json', 'w') as f:
                json.dump(profiles, f)
        else:
            await bot.send_message(message.channel, "You do not have access to this part.")

    await bot.process_commands(message)


async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 0
        users[user.id]['bbps'] = 1000


async def add_experience(users, user, exp):
    users[user.id]['experience'] += exp


async def add_bbp(users, user, bbps):
    users[user.id]['bbps'] += bbps


async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
#        await bot.send_message(user, '{}, You just leveled :up:!! You are now level {}'.format(user.mention, lvl_end))
        users[user.id]['level'] = lvl_end


class Member():
    """Anyone can run these commands!"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def ping(ctx):
        """Pong"""
        before = time.monotonic()
        await(await bot.ws.ping())
        after = time.monotonic()
        _ping = (after - before) * 1000
        await bot.say("**Trip FROM me to you-->** :ping_pong: **{0:.0f}ms**".format(_ping))
        await bot.say(ctx, "**Trip FROM Me to Rovio-->** :ping_pong: **{0:.0f}ms**".format(_ping))

    @commands.command(pass_context=True)
    async def profile(self, ctx, arg=None):
        """Shows the profile of the tagged person!"""
        if arg == None:
            member = ctx.message.author.id
            nickname = ctx.message.author.name
            membObj = ctx.message.author
        else:
            member = ctx.message.mentions[0].id
            nickname = ctx.message.mentions[0].name
            membObj = ctx.message.mentions[0]
        with open('profiles.json') as f:
            profiles = json.load(f)
        if member not in profiles:
            await bot.say("That person does not have a profile!")
        else:
            stuff = profiles[member]
            embed = discord.Embed(colour=discord.Colour(0xFAA61A), description="Battle Bay Tag **" + stuff[0] + "**")
            if len(stuff) == 2 or len(stuff) == 3:
                embed.set_image(url=stuff[1])
            embed.set_author(name=nickname, icon_url=membObj.avatar_url)
            await bot.say(embed=embed)
            if len(stuff) == 3:
                embed2 = discord.Embed(colour=discord.Colour(0xFAA61A))
                embed2.set_image(url=stuff[2])
                await bot.say(embed=embed2)

    @commands.command(pass_context=True)
    async def Introduction(self, ctx, arg=None):
        """Shows the Players Introduction of the tagged person!"""
        if arg == None:
            member = ctx.message.author.id
            nickname = ctx.message.author.name
            membObj = ctx.message.author
        else:
            member = ctx.message.mentions[0].id
            nickname = ctx.message.mentions[0].name
            membObj = ctx.message.mentions[0]
        with open('background.json') as f:
            profiles = json.load(f)
        if member not in profiles:
            await bot.say("That person does not have a Introduction!")
        else:
            stuff = profiles[member]
            embed = discord.Embed(colour=discord.Colour(0xFAA61A), description="BIO **" + stuff[0] + "**")
            if len(stuff) == 2 or len(stuff) == 3:
                embed.set_image(url=stuff[1])
            embed.set_author(name=nickname, icon_url=membObj.avatar_url)
            await bot.say(embed=embed)
            if len(stuff) == 3:
                embed2 = discord.Embed(colour=discord.Colour(0xFAA61A))
                embed2.set_image(url=stuff[2])
                await bot.say(embed=embed2)


#    @commands.command(pass_context=True)
#    async def getupdate(self, ctx):
#        """"""
#        await bot.say("___**Checking for update:**___ ...........................................................")
#        await bot.say("___**Accessing Servers:**___ PLEASE WAIT!! ................")
#        await bot.say("___**Game Version**___ - **4.2.20442** January 4th, 2019 Possibly found, Attemtempting to get update")
#        await bot.say("___**Android Version**___ - **Need Android Versions Check DM** For further information, as this is just a test.")

    @commands.command(pass_context=True)
    async def memberlist(self, ctx):
        """Shows how many users are using the bot"""
        await bot.say("Members earning points: **" + str(len(set(bot.get_all_members()))) + "**.")

    @commands.command(pass_context=True)
    async def communityinfo(self, ctx):
        """Shows Information about the Battle Bay Community"""
        await bot.say("___**Community Information about Battle Bay**___")
        await bot.say("~22,411 Active Battlers!")
        await bot.say("1,649 Discord Members! (12.3%)+2.3%")
        await bot.say("14,943 Forum Members (~10874 Active)")
        await bot.say("___**Game Version**___ - **4.1.21728** December 3, 2018")
#        await bot.say("___**Top 7 Guilds**___")
#        await bot.say("THE DREAM TEAM [TDTE]")
#        await bot.say("Silencio [75002]")
#        await bot.say("Nightmare Clan [-NC-]")
#        await bot.say("[HXD]")
#        await bot.say("Be Boozled [BEBZ1]")
#        await bot.say("Guardians of the Seas [GSEAS]")
#        await bot.say("Nightma2e Clan [-NC2-]")
#        await bot.say("**6th of October, 2018**")

#    @commands.command(pass_context=True)
#    async def servers(self):
#        await bot.say("We are on **" + str(len(self.bot.servers)) + "** servers.")

    @commands.command(pass_context=True)
    async def join(self, ctx):
        """Used to start earning points!"""
        member = ctx.message.author
        with open('userdata.json') as f:
            data = json.load(f)
        if member.id not in data:
            newMember = {member.id: 1000}
            data.update(newMember)
            with open('userdata.json', 'w') as f:
                json.dump(data, f)
                await bot.say("Successfully merged into database!")
        else:
            await bot.say("Sorry, you are already in the database!")

    @commands.command(pass_context=True)
    async def messageofday(self, ctx):
        """Shows the message of the day"""
        with open('messageofday.json') as f:
            await bot.say(embed=discord.Embed(colour=discord.Colour(0xFAA61A), description=""+ json.load(f)["text"] +""))

    @commands.command(pass_context=True)
    async def points(self, ctx, useless=None):
        """Used to check a user's bbps; if nobody is tagged your points are checked"""
        if useless == None:
            personId = ctx.message.author.id
        else:
            mentions = ctx.message.mentions
            person = mentions[0]
            personId = person.id
        with open('userdata.json') as f:
            data = json.load(f)
        if personId in data:
            olddata = data[personId]
            await bot.say("<@" + personId + "> " + " has **" + str(olddata) + "** BBPs!")
        else:
            await bot.say("Sorry, that user is not in the database!")

    @commands.command()
    async def create(self):
        """!create #BBTAG <picurl1.com> <picurl2.com>"""

    # this does nothing; just so that command shows up in help message and the client doesn't throw an error

    @commands.command()
    async def background(self):
        """!create #BBTAG <picurl1.com> <picurl2.com>"""

    # this does nothing; just so that command shows up in help message and the client doesn't throw an error

    @commands.command(pass_context=True)
    async def rank(self, ctx, arg=None):
        """Joins a rank and adds you into that role"""

        async def clearRoles():
            roleList = []
            roleList.append(discord.utils.get(ctx.message.server.roles, name='Enforcer'))
            roleList.append(discord.utils.get(ctx.message.server.roles, name='Defender'))
            roleList.append(discord.utils.get(ctx.message.server.roles, name='Shooter'))
            roleList.append(discord.utils.get(ctx.message.server.roles, name='Fixer'))
            roleList.append(discord.utils.get(ctx.message.server.roles, name='Speeder'))
            roleList.append(discord.utils.get(ctx.message.server.roles, name='Interceptor'))
            roleList.append(discord.utils.get(ctx.message.server.roles, name='Reaper'))
            roleList.append(discord.utils.get(ctx.message.server.roles, name='Guardian'))

            for grp in roleList:
                await bot.remove_roles(ctx.message.author, *roleList)

        if arg == None:
            await bot.say("Please pick a rank to join! (!rank speeder | !rank interceptor | !rank reaper | etc)")
        else:
            with open('groups.json') as f:
                groups = json.load(f)
            sender = ctx.message.author.id
            group = ""
            if arg == "defender":
                group = ":defender:"
                role = discord.utils.get(ctx.message.server.roles, name='Defender')
                await bot.add_roles(ctx.message.author, role)

            elif arg == "enforcer":
                group = ":enforcer:"
                role = discord.utils.get(ctx.message.server.roles, name='Enforcer')
                await bot.add_roles(ctx.message.author, role)
            elif arg == "fixer":
                group = ":fixer:"
                role = discord.utils.get(ctx.message.server.roles, name='Fixer')
                await bot.add_roles(ctx.message.author, role)
            elif arg == "shooter":
                group = ":shooter:"
                role = discord.utils.get(ctx.message.server.roles, name='Shooter')
                await bot.add_roles(ctx.message.author, role)
            elif arg == "speeder":
                group = ":speeder:"
                role = discord.utils.get(ctx.message.server.roles, name='Speeder')
                await bot.add_roles(ctx.message.author, role)
            elif arg == "interceptor":
                group = ":Interceptor:"
                role = discord.utils.get(ctx.message.server.roles, name='Interceptor')
                await bot.add_roles(ctx.message.author, role)
            elif arg == "reaper":
                group = ":Reaper:"
                role = discord.utils.get(ctx.message.server.roles, name='Reaper')
                await bot.add_roles(ctx.message.author, role)
            elif arg == "guardian":
                group = ":Guardian:"
                role = discord.utils.get(ctx.message.server.roles, name='Guardian')
                await bot.add_roles(ctx.message.author, role)
            else:
                await bot.say("That is not a valid rank!")
                return
            newGroup = {sender: group}
            groups.update(newGroup)
            with open('groups.json', 'w') as f:
                json.dump(groups, f)

            await bot.say("Joined the " + arg + " rank!")

    @commands.command(pass_context=True)
    async def setinfamy(self, ctx, arg=None):
        """Sets your infamy level"""

        argu = int(arg)

        async def upd():
            with open('infamy.json') as f:
                infamies = json.load(f)
            datas = [argu, time.time()]
            newInfamy = {ctx.message.author.id: datas}
            infamies.update(newInfamy)
            with open('infamy.json', 'w') as f:
                json.dump(infamies, f)
            await bot.say("Your infamy has been set to " + str(argu))

        if arg == None or int(arg) < 0 or int(arg) > 6500:
            await bot.say("Please give a valid infamy value!")
            return

        else:
            await upd()

    @commands.command(pass_context=True)
    async def infamy(self, ctx, arg=None):
        """Checks your or someone else's infamy"""
        with open('infamy.json') as f:
            infamies = json.load(f)
        if arg == None:
            personId = ctx.message.author.id
        else:
            personId = ctx.message.mentions[0].id
        info = infamies[personId]
        pastTime = info[1]
        current = time.time()
        difference = current - pastTime
        m, s = divmod(difference, 60)
        h, m = divmod(m, 60)
        await bot.say("<@" + personId + "> is at: " + str(info[0]) + " infamy, since" + "  %d hours %02d minutes %02d seconds" % (h, m, s) + " ago!")

    @commands.command(pass_context=True)
    async def setgs(self, ctx, arg=None):
        """Sets your Gearscore level"""

        argu = int(arg)

        async def upd():
            with open('gearscore.json') as f:
                infamies = json.load(f)
            datas = [argu, time.time()]
            newInfamy = {ctx.message.author.id: datas}
            infamies.update(newInfamy)
            with open('gearscore.json', 'w') as f:
                json.dump(infamies, f)
            await bot.say("Your Gearscore has been set to " + str(argu))

        if arg == None or int(arg) < 0 or int(arg) > 25000:
            await bot.say("Please give a valid Gearscore value!")
            return

        else:
            await upd()

    @commands.command(pass_context=True)
    async def gs(self, ctx, arg=None):
        """Checks your or someone else's Gearscore"""
        with open('gearscore.json') as f:
            infamies = json.load(f)
        if arg == None:
            personId = ctx.message.author.id
        else:
            personId = ctx.message.mentions[0].id
        info = infamies[personId]
        pastTime = info[1]
        current = time.time()
        difference = current - pastTime
        m, s = divmod(difference, 60)
        h, m = divmod(m, 60)
        await bot.say("<@" + personId + "> is at: " + str(info[0]) + " Gearsore, since" + "  %d hours %02d minutes %02d seconds" % (h, m, s) + " ago!")



    @commands.command(pass_context=True)
    async def addstream(self, ctx, *, arg=None):
        """Adds a twitch stream! Please do !help addstream
        **!addstream <TwitchUsername> |<TwitchURL> |T** for Twitch Streams
        **!addstream <Youtube Username> |<ChannelID> |Y** for YouTube Streams
        ALL PARTS ARE NECESSARY AND MAKE SURE PARAMETERS ARE SPLIT BY A SPACE THEN VERTICAL LINE
        You can get your YouTube channel ID by going to your YouTube channel page and copying it from the URL bar!"""
        with open('streams.json') as f:
            streams = json.load(f)

        words = arg.split(" |")
        if len(words) != 3:
            await bot.say("Please give a valid input!")
            return

        else:
            personId = ctx.message.author.id
            stream = [words[0], words[1], words[2]]
            newData = {personId: stream}
            streams.update(newData)
            with open('streams.json', 'w') as f:
                json.dump(streams, f)
            await bot.say("Successfully updated stream!")

    @commands.command(pass_context=True)
    async def livestreams(self, ctx):
        """Shows all current livestreams! Use this if you go live!"""
        with open('streams.json') as f:
            streams = json.load(f)
        upStreams = []
        async with aiohttp.ClientSession(loop=bot.loop) as session:
            for x in streams:
                if streams[x][2] == "T":
                    url = 'https://api.twitch.tv/kraken/streams/' + streams[x][0] + '?client_id=e3te3c43l83eqjeojupne0se5t681s'
                    contents = await fetch(session, url)
                    data = json.loads(contents)
                    if data["stream"] == None:
                        pass
                    else:
                        upStreams.append(x)

                if streams[x][2] == "Y":
                    url = 'https://www.googleapis.com/youtube/v3/search?part=snippet&channelId=' + streams[x][1] + '&type=video&eventType=live&key=AIzaSyBRAFpLN6lhv20hXvg-U-EjVqJ_XUmuIIA'

                    contents = await fetch(session, url)
                    data = json.loads(contents)

                    if len(data["items"]) > 0:
                        upStreams.append(x)

            finalMessage = ":red_circle: Current Live Streams:red_circle: \n"
            counter = 1
            for x in upStreams:
                if streams[x][2] == "T":
                    finalMessage = finalMessage + str(counter) + ") <@" + x + "> is live at: " + streams[x][1] + "\n"
                    counter += 1
                if streams[x][2] == "Y":
                    finalMessage = finalMessage + str(
                        counter) + ") <@" + x + "> is live at: " + "https://www.youtube.com/channel/" + streams[x][
                                       1] + "\n"
                    counter += 1
            if len(upStreams) >= 1:
                embed = discord.Embed(colour=discord.Colour(0xFAA61A), description=finalMessage)
                await bot.send_message(ctx.message.channel, embed=embed)

    @commands.command(pass_context=True)
    async def achievements(self, ctx, arg=None):
        """Used to view people's or your achievements."""
        if arg == None:
            personId = ctx.message.author.id
        else:
            personId = ctx.message.mentions[0].id
        with open('badges.json') as f:
            badges = json.load(f)
        badgeUrl = badges[personId]
        embed = discord.Embed(colour=discord.Colour(0xFAA61A))
        embed.set_image(url=badgeUrl)
        await bot.send_message(ctx.message.channel, embed=embed)


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            exc = '{}:  {}'.format(type(e).__name__, e)
            print('Failed to load Extension {}\n{}'.format(extension, exc))


class Moderator():
    """Only Moderators can run these commands!"""

    def __init__(self, bot):
        self.bot = bot
        self.votes = []
        self.messageofdaymod = None
        self.eventmod = dict()

    @commands.command(pass_context=True)
    async def addpoints(self, ctx, useless, value: int):
        """Adds points to an account; used '!addpoints @username xxx' """
        roles = ctx.message.author.roles
        role = discord.utils.get(ctx.message.server.roles, name='[BB19218BMOD]')
        if role in roles:
            mentions = ctx.message.mentions
            person = mentions[0]
            personId = person.id
            with open('userdata.json') as f:
                data = json.load(f)
            if personId in data:
                olddata = data[personId]
                newdata = olddata + value
                newformatted = {personId: newdata}
                data.update(newformatted)
                with open('userdata.json', 'w') as f:
                    json.dump(data, f)
                await bot.say("Added " + str(value) + " points!")
            else:
                await bot.say("Sorry, that user is not in the database!")
        else:
            await bot.say("You must be a Moderator in order to use this command.  :robot:")

    @commands.command(pass_context=True)
    async def setpoints(self, ctx, useless, value: int):
        """Sets points of an account; used '!setpoints @username xxx' """
        mentions = ctx.message.mentions
        person = mentions[0]
        personId = person.id
        roles = ctx.message.author.roles
        role = discord.utils.get(ctx.message.server.roles, name='[BB19218BMOD]')
        if role in roles:
            with open('userdata.json') as f:
                data = json.load(f)
            if personId in data:
                # olddata = data[personId]
                # print(olddata)
                # print(value)
                newdata = value
                newformatted = {personId: newdata}
                data.update(newformatted)
                with open('userdata.json', 'w') as f:
                    json.dump(data, f)
                await bot.say("Points set to: " + str(value))
            else:
                await bot.say("Sorry, that user is not in the database!")
        else:
            await bot.say("You must be a Moderator in order to use this command.  :robot:")

    @commands.command(pass_context=True)
    async def updateachievement(self, ctx, arg=None, arg2=None):
        """Only for Mods to change badges!"""
        roles = ctx.message.author.roles
        role = discord.utils.get(ctx.message.server.roles, name='[BB19218BMOD]')
        mentions = ctx.message.raw_mentions
        person = mentions[0]
        if role in roles:
            with open('badges.json') as f:
                badges = json.load(f)
            if arg2 == None:
                await bot.say("Please give a valid input!")
                return
            else:
                personId = person
                newBadge = {personId: arg2}
                badges.update(newBadge)
                with open('badges.json', 'w') as f:
                    json.dump(badges, f)
                await bot.say("Successfully updated achievement!")
        else:
            await bot.say("You must be a Moderator in order to use this command.  :robot:")

    @commands.command(pass_context=True)
    async def changeinfamy(self, ctx, arg=None, arg2=None):
        """Only for Mods to change infamy!"""
        roles = ctx.message.author.roles
        role = discord.utils.get(ctx.message.server.roles, name='[BB19218BMOD]')
        mentions = ctx.message.raw_mentions
        person = mentions[0]
        if role in roles:
            argu = int(arg2)

            async def upd():
                with open('infamy.json') as f:
                    infamies = json.load(f)
                datas = [argu, time.time()]
                newInfamy = {ctx.message.mentions[0].id: datas}
                infamies.update(newInfamy)
                with open('infamy.json', 'w') as f:
                    json.dump(infamies, f)
                await bot.say("Infamy has been set to " + str(argu))

            if arg == None:
                await bot.say("Please give a valid infamy value!")
                return
            else:
                await upd()
        else:
            await bot.say("You must be a Moderator in order to use this command.  :robot:")

    @commands.command(pass_context=True)
    async def prune(self, ctx, user=None, value=None):
        """Prunes x messages back; !prune @username x"""
        roles = ctx.message.author.roles
        role = discord.utils.get(ctx.message.server.roles, name='[BB19218BMOD]')
        mentions = ctx.message.raw_mentions
        person = mentions[0]

        if role in roles:
            if value == None:
                await bot.say("Please give a number of messages!")
            else:
                def checkFx(message):
                    if message.author.id == person:
                        return True
                    else:
                        return False

                # personId = person.id
                channel = ctx.message.channel
                deleted = await bot.purge_from(channel, limit=int(value), check=checkFx)
                await bot.send_message(channel, 'Deleted {} message(s)'.format(len(deleted)))

        else:
            await bot.say("Nice try, only moderators can do that!")

    @commands.command(pass_context=True)
    async def delete(self, ctx):
        """Only for Moderators!"""
        mentions = ctx.message.mentions
        person = mentions[0]
        personId = person.id
        roles = ctx.message.author.roles
        role = discord.utils.get(ctx.message.server.roles, name='[BB19218BMOD]')
        if role in roles:
            # points
            with open('userdata.json') as f:
                data = json.load(f)
            if personId in data:
                del data[personId]
                with open('userdata.json', 'w') as f:
                    json.dump(data, f)
                await bot.say("Deleted points!")
            else:
                await bot.say("Sorry, that user is not in the database!")

            # profiles
            with open('profiles.json') as f:
                profiles = json.load(f)
            if personId in profiles:
                del profiles[personId]
                with open('profiles.json', 'w') as f:
                    json.dump(profiles, f)
                await bot.say("Deleted profile!")

            # class
            with open('groups.json') as f:
                groups = json.load(f)
            if personId in groups:
                del groups[personId]
                with open('groups.json', 'w') as f:
                    json.dump(groups, f)
                await bot.say("Deleted Class!")

            # infamy
            with open('infamy.json') as f:
                infamies = json.load(f)
            if personId in infamies:
                del infamies[personId]
                with open('infamy.json', 'w') as f:
                    json.dump(infamies, f)
                await bot.say("Deleted infamy!")

            # badge
            with open('badges.json') as f:
                badge = json.load(f)
            if personId in badge:
                del badge[personId]
                with open('badges.json', 'w') as f:
                    json.dump(badge, f)
                await bot.say("Deleted badge!")

        else:
            await bot.say("You must be a Moderator in order to use this command.  :robot:")

    @commands.command(pass_context=True)
    async def setmessageofday(self, ctx, text: str, timeout: int):
        """For Moderators only. !setmessageofday <text> <timeout in seconds>"""
        if discord.utils.get(ctx.message.server.roles, name='[BB19218BMOD]') in ctx.message.author.roles:
            with open('messageofday.json', 'w') as f:
                json.dump({"text": text, "timeout": timeout, "channel": ctx.message.channel.id}, f)

            self.setmessageofdayEventMod()
        else:
            await bot.say("You must be a Moderator in order to use this command.  :robot:")

    def setmessageofdayEventMod(self):
        with open('messageofday.json') as f:
            messageofday = json.load(f)
            if "timeout" in messageofday and "channel" in messageofday and "text" in messageofday:
                channel = self.bot.get_channel(messageofday["channel"])
                if self.messageofdaymod is None:
                    self.messageofdaymod = EventMod(channel, messageofday["timeout"], messageofday["text"])
                else:
                    self.messageofdaymod.cancel()
                    self.messageofdaymod.channel = channel
                    self.messageofdaymod.timeout = messageofday["timeout"]
                    self.messageofdaymod.text = messageofday["text"]

                self.messageofdaymod.start()

    @commands.command(pass_context=True)
    async def startmod(self, ctx, name: str, description: str, timeout: int):
        """For Moderators only. !startmod <name> <description> <timeout in seconds>"""
        if discord.utils.get(ctx.message.server.roles, name='[BB19218BMOD]') in ctx.message.author.roles:
            self.removemod(name)
            self.eventmod[name] = EventMod(ctx.message.channel, timeout, description, True)
            self.eventmod[name].start()
        else:
            await self.bot.say("Nice try, only moderators can do that!")\

    @commands.command(pass_context=True)
    async def listmod(self, ctx):
        """For Moderators only. !listmod"""
        if discord.utils.get(ctx.message.server.roles, name='[BB19218BMOD]') in ctx.message.author.roles:
            if len(self.eventmod) > 0:
                await self.bot.say("- " + ("\n- ".join(self.eventmod.keys())))
            else:
                await self.bot.say("There is no event.")
        else:
            await self.bot.say("Nice try, only moderators can do that!")

    @commands.command(pass_context=True)
    async def stopmod(self, ctx, name: str):
        """For Moderators only. !stopmod <name>"""
        if discord.utils.get(ctx.message.server.roles, name='[BB19218BMOD]') in ctx.message.author.roles:
            self.removemod(name)
        else:
            await self.bot.say("Nice try, only moderators can do that!")

    def removemod(self, name):
        if name in self.eventmod:
            self.eventmod[name].cancel()
            del self.eventmod[name]

    @commands.command(pass_context=True)
    async def deletestream(self, ctx, arg=None):
        """Deletes the stream of a given person. !deletestream @username"""
        roles = ctx.message.author.roles
        role = discord.utils.get(ctx.message.server.roles, name='[BB19218BMOD]')
        if role in roles:
            if arg == None:
                await bot.say("Please tag someone to delete their livestream!")
            else:
                with open('streams.json') as f:
                    streams = json.load(f)
                personId = ctx.message.mentions[0].id
                del streams[personId]
                with open('streams.json', 'w') as f:
                    json.dump(streams, f)
                await bot.say("Deleted stream!")
        else:
            await bot.say("Nice try, only moderators can do that!")

    @commands.command(pass_context=True)
    async def vote(self, ctx, question: str, *options: str):
        """For Moderators only. !vote <question> <options...>"""
        if discord.utils.get(ctx.message.server.roles, name='[BB19218BMOD]') in ctx.message.author.roles:
            if 1 < len(options) <= 10:
                if len(options) == 2 and options[0].lower() == 'yes' and options[1].lower() == 'no':
                    reactions = ['✅', '❌']
                else:
                    reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

                description = ""
                for x, option in enumerate(options):
                    description += reactions[x] + " " + option + "\n"

                embed = discord.Embed(colour=discord.Colour(0xFAA61A), title=question, description=description)
                message = await self.bot.say(embed=embed)
                self.votes.append(message.id)

                for reaction in reactions[:len(options)]:
                    await self.bot.add_reaction(message, reaction)

                embed.set_footer(text="Vote ID: " + str(message.id))
                await self.bot.edit_message(message, embed=embed)
            else:
                await self.bot.say("It must have between 2 to 10 options.")
        else:
            await self.bot.say("Nice try, only moderators can do that!")

    @commands.command(pass_context=True)
    async def listvote(self, ctx):
        """For Moderators only. !listvote"""
        if discord.utils.get(ctx.message.server.roles, name='[BB19218BMOD]') in ctx.message.author.roles:
            description = ""
            for message_id in self.votes:
                vote_message = await self.bot.get_message(ctx.message.channel, message_id)
                if vote_message.embeds:
                    description += "- " + str(message_id) + " = " + vote_message.embeds[0]['title'] + "\n"

            if description is "":
                description = "There is no vote in progress!"

            await self.bot.say(description)
        else:
            await self.bot.say("Nice try, only moderators can do that!")

    @commands.command(pass_context=True)
    async def endvote(self, ctx, message_id=None):
        """For Moderators only. !endvote [id]"""
        if discord.utils.get(ctx.message.server.roles, name='[BB19218BMOD]') in ctx.message.author.roles:
            if len(self.votes) > 0:
                if message_id is None:
                    message_id = self.votes[0]

                vote_message = await self.bot.get_message(ctx.message.channel, message_id)
                if vote_message.embeds and vote_message.id in self.votes:
                    self.votes.remove(vote_message.id)

                    options_to_parse = [x.strip() for x in vote_message.embeds[0]['description'].split('\n')]
                    options = {x[:2]: x[3:] for x in options_to_parse} if options_to_parse[0][0] == "1" else {x[:1]: x[2:] for x in options_to_parse}

                    vote_text_result = "Results of the vote : " + vote_message.embeds[0]['title'] + "\n\n"
                    for reaction in vote_message.reactions:
                        if reaction.emoji in options.keys():
                            vote_text_result += options[reaction.emoji] + " : " + str(len(await self.bot.get_reaction_users(reaction)) - 1) + "\n"

                    await self.bot.say(vote_text_result)
            else:
                await self.bot.say("There is no vote!")
        else:
            await self.bot.say("Nice try, only moderators can do that!")


bot.add_cog(Moderator(bot))
bot.add_cog(Member(bot))
bot.loop.create_task(backgroundStream(asyncio.get_event_loop()))

bot.run(TOKEN)
