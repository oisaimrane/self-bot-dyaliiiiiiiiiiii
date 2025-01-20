import os
import discord
from discord.ext import commands
from youtube_dl import YoutubeDL

# Replace with your Discord token (ensure it’s set as an environment variable)
token = os.getenv("DISCORD_TOKEN")
if not token:
    raise ValueError("DISCORD_TOKEN environment variable is not set")

# Set your admin account's Discord ID
admin_id = 793877159966015548  # Replace with your admin ID

# Define bot intents and prefix
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# Auto-react feature
@client.event
async def on_message(message):
    if not message.guild:
        return  # Ignore DMs

    if client.user.mentioned_in(message) and message.author.id != client.user.id:
        try:
            await message.add_reaction("👍")  # Change emoji if needed
        except discord.Forbidden:
            print("Missing permission to add reaction.")
    
    await client.process_commands(message)

# Music feature
@client.event
async def on_ready():
    print(f'Logged in as {client.user}')

@client.event
async def on_voice_state_update(member, before, after):
    # You can add more functionality here, like auto-joining or leaving a voice channel

@client.event
async def on_message(message):
    # Handle your music commands here
    if message.content.startswith('!join'):
        if message.author.voice:
            channel = message.author.voice.channel
            await channel.connect()
        else:
            await message.channel.send("You must be in a voice channel to use this command!")
    elif message.content.startswith('!play'):
        # You can implement the play command logic here
        pass

# Run the selfbot
client.run(token)
