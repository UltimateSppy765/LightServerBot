import os,json,asyncio
import disnake as discord

def perviews():
    return [ToggleAdmin(),AnnounceRole()]

class ToggleAdmin(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(custom_id=os.environ['toggle_admin_role'])
    async def adminroletoggle(self,button,itr):
        if itr.author.id not in json.loads(os.environ['server_admins']):
            await itr.response.defer()
            return
        await itr.response.defer(with_message=True,ephemeral=True)
        if itr.author.get_role(943965618976210966):
            await itr.author.remove_roles(itr.guild.get_role(943965618976210966),reason='Toggled Admin Role.')
            return await itr.edit_original_message(content='Removed <@&943965618976210966>.')
        else:
            await itr.author.add_roles(itr.guild.get_role(943965618976210966),reason='Toggled Admin Role.')
            return await itr.edit_original_message(content='Added <@&943965618976210966>.')

class AnnounceRole(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        
    @discord.ui.button(custom_id=os.environ['announcement_role'])
    async def announcerole(self,button,itr):
        await itr.response.defer(with_message=True,ephemeral=True)
        if itr.author.get_role(944151595023736842):
            return await itr.edit_original_message(content='You already have the permission to send messages in <#944150808864358430>.')
        else:
            await itr.author.add_roles(itr.guild.get_role(944151595023736842),reason='Requested by user for an announcement.')
            await itr.edit_original_message(content='You have been granted the permission to send messages in <#944150808864358430> for 30 seconds.')
            await asyncio.sleep(30)
            await itr.author.remove_roles(itr.guild.get_role(944151595023736842),reason='30 seconds complete.')
            return await itr.followup.send('Your 30 seconds are up, the permissions have been removed.')
