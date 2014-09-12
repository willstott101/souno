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

        #TODO - Create watchfolder specific .ini, store more info about each watchfolder.
        #i.e. date last crawled, and stuff.

        self.folders = data.cfg_watchfolders.parser.sections()
        data.cfg_watchfolders.save()
        return self.folders

    def new(self, name=None, path=None):
        '''Create a watchfolder if it didn't exist.'''
        # Did we get a path?
        if path is None:
            #Ask the user for a path
            path = filedialog.askdirectory(title='New Watched Folder')
        if path is '':
            #abort because the user cancelled
            return
        #Did we get a name?
        if name is None:
            #Find next available default name
            i = 1
            while data.cfg_watchfolders.has_section( 'folder' + str(i) ):
                i += 1
            name = 'folder' + str(i)
        #Add the folder to the file
        data.cfg_watchfolders.parser.add_section(name)
        data.cfg_watchfolders.parser.set(name, 'path', path)
        #Apply change
        self.update()

        #Update gui (assumes visible when folder added)
        self.display(gui.Home)

    def remove(self, name):
        '''Removes given watchfolder from the list.'''
        print('Clicked remove button for: ' + name)
        if data.cfg_watchfolders.parser.has_section( name ):
            data.cfg_watchfolders.parser.remove_section( name )
        self.update()

        #TODO- Display watchfolders in a better place.
        self.display(gui.Home)

    def display(self, parent):
        # Clear the current objects
        for f in gui.watchfolders:
            f.destroy()
        gui.watchfolders = []
        gui.Home.update()
        #Organise carefully
        y = 1
        for f in self.folders:
            p = data.cfg_watchfolders.parser.get(f, 'path')
            #Add folder name
            gui.watchfolders.append( gui.Label(parent, text=f ))
            gui.watchfolders[len(gui.watchfolders) -1].grid(row=y, column=0)
            #Add folder path
            gui.watchfolders.append( gui.Label(parent, text=' at ' + p, fg='gray') )
            gui.watchfolders[len(gui.watchfolders) -1].grid(row=y, column=1)
            #Add delete button
            gui.watchfolders.append( gui.Button(parent, text='Remove', bg='gray', command=
                lambda _foo=f: self.remove(_foo)) )
            gui.watchfolders[len(gui.watchfolders) -1].grid(row=y, column=2)
            #Add play button
            #TODO- Remove this, replace with library.
            gui.watchfolders.append( gui.Button(parent, text='Play', fg='red', command=
                lambda _foo=p: data.player.play(data.crawler.crawl_folder(_foo)[0])) )
            gui.watchfolders[len(gui.watchfolders) -1].grid(row=y, column=3)
            y += 1
        #Place a button to add new folders
        gui.watchfolders.append( gui.Button(parent, text="Add", command=self.new) )
        gui.watchfolders[len(gui.watchfolders) -1].grid(row=y, column=2)

    def __init__(self):
        '''Loads watchfolders from config'''
        gui.watchfolders = []
        self.update()
