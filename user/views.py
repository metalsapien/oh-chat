''' This module contains all the routes and functions responsible for 
    logical functioning and response of the app from the server.
    It uses SocketIO to connect to the client through events. '''

from ohchat import app, socketio
from flask import render_template, request, url_for, redirect, flash
from flask_socketio import emit, disconnect
from user.forms import VerifyForm
from datetime import datetime
import time
import json

# Initializing the python dictionaries and list to store the user
# dynamically and temporarily.

# names_as_value takes key as session id and
# value as user name.
names_as_value = {}
# sid_as_value takes key as username and
# value as session id.
sid_as_value = {}
# total_users stores the list of all the users currently online.
total_users = []

@app.route('/', methods=['GET', 'POST'])
def verify():
    ''' This function gets called when the user is on the login page.
    It posts the username passed to it onto the server and redirects user
    to the main chat page '''

    form = VerifyForm()
    # Conncets to the server if the username is unique and form is valid.
    if request.method == 'POST' and form.validate_on_submit() and form.username.data not in total_users:  # NOQA
        username = form.username.data
        total_users.append(username)
        flash('Welcome ' + '<strong>' + username + '</strong>')
        return redirect(url_for('ohchat', username=username))
    # Flashse error if username is already active in the server
    elif request.method == 'POST' and form.username.data in total_users and form.username.data != '':  # NOQA
        flash("Username already active")
    # Flashes error if the username field is empty
    elif request.method == 'POST' and form.username.data == '':
        flash("Username is required")

    return render_template('verify.html', form=form)


@app.route('/ohchat/<username>', methods=['GET', 'POST'])
def ohchat(username):
    ''' This function leads to the main server/chatting page after login. '''

    # Stroing the current date and time.
    ctime = time.strftime('%I:%M %p')
    date = datetime.today().strftime("%d %B, %Y")
    # Redirects to the login page if username is not found the total_users list.
    if username not in total_users:
        return redirect(url_for('verify'))

    return render_template('ohchat.html',
                            username=username,
                            time=ctime, 
                            total_users=total_users, 
                            date=date)


@socketio.on('username')
def username(name):
    ''' This function/event gets called whenever a user connects to the
    server and displays all the neccessary names on the page. '''

    names_as_value[request.sid] = name
    sid_as_value[name] = request.sid
    anonymous_user = {}
    # Getting the current time.
    ctime = time.strftime('%I:%M %p')
    # Storing the anonymous users that are online into a local dictionary
    # so as to display it on the total users online section.
    for i in range(len(total_users)):
        if total_users[i] != name:
            anonymous_user[i] = total_users[i]

    # Notifying all the users if the current user logs in.
    emit('user_online', 
        { 'name' : name, 'time' : ctime }, 
        broadcast=True, 
        json=True)
    # Sending all the anonymous username to be displayed
    emit('anony_user', anonymous_user)
    # Event to display the current users session id after login.
    emit('id', request.sid)


@socketio.on('message')
def from_client(message):
    ''' This function/event gets called if the client sends a message to
    the server. The server returns the sent message back to the room
    as directed by the sender '''

    chat_time = time.strftime('%I:%M %p')
    # Server responds back to the client with broadcasting feature.
    emit('from server', 
        { 'name':names_as_value[request.sid], 
        'time':chat_time, 'msg':message }, 
        broadcast=True, 
        json=True)


@socketio.on('private_message')
def private_message(message):
    ''' This function/event gets called when a user sends a private message
    to another user. '''

    # Getting the session id of the recipient.
    sid = sid_as_value[message['recipient']]
    # Storing the message to be sent.
    message = message['message']
    # Getting the current time at which the message will be sent.
    chat_time = time.strftime('%I:%M %p')
    # Sending the message to the recipient only.
    emit('sent_pm', 
        { 'name':names_as_value[request.sid], 
        'time':chat_time, 
        'msg':message }, 
        room=sid, 
        json=True)
    # Sending the same message to the current user only.
    emit('sent_pm', 
        { 'name':names_as_value[request.sid], 
        'time':chat_time, 
        'msg':message }, 
        room=request.sid, 
        json=True)


@socketio.on('disconnect')
def disconnect_user():
    ''' This function gets called when the user disconnects from the server. '''

    username = names_as_value[request.sid]
    # Deleting the username from the list
    total_users.remove(username)
    # Deleting the session id from the dictioanry
    del sid_as_value[username]
    # Deleting the username from the dictionary
    del names_as_value[request.sid]


@socketio.on('disconnect_me')
def disconnect_me(msg):
    ''' This function gets called when the user click at disconnect button.
    This in return calls the main disconnect function. '''

    ctime = time.strftime('%I:%M %p')
    username = names_as_value[request.sid]
    # An event that deletes the disconnected user dynamically from the page
    # and broadcasts it to notify other users about the disconnection.
    emit('user_disconnect', { 'name' : username, 'time' : ctime }, broadcast=True, json=True)
    # This is refreshes the page after disconncetion leading back to the login page.
    emit('refresh', "Page refresh")
    # This is main function that disconnects the user from the server.
    disconnect()
