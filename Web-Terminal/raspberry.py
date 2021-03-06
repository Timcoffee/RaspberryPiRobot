#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
    RPi_Robot
    ~~~~~~

    A robot website application written with
    Flask.

    :copyright: (c) TEOTW by Jailman.
    :license: Apache 2.0.
"""

'''##########Import modules##########'''
# from sqlite3 import dbapi2 as sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
     render_template, flash
from time import sleep
from datetime import timedelta
#import dirvers
# from Modules import driver
# from Modules import servo

'''##########App & config setup##########'''
# create our little application :)
app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY='SeriouslydevelopedbyJailman',
    USERNAME='admin',
    PASSWORD='111'
))
app.config.from_envvar('FLASKR_SETTINGS', silent=True)
app.permanent_session_lifetime = timedelta(hours=5)



'''##########Login & error & command pages##########'''
#error handler
@app.errorhandler(403)
def forbidden(error):
    title = 'Error 403'
    return render_template('403.html', title=title), 403

@app.errorhandler(404)
def page_not_found(error):
    title = 'Error 404'
    return render_template('404.html', title=title), 404

@app.errorhandler(500)
def server_error(error):
    title = 'Error 503'
    return render_template('503.html', title=title), 500


#command page
@app.route('/command')
def command():
    title = 'Command'
    if not session.get('logged_in'):
        abort(403)
    return render_template('command.html', title=title)


#login page
@app.route('/', methods=['GET', 'POST'])
def login():
    title = 'Login'          
    if session.get('logged_in'):
        return redirect(url_for('index'))
    # flash('You wanna damn log in, son?')
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            abort(403)
        elif request.form['password'] != app.config['PASSWORD']:
            abort(403)
        else:
            session['logged_in'] = True
            # flash('You were logged in, fucker!')
            return redirect(url_for('index'))
    return render_template('login.html', title=title)


#logout page
@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('Warning: You were logged out!')
    return redirect(url_for('login'))



'''##########Pi Pages##########'''
#raspberrypi pages
@app.route('/index')
def index():
    # session.permanent = True
    if not session.get('logged_in'):
        abort(403)
    return render_template('index.html')

@app.route('/Patrol_Monitor')
def Patrol_Monitor():
    if not session.get('logged_in'):
        abort(403)
    return render_template('Patrol_Monitor.html')

@app.route('/Sensor_Graph')
def Sensor_Graph():
    if not session.get('logged_in'):
        abort(403)
    return render_template('Sensor_Graph.html')

@app.route('/Home_Automation')
def Home_Automation():
    if not session.get('logged_in'):
        abort(403)
    return render_template('Home_Automation.html')

@app.route('/Amaze_Me')
def Amaze_Me():
    if not session.get('logged_in'):
        abort(403)
    return render_template('Amaze_Me.html')

'''##########Charts Demo##########'''
@app.route('/get_temperature')
def get_temperature():
    return '[30.1, 30.1, 30.1, 30.1, 30.1, 30.1, 30.1, 30.1, 30.1, 30.1, 30.1, 30.1]'

@app.route('/get_humidity')
def get_humidity():
    return '[32.3, 32.5, 32.1, 32.6, 30.8, 30.9, 31.1, 31.5, 32.1, 31.9, 31.7, 31.5]'

@app.route('/get_time')
def get_time():
    return "['2:00', '2:05', '2:10', '2:15', '2:20', '2:25', '2:30', '2:35', '2:40', '2:45', '2:50', '2:55']"

'''##########Pi Power Control##########'''
# from Modules.gpiostat import gpio_status

@app.route('/power')
def query():
    # querystatus
    return "on"
    # GPIO_PIN = 12
    # return gpio_status(GPIO_PIN)

@app.route('/power/<control>')
def switch(control):
    if control == "on":
        # switchon
        return "on"
    if control == "off":
        # switchoff
        return "off"


'''##########Robot drivers##########'''

@app.route('/driver/<control>')
def robot_driver(control):
    from Modules import driver as d
    d.init_driver()
    if control == "forward":
        d.forward()
    if control == "backward":
        d.backward()
    if control == "stop":
        d.stop()
    if control == "left":
        d.left()
    if control == "right":
        d.right()

'''##########Servo drivers##########'''
# @app.route('/servo/<float:post_value>')
# def servo_ctrl(post_value):
#     servo.somefunc(post_value)








if __name__ == '__main__':
    app.run(
        debug = False,
        host='0.0.0.0',
        port=80
        )
