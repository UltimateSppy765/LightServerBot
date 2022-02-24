import os,json,traceback
import disnake as discord
from imports.modules import PersistentViews,keep_alive
from disnake.ext import commands

class PersistentView(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix='!',intents=discord.Intents.all(),sync_commands=False,description='Let the light shine!',owner_id=770542184310243342,activity=discord.Activity(type=discord.ActivityType.watching,name='hopes rise!'),allowed_mentions=discord.AllowedMentions(roles=False))
        self.persistent_views_added=False

    async def on_ready(self):
        if not self.persistent_views_added:
            for i in PersistentViews.perviews():
                self.add_view(i)
            self.persistent_views_added=True
        print(f'Bot is ready.\nLogged in as {client.user.name} - {client.user.id}')

client=PersistentView()

with open('coglist.json','r') as file:
    data=json.load(file)

@client.command()
async def ping(ctx):
    """Shows the latency of the bot."""
    await ctx.reply(f'Ping is `{round(client.latency*1000)}ms`',mention_author=False)

successnum=0
for i in data:
    if i['load_on_start']==True:
        try:
            client.load_extension(i['path'])
            successnum+=1
        except:
            print(f"Failed to load extension: {i['name']}")
            print(traceback.format_exc())
if successnum>0:
    print(f'Successfully loaded {successnum} cog{"s" if successnum>1 else ""}.')

keep_alive.keep_alive()
#client.run(os.environ['BOT_TOKEN'])