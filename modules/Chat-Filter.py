

chat_filter = ["SHIT", "FUCK", "ASS", "pineapple"]
bypass_list = []

@bot.event
async def on_message(message):
    contents = message.content.split(" ") #contents is a list type
    for word in contents:
        if word.upper() in chat_filter:
            if not message.author.id in bypass_list:
                try:
                    await bot.delete_message(message)
                    await bot.send_message(message.channel, "**Hey! You're not allowed to say that word!**")
                except discord.errors.Notfound:
                    return