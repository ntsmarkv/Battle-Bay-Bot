@bot.command(pass_context=True)
async def equality(ctx, url):
    channel = ctx.message.author.voice.voice_channel
    await bot.join_voice_channel(channel)
    server = ctx.message.server
    player = voice.create_ffmpeg_player('music/voice/eg.wav')
    players[server.id] = player
    player.start()