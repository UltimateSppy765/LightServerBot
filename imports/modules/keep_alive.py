from flask import Flask,render_template,redirect
from threading import Thread

app=Flask('')

@app.route('/')
def main():
    return redirect('https://www.youtube.com/watch?v=dQw4w9WgXcQ')

@app.route('/alive')
def alive():
    return render_template('index.html')

@app.route('/lightserver')
def lightserverjoin():
    return 

def run():
    app.run(host='0.0.0.0',port=8080)

def keep_alive():
    server=Thread(target=run)
    server.start()