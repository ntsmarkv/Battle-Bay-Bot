    @commands.command(pass_context=True)
    @commands.cooldown(1, 86400, commands.BucketType.user)
    async def getreward(self, ctx, useless, value: int):
        """Collect your Reward BBPs!' """
        roles = ctx.message.author.roles
        role = discord.utils.get(ctx.message.server.roles, name='@everyone')
        if role in roles:
            mentions = ctx.message.mentions
            person = mentions[0]
            personId = person.id
            with open('userdata.json') as f:
                data = json.load(f)
            if personId in data:
                olddata = data[personId]
                newdata = olddata + 500
                newformatted = {personId: newdata}
                data.update(newformatted)
                with open('userdata.json', 'w') as f:
                    json.dump(data, f)
                await bot.say("Collected; **500** reward BBPs!")
            else:
                await bot.say("Sorry, that user is not in the database!")
        else:
            await bot.say("**You**< already collected your reward BBPss, or **You** are not yet authorized.")