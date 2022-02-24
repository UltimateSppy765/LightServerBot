import os
from quart import Quart,render_template,redirect,request
from threading import Thread

app=Quart('')

@app.route('/')
async def main():
    return await render_template('index.html',text="The bot is alive!")

@app.route('/join')
async def joinserver():
    return await redirect('https://discord.com/api/oauth2/authorize?client_id=943942461892489296&redirect_uri=https%3A%2F%2Flightserverbot.ultimatesppy765.repl.co%2Flightserver&response_type=code&scope=guilds.join%20identify')

@app.route('/lightserver')
async def lightserverjoin():
    if await request.args.get('error')=="access_denied":
        return await redirect(os.environ['access_denied_auth'])
    print(err)
    codee=await request.args.get('code')
    print(codee)
    return 

def run():
    app.run(host='0.0.0.0',port=8080)

def keep_alive():
    server=Thread(target=run)
    server.start()
