import configparser


class DataStore:
    '''Class to control references to saved data.'''

    def save(self):
        '''Saves the currently loaded config to file.'''
        # Open/Create the file, in a safe way.
        #The 'with' method auto-closes the file.
        with open(self.filename, mode='w', encoding='utf-8') as fileobj:
            #(Re)Write the config.
            self.parser.write(fileobj)

    def has_section(self, section):
        '''Shortcut to self.parser.has_section()'''
        return self.parser.has_section(section)

    def has_option(self, section, option):
        '''Shortcut to self.parser.has_option()'''
        return self.parser.has_option(section, option)

        # Called when class is instanced.

    def __init__(self, filename, defaults={}):
        '''Reads the file at 'filename'.'''

        #Store the filename
        self.filename = filename

        #Create a parser to read/write to/from objects.
        self.parser = configparser.ConfigParser(defaults)

        #Load the data file (.ini)
        self.parser.read(filename)