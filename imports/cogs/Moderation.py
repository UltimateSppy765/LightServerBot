from disnake.ext import commands
import disnake as discord
from datetime import timedelta
import os,json

def admin_only():
    def predicate(itr):
        return itr.author.id in json.loads(os.environ['server_admins'])
    return commands.check(predicate)

class WipeChecks():
    def __init__(self,count:int,user_id:int=None,text:str=None):
        self.counter=1
        self.count=count
        self.user_id=user_id
        self.textchk=text
    
    def usercheck(self,m):
        if self.counter>self.count:
            return False
        if m.author.id==self.user_id:
            self.counter+=1
            return True

    def hastextcheck(self,m):
        if self.counter>self.count:
            return False
        if self.textchk in m.content.lower():
            if self.user_id:
                if self.user_id==m.author.id:
                    self.counter+=1
                    return True
                else:
                    return False
            else:
                self.counter+=1
                return True
        else:
            return False

class Wipedone(discord.ui.View):
    def __init__(self,followup):
        self.responded=False
        self.followup=followup
        super().__init__(timeout=10)

    @discord.ui.button(label="Got it!",style=discord.ButtonStyle.green)
    async def wipegotit(self,btn:discord.ui.Button,itr:discord.MessageInteraction):
        if itr.user.id!=itr.message.interaction.user.id:
            return await itr.response.send_message(':x: You cannot use a button on a command invoked by someone else.',ephemeral=True)
        self.responded=True
        await self.followup.delete_message(itr.message.id)

    async def on_timeout(self):
        if not self.responded:
            return await self.message.edit(view=None)

class Moderation(commands.Cog):
    def __init__(self,client):
        self.client=client
    @commands.bot_has_permissions(read_message_history=True,manage_messages=True)
    @admin_only()
    @commands.slash_command()
    async def wipe(self,itr):
        pass

    @wipe.error
    async def wipe_error(self,itr,error):
        if isinstance(error,commands.CheckFailure):
            return await itr.response.send_message(':x: You cannot use this command.',ephemeral=True)
        elif isinstance(error,commands.BotMissingPermissions):
            strr=''
            for i in error.missing_permissions:
                i=i.replace('_',' ')
                i=i.title()
                strr=strr+f'• {i}\n'
            return await itr.response.send_message(f':x: The bot does not have the following permissions in this channel to run this command:```\n{strr}```',ephemeral=True)
        elif isinstance(error,discord.HTTPException):
            if isinstance(error,discord.Forbidden):
                text=f':x: The bot is forbidden to perform some actions involved in this command. ```\n{error.text}\n```'
            else:
                text=f':x: The bot ran into an error while trying to execute this command. ```\n{error.text}\n```'
            if itr.response.is_done():
                return await itr.edit_original_message(text)
            else:
                return await itr.response.send_message(text,ephemeral=True)

    @wipe.sub_command()
    async def off(self,itr,count:int=20,hidden:bool=False):
        await itr.response.defer(ephemeral=hidden)
        pur=await itr.channel.purge(limit=count,before=itr,after=discord.utils.snowflake_time(itr.id)-timedelta(days=14),bulk=True,oldest_first=False)
        view=Wipedone(followup=itr.followup) if not hidden else None
        await itr.edit_original_message(content=f":broom: Successfully wiped {len(pur)} message{'s' if len(pur)>1 else ''}." if len(pur)>0 else ":negative_squared_cross_mark: No messages were wiped.",view=view)
        if not hidden:
            view.message=await itr.original_message()

    @wipe.sub_command()
    async def user(self,itr,user:discord.User,count:int=20,hidden:bool=False):
        await itr.response.defer(ephemeral=hidden)
        pur=await itr.channel.purge(check=WipeChecks(count=count,user_id=user.id).usercheck,limit=1000,before=itr,after=discord.utils.snowflake_time(itr.id)-timedelta(days=14),bulk=True,oldest_first=False)
        view=Wipedone(followup=itr.followup) if not hidden else None
        await itr.edit_original_message(content=f":broom: Successfully wiped {len(pur)} message{'s' if len(pur)>1 else ''}." if len(pur)>0 else ":negative_squared_cross_mark: No messages were wiped.",view=view)
        if not hidden:
            view.message=await itr.original_message()

    @wipe.sub_command()
    async def text(self,itr,text:str,user:discord.User=None,count:int=20,hidden:bool=False):
        await itr.response.defer(ephemeral=hidden)
        pur=await itr.channel.purge(check=WipeChecks(count=count,text=text.strip().lower(),user_id=user.id if user else None).hastextcheck,limit=1000,before=itr,after=discord.utils.snowflake_time(itr.id)-timedelta(days=14),bulk=True,oldest_first=False)
        view=Wipedone(followup=itr.followup) if not hidden else None
        await itr.edit_original_message(content=f":broom: Successfully wiped {len(pur)} message{'s' if len(pur)>1 else ''}." if len(pur)>0 else ":negative_squared_cross_mark: No messages were wiped.",view=view)
        if not hidden:
            view.message=await itr.original_message()
            
def setup(client):
    client.add_cog(Moderation(client))
