import os
import disnake as discord

def perviews():
    return [ToggleAdmin()]

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
            await itr.author.remove_roles(943965618976210966)
            return await itr.edit_original_message(content='Removed <@&943965618976210966>.')
        else:
            await itr.author.add_roles(943965618976210966)
            return await itr.edit_original_message(content='Added <@&943965618976210966>.')
