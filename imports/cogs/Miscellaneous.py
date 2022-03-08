from disnake.ext import commands
import disnake as discord

class Miscellaneous(commands.Cog):
    """Miscellaneous commands."""
    def __init__(self,client):
        self.client=client

    @commands.slash_command()
    async def ping(self,itr):
        await itr.response.send_message(f'Bot latency is `{round(self.client.latency*1000)}ms`.',ephemeral=True)

    @commands.cooldown(per=15,rate=1,type=commands.BucketType.member)
    @commands.slash_command(name='start-yt')
    async def ytinv(self,itr,channel:discord.VoiceChannel):
        if channel==itr.guild.afk_channel:
            return await itr.response.send_message(':x: You cannot start this activity in the Guild\'s AFK channel.',ephemeral=True)
        inv=await channel.create_invite(max_age=30,max_uses=1,target_type=discord.InviteTarget.embedded_application,target_application=discord.PartyType.watch_together,reason=f'Watch Together invite requested by {str(itr.author)}')
        await itr.response.send_message(f':postbox: A one time invite has been generated to start Watch Together in {channel.mention}. This is valid for 30 seconds. Do not share this outside the server.\n{inv.url}',ephemeral=True)

    @ytinv.error
    async def ytinv_error(self,itr,err):
        if isinstance(err,commands.CommandOnCooldown):
            return await itr.response.send_message(f':hourglass: You are on cooldown. Please try again in {round(err.retry_after)} seconds.')

def setup(client):
    client.add_cog(Miscellaneous(client))
