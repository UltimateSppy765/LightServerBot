from disnake.ext import commands

class Miscellaneous(commands.Cog):
    """Miscellaneous commands."""
    def __init__(self,client):
        self.client=client

    @commands.slash_command()
    async def ping(self,itr):
        await itr.response.send_message(f'Bot latency is `{round(self.client.latency*1000)}ms`.',ephemeral=True)