import os
from flask import Flask,render_template,redirect,request
from threading import Thread

app=Flask('')

@app.route('/')
def main():
    return render_template('index.html',text="The bot is alive!")

@app.route('/join')
def joinserver():
    return redirect('https://discord.com/api/oauth2/authorize?client_id=943942461892489296&redirect_uri=https%3A%2F%2Flightserverbot.ultimatesppy765.repl.co%2Flightserver&response_type=code&scope=guilds.join%20identify%20guilds')

@app.route('/lightserver')
def lightserverjoin():
    err=request.args.get('error')
    print(err)
    codee=request.args.get('code')
    print(codee)
    return 

def run():
    app.run(host='0.0.0.0',port=8080)

def keep_alive():
    server=Thread(target=run)
    server.start()
