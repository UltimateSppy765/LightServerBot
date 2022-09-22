import os,aiohttp,json
from flask import Flask,render_template,redirect,request
from threading import Thread

app=Flask('')

async def handlejoin(code:str):
    async with aiohttp.ClientSession() as session:
        async with session.post('https://discord.com/api/v10/oauth2/token',headers={'Content-Type':'application/x-www-form-urlencoded'},data={'grant_type':'authorization_code','code':code,'redirect_uri':'https://lightserverbot.ultimatesppy765.repl.co/lightserver'},auth=aiohttp.BasicAuth(os.environ['CLIENT_ID'],os.environ['CLIENT_SECRET'])) as resp:
            somejson1=await resp.json()
            atoken=somejson1['access_token']

        async with session.get('https://discord.com/api/v10/users/@me',headers={'Authorization':f'Bearer {atoken}'}) as resp:
            somejson2=await resp.json()
            user_id=somejson2['id']

        if int(user_id) not in json.loads(os.environ['whitelist'])+json.loads(os.environ['server_admins']):
            async with session.post('https://discord.com/api/v10/oauth2/token/revoke',headers={'Content-Type':'application/x-www-form-urlencoded'},data={'client_id':os.environ['CLIENT_ID'],'client_secret':os.environ['CLIENT_SECRET'],'token':atoken}) as resp:
                pass
            return redirect('https://ultimatesppy765.github.io/LightServerBot/denied')
        
        dummylist=['950856588518899712'] if int(user_id) in json.loads(os.environ['server_admins']) else []

        async with session.put(f'https://discord.com/api/v10/guilds/943965618976210965/members/{user_id}',headers={'Authorization':f'Bot {os.environ["BOT_TOKEN"]}'},json={'access_token':atoken,'roles':json.loads(os.environ['memroles'].replace("'",'"'))[user_id]+['944108632088387594']+dummylist}) as resp:
            ineedthisnumber=resp.status

        async with session.post('https://discord.com/api/v10/oauth2/token/revoke',headers={'Content-Type':'application/x-www-form-urlencoded'},data={'client_id':os.environ['CLIENT_ID'],'client_secret':os.environ['CLIENT_SECRET'],'token':atoken}) as resp:
            pass

        if ineedthisnumber==201 or ineedthisnumber==204:
            return redirect('https://discord.com/channels/943965618976210965/943967423923617883')

@app.route('/')
async def main():
    return render_template('index.html',text="The bot is alive!")

@app.route('/dummy')
async def dummy():
    return render_template('instaclose.html')

@app.route('/join')
async def joinserver():
    return redirect('https://discord.com/api/oauth2/authorize?client_id=943942461892489296&redirect_uri=https%3A%2F%2Flightserverbot.ultimatesppy765.repl.co%2Flightserver&response_type=code&scope=guilds.join%20identify')

@app.route('/lightserver')
async def lightserverjoin():
    if request.args.get('error')=="access_denied":
        return redirect(os.environ['access_denied_auth'])
    return await handlejoin(request.args.get('code'))

@app.errorhandler(404)
async def page_not_found(err):
    return redirect('https://http.cat/404')

@app.errorhandler(500)
async def internal_server_error(err):
    return redirect('https://http.cat/500')

def run():
    app.run(host='0.0.0.0',port=8080)

def keep_alive():
    server=Thread(target=run)
    server.start()
