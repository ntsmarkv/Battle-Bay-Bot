@bot.event
async def on_member_join(member):
    with open('users.json', 'r') as f:
        users = json.load(f)

    await update_data(users, member)

    with open('users.json', 'w') as f:
        json.dump(users, f)
    await bot.send_message(discord.utils.get(member.server.channels, type=discord.ChannelType.text), embed=discord.Embed(colour=discord.Colour(0xFAA61A), description="If you need help use; !help."))


@bot.event
async def on_message(message):
 with open('users.json', 'r') as f:
           users = json.load(f)

     await update_data(users, message.author)
     await add_experience(users, message.author, 5)
     await level_up(users, message.author, message.channel)
     await add_bbp(users, message.author, 1)

        with open('users.json', 'w') as f:
          json.dump(users, f)

async def update_data(users, user):
    if not user.id in users:
        users[user.id] = {}
        users[user.id]['experience'] = 0
        users[user.id]['level'] = 0
        users[user.id]['points'] = 1000


async def add_experience(users, user, exp):
    users[user.id]['experience'] += exp


async def add_bbp(users, user, bbps):
    users[user.id]['points'] += bbps


async def level_up(users, user, channel):
    experience = users[user.id]['experience']
    lvl_start = users[user.id]['level']
    lvl_end = int(experience ** (1/4))

    if lvl_start < lvl_end:
#        await bot.send_message(user, '{}, You just leveled :up:!! You are now level {}'.format(user.mention, lvl_end))
        users[user.id]['level'] = lvl_end