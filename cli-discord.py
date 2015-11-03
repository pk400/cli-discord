import discord
import logging
import sys
import threading
import os
import curses

# Set up the logging module to output diagnostic to the console.
logging.basicConfig()

client = discord.Client()
client.login(str(sys.argv[1]), str(sys.argv[2]))
currchannel = 0
screen = 0

class Screen(object):
    def __init__(self):
        self.line = 1
        self.screen = curses.initscr()
        
    def getScreen(self):
        return self.screen
        
    def addstr(self, x, s):
        self.screen.addstr(self.line, x, s)
        self.line += 1
    
    def refresh(self):
        self.screen.refresh()
     
    def outs(self):
        print self.line

if not client.is_logged_in:
    print('Logging in to Discord failed')
    exit(1)

@client.event
def on_ready():
#    os.system('clear')
#    global currline
#   currline = 1
    
    global screen
    screen = Screen()
    
    screen.getScreen().clear()
    screen.getScreen().border(0)
    screen.getScreen().addstr(0, 2, 'cli-discord - ' + client.user.name)
    screen.refresh()
    
    client.change_status(291, True)

@client.event
def on_message(message):
    if message.content.startswith('/ch'):
        screen.addstr(1, 'Joining channel ' + message.channel.name)
        global currchannel
        currchannel = message.channel
    if message.author.id != client.user.id:
        screen.addstr(1, '[' + message.channel.name + '] '
        + message.author.name + ': ' + message.content)
    screen.refresh()

def read_in():
    screen2 = curses.initscr()
    while client.is_logged_in:
        if currchannel:
            #msg = raw_input(currchannel.name + '>')
            msg = screen2.getstr(100, 100)
            #msg = screen.getScreen().getstr(100, 100).decode(encoding="utf-8")
            if len(msg) > 0:
                client.send_message(currchannel, msg)
            screen2.refresh()
    sys.exit(0)

t = threading.Thread(target=read_in)
# Kills the thread when the program closes
# Otherwise you would have to kill it manually
#t.daemon = True
#t.start()

try:
    client.run()
finally:
    curses.endwin()
