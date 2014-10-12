import data
import vlc
import os
import gui

class Player:
    '''Contains all music playing methods, and wraps vlc.py'''

    def end_callback(self, event):
        '''Called when the song ends.'''
        gui.Home.title('Souno Beta Player, Nothing playing')

    def meta_parsed_callback(self, event):
        '''Handles the changing of the meta-data display.'''
        gui.Home.title('Souno Beta Player, %s' % 'Now Playing')
        print(event)

    def change_media_callback(self, event):
        if self.media.is_parsed():
            print('media was parsed, setting title.')
            gui.Home.title('Souno Beta Player, %s' % self.media.get_meta(vlc.Meta.Title))
        else:
            print("media wasn't parsed, setting callback.")
            self.media_event_manager = self.media.event_manager()
            self.media_event_manager.event_attach(vlc.EventType.MediaParsedChanged, self.meta_parsed_callback)


    def __init__(self):
        '''Initializes a vlc MediaPlayer instance, and sets callbacks.'''
        self.instance = vlc.Instance()
        self.player = self.instance.media_player_new()
        self.event_manager = self.player.event_manager()

        self.event_manager.event_attach(vlc.EventType.MediaPlayerEndReached, self.end_callback)
        self.event_manager.event_attach(vlc.EventType.MediaPlayerMediaChanged, self.change_media_callback)

        return
    def play(self, path):
        '''plays a song from a file path'''

        #Does souno have permission to read the file?
        movie = os.path.expanduser(path)
        if not os.access(movie, os.R_OK):
            print('Error: %s file not readable' % movie)
            return False

        #TODO- Organise for two players, so the tracks change quick.

        self.media = self.instance.media_new(movie)
        self.player.set_media(self.media)
        self.player.play()
        self.media.parse_async()