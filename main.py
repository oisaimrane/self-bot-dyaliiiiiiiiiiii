import os
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

# Ensure the DISCORD_TOKEN is set as an environment variable
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

# Set your admin account's Discord ID
admin_id = 793877159966015548  # Replace with your admin ID

# Define bot intents and selfbot settings
intents = discord.Intents.default()
client = commands.Bot(command_prefix="!", self_bot=True, intents=intents)

# Auto-react feature for messages where the selfbot is mentioned
@client.event
async def on_message(message):
    if not message.guild:
        return  # Ignore DMs

    if client.user.mentioned_in(message) and message.author.id != client.user.id:
        try:
            await message.add_reaction("👍")  # Change emoji if needed
        except discord.Forbidden:
            print("Missing permission to add reaction.")
    
    await client.process_commands(message)  # Process other commands

# Music feature: Join voice channel
@client.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
    else:
        await ctx.send("You must be in a voice channel to use this command!")

# Music feature: Play audio from URL
@client.command()
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

# Music feature: Leave voice channel
@client.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
    else:
        await ctx.send("I'm not in a voice channel!")

# Selfbot Ready Event: Print when logged in
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

# Optional: Handle voice state changes (example: auto join/leave)
@client.event
async def on_voice_state_update(member, before, after):
    # Implement any automatic behavior when voice states change, e.g., auto join/leave
    pass

# Run the selfbot with user token
client.run(token)
