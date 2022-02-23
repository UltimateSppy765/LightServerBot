import disnake as discord
from disnake.ext import commands

client=commands.Bot(command_prefix='!',intents=discord.Intents.all(),sync_commands=False,description='Let the light shine!',owner_id=770542184310243342,activity=discord.Activity(type=discord.ActivityType.watching,name='hopes rise'),allowed_mentions=discord.AllowedMentions(roles=False))

@client.event
async def on_ready():
    print('Bot is ready.')
    print(f'Logged in as {client.user.name} - {client.user.id}')

@client.command()
async def ping(ctx):
    """Shows the latency of the bot."""
    await ctx.reply(f'Ping is `{round(client.latency*1000)}ms`',mention_author=False)

client.run(os.environ['BOT_TOKEN'])
