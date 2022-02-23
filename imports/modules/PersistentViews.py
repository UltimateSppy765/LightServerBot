import os
import disnake as discord

def perviews():
    return [ToggleAdmin()]

class ToggleAdmin(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(custom_id=os.environ['toggle_admin_role'])
    async def adminroletoggle(self,button,itr):
        await itr.response.send_message('Hello World!',ephemeral=True)
