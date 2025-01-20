import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

# Replace with your Discord token
token = ""

# Set your admin account's Discord ID
admin_id = 793877159966015548  # Replace with your admin ID

# Define bot intents and prefix
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", self_bot=True, intents=intents)

# Auto-react feature
@bot.event
async def on_message(message):
    if not message.guild:
        return  # Ignore DMs

    if bot.user.mentioned_in(message) and message.author.id != bot.user.id:
        try:
            await message.add_reaction("👍")  # Change emoji if needed
        except discord.Forbidden:
            print("Missing permission to add reaction.")
    await bot.process_commands(message)

# Music feature
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You must be in a voice channel to use this command!")

@bot.command()
async def play(ctx, url):
    if ctx.voice_client is None:
        await ctx.send("I need to be in a voice channel first! Use `!join`.")
        return

    YDL_OPTIONS = {"format": "bestaudio", "noplaylist": True}
    FFMPEG_OPTIONS = {"options": "-vn"}

    vc = ctx.voice_client

    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info["url"]
        vc.play(discord.FFmpegPCMAudio(executable="ffmpeg", source=url2, **FFMPEG_OPTIONS))
        await ctx.send(f"Now playing: {info['title']}")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel!")

# Run the bot
bot.run(token)