    ##	@commands.command(pass_context=True)
    ##	async def setbadge(self, ctx, arg=None):
    ##		"""Used to change your badge; !setbadge picurl.com"""
    ##		with open('badges.json') as f:
    ##			badges = json.load(f)
    ##		if arg == None:
    ##			await bot.say("Please give a valid input!")
    ##			return
    ##		else:
    ##			personId = ctx.message.author.id
    ##			newBadge = {personId: arg}
    ##			badges.update(newBadge)
    ##			with open('badges.json', 'w') as f:
    ##				json.dump(badges, f)
    ##			await bot.say("Successfully updated badge!")
