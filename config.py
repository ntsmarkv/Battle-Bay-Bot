import asyncio
import discord
from discord.ext import commands
if not discord.opus.is_loaded():
    # the 'opus' library here is opus.dll on windows
    # or libopus.so on linux in the current directory
    # you should replace this with the location the
    # opus library is located in and with the proper filename.
    # note that on windows this DLL is automatically provided for you
    discord.opus.load_opus('opus')


class config:
    """Utility Modules"""
    @commands.command(pass_context=True)
    async def ping(ctx):
        """Pong"""
        before = time.monotonic()
        await(await bot.ws.ping())
        after = time.monotonic()
        _ping = (after - before) * 1000
        await bot.say("**Trip FROM me to you-->** :ping_pong: **{0:.0f}ms**".format(_ping))
        await bot.say(ctx, "**Trip FROM Me to Rovio-->** :ping_pong: **{0:.0f}ms**".format(_ping))


def setup(bot):
    bot.add_cog(config(bot))
    print('Utilities is loaded')
    print('Beta Testers now has Access')