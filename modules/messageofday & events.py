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


@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    bot.get_cog("Moderator").setmessageofdayEventMod()


class Moderator():
    """Only Moderators can run these commands!"""

    def __init__(self, bot):
        self.bot = bot
        self.votes = []
        self.messageofdaymod = None
        self.eventmod = dict()

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


bot.add_cog(Moderator(bot))
bot.add_cog(Member(bot))

bot.run(TOKEN)