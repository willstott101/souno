from tkinter import filedialog
import data
import gui


class FolderWatcher:
    '''Watches folders.'''
    folders = []
    playlists = []

    def update(self):
        '''Loads watchfolders, and populates playlists with files found.'''

        #TODO - Populate playlists with .mp3 files.
        #Probably a method for finding files with given extensions in data.py

        self.folders = data.playlists.parser.items(section='watchfolders')
        data.playlists.save()
        return self.folders

    def new(self, name=None, path=None):
        '''Create a watchfolder if it didn't exist.'''
        # Did we get a path?
        if path is None:
            #Ask the user for a path
            path = filedialog.askdirectory(title='Add Watched Folder')
        if path is '':
            #Cancel if the user cancels
            return
        #Did we get a name?
        if name is None:
            #Find next available default name
            i = 1
            while data.playlists.has_option('watchfolders', 'folder' + str(i)):
                i += 1
            name = 'folder' + str(i)
        #Add the folder to the file
        data.playlists.parser.set('watchfolders', name, path)
        #Apply change
        self.update()
        #Update gui (assumes visible when folder added)
        self.display(gui.Home)

    def remove(self, name):
        '''Removes given watchfolder from the list.'''
        print('Clicked remove button for: ' + name)
        if data.playlists.has_option('watchfolders', name):
            data.playlists.parser.remove_option('watchfolders', name)
        self.update()
        self.display(gui.Home)

    def display(self, parent):
        # Clear the current objects
        for f in gui.watchfolders:
            f.destroy()
        gui.watchfolders = []
        gui.Home.update()
        #Organise carefully
        y = 0
        for f in self.folders:
            #Add folder name
            gui.watchfolders.append( gui.Label(parent, text=f[0]) )
            gui.watchfolders[len(gui.watchfolders) -1].grid(row=y, column=0)
            #Add folder path
            gui.watchfolders.append( gui.Label(parent, text=' at ' + f[1], fg='gray') )
            gui.watchfolders[len(gui.watchfolders) -1].grid(row=y, column=1)
            #Add delete button
            gui.watchfolders.append( gui.Button(parent, text='Remove', bg='gray', command=
                lambda _foo=f[0]: self.remove(_foo)) )
            gui.watchfolders[len(gui.watchfolders) -1].grid(row=y, column=2)
            #Add play button
            #TODO- Remove this, replace with library.
            gui.watchfolders.append( gui.Button(parent, text='Play', fg='red', command=
                lambda _foo=f[1]: data.player.play(data.crawler.crawl_folder(_foo)[0])) )
            gui.watchfolders[len(gui.watchfolders) -1].grid(row=y, column=3)
            y += 1
        #Place a button to add new folders
        gui.watchfolders.append( gui.Button(parent, text="Add", command=self.new) )
        gui.watchfolders[len(gui.watchfolders) -1].grid(row=y, column=2)

    def __init__(self):
        '''Loads watchfolders from config'''
        gui.watchfolders = []
        self.update()
