#!/usr/bin/python

import sys
sys.path.insert(0, 'ext-libs') 
sys.path.insert(0, 'libs')
import data
import datastore
import watchfolders
import player
import crawler
import gui

#instantiate a Tk window
gui.Home = gui.Tk()
#set the title of the window
gui.Home.title('Tk test')
#set the size+position of the window
gui.Home.geometry('1200x800+200+100')
#dunno what this does, fixes some of filedialog if I use it.
gui.Home.update()

#Read the config file, and/or define and save defaults.
data.cfg_config = datastore.DataStore('config.ini', defaults = {
	'lang': 'EN'
})
data.cfg_config.save()

#Load the user's playlists and stuff.
data.cfg_watchfolders = datastore.DataStore('playlists.ini')
data.cfg_watchfolders.save()

#Create a folderwatcher object to watch folders.
data.folderwatcher = watchfolders.FolderWatcher()

#Create a player instance.
data.player = player.Player()

#Create a crawler instance
data.crawler = crawler.Crawler()

#Draw the folder object on the screen -TEMP
#TODO- Replace this, move to a menu window.
data.folderwatcher.display(gui.Home)
