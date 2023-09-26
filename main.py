import os
import discord
from discord.ext import tasks
import asyncio
import datetime as dt
from dotenv import load_dotenv
from helper import SecondToDesiredHour

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))
target_hour = int(os.getenv("HOUR_TO_SEND_MESSAGE"))
client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
  guild = discord.utils.find(lambda g: g.id == GUILD_ID, client.guilds)
  print(
    f'{client.user} is connected to the following guild:\n'
    f'{guild.name}(id: {guild.id})'
  )
  standup_task.start()

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

@tasks.loop(hours=24)
async def standup_task():
	now = dt.datetime.now()
	if now.hour == target_hour:
		TEST_CHANNEL_ID = int(os.getenv("DISCORD_TEST_CHANNEL_ID"))
		message_channel = client.get_channel(TEST_CHANNEL_ID)
		await message_channel.send(
"""
1. What have you done ?
2. What are you planning to work on today ?
3. Any blockers ?
"""
		)
	else:
		hours_until_target = (target_hour - now.hour) % 24
		print(hours_until_target * 60 * 60)
		await asyncio.sleep(hours_until_target * 60 * 60)
		standup_task.restart()

@standup_task.before_loop
async def before_reminder():
	now = dt.datetime.now()
	if(now.hour == target_hour):
		return
	total_wait = SecondToDesiredHour.get_second_until_desired_hour(target_hour) + 1 # add 1 second margin of error to make sure the time is passed
	print(f"Waiting for {total_wait} seconds before starting the reminder loop.")
	await asyncio.sleep(total_wait)

client.run(TOKEN)