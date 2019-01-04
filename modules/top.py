    @commands.command(pass_context=True)
    async def top(self, ctx):
        """Shows top 10 members"""
        with open('userdata.json') as f:
            data = json.load(f)
        unsorted = []
        for xel in data:
            newString = "00000000" + str(data[xel])
            shortened = newString[-8:] + " " + xel
            unsorted.append(shortened)
        finished = sorted(unsorted)
        flipped = list(reversed(finished))
        counter = 1
        finalMessage = "**Top 10 Members:** \n"
        # await bot.say("Top 10 members:")
        for x in flipped:
            if counter <= 10:
                num = int(x.split()[0])
                userId = x.split()[1]
                # await bot.say(str(counter) + ". <@" + str(userId) + "> has " + str(num) + " points")
                finalMessage = finalMessage + str(counter) + ". <@" + str(userId) + "> has **" + str(num) + "** bbps \n"
                counter += 1
        await bot.send_message(ctx.message.channel, embed=discord.Embed(description=finalMessage, color=0xFAA61A))
