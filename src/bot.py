import os
import discord
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
  guild = discord.utils.find(lambda g: g.id == GUILD_ID, client.guilds)
  print(
    f'{client.user} is connected to the following guild:\n'
    f'{guild.name}(id: {guild.id})'
  )

@client.event
async def on_member_join(member):
  await member.create_dm()
  await member.dm_channel.send(
    f'Hi {member.name}, welcome to my Discord server!'
  )

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  
  if not message.content.startswith('!subot'):
    return

  response = 'I am a bot that can do many things. Many new features are coming!'
  await message.channel.send(response)

client.run(TOKEN)