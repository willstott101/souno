from os import walk, path

class Crawler:
    '''Handles crawling of directories to check for music files.'''

    def crawl_folder(self, mypath):
        '''Crawls the first level of a folder.'''

        f = []
        for (dirpath, dirnames, filenames) in walk(mypath):
            f.extend(filenames)
            break
        pathlist = [path.join(mypath, pth) for pth in f]
        return [i for i in pathlist if i.endswith('.mp3')]