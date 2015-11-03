import discord
import logging
import sys
import threading

# Set up the logging module to output diagnostic to the console.
logging.basicConfig()

client = discord.Client()
client.login(str(sys.argv[1]), str(sys.argv[2]))
currchannel = 0

if not client.is_logged_in:
    print('Logging in to Discord failed')
    exit(1)

@client.event
def on_ready():
    print('Connected as ' + client.user.name)

@client.event
def on_message(message):
    if message.author.id != client.user.id:
        print('[' + message.channel.name + '] '
        + message.author.name + ': ' + message.content)
    if message.content.startswith('/ch'):
        print message.channel.id
        global currchannel
        currchannel = message.channel

def read_in():
    while client.is_logged_in:
        if currchannel:
            client.send_message(currchannel, raw_input(currchannel.name + '>'))
            print(raw_input(currchannel.name + '>'))

t = threading.Thread(target=read_in)
# Kills the thread when the program closes
# Otherwise you would have to kill it manually
t.daemon = True
t.start()

client.run()
