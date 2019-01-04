    @commands.command(pass_context=True)
    async def activity(self, ctx):
        """Shows monthly activity BBPs for members"""
        with open('activity.json') as f:
            data = json.load(f)
        unsorted = []
        for xel in data:
            newString = "00000000" + str(data[xel])
            shortened = newString[-8:] + " " + xel
            unsorted.append(shortened)
        finished = sorted(unsorted)
        flipped = list(reversed(finished))
        counter = 1
        finalMessage = "**Most Active Members:** \n"
        for x in flipped:
            if counter <= 20:
                num = int(x.split()[0])
                userId = x.split()[1]
                # await bot.say(str(counter) + ". <@" + str(userId) + "> has " + str(num) + " points")
                finalMessage = finalMessage + str(counter) + ". <@" + str(userId) + "> has **" + str(num) + "** activity points \n"
                counter += 1
        embed = discord.Embed(description=finalMessage, color=0xFAA61A)
        await bot.send_message(ctx.message.channel, embed=embed)
