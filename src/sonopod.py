#!/usr/bin/env python2.7

#stdlib
import os.path
import urllib
import logging
from collections import namedtuple
from builtins import input

try:
    import cPickle as pickle
except ImportError:
    import pickle

# imports, see requirements.txt
import podcastparser # get `podcastparser` with pip
import soco # get `soco` with pip
from clint import resources # get `clint` with pip
from clint.textui import colored  # get `clint` with pip
resources.init('lurtgjort.no', 'SonoPod')

Podcast = namedtuple('Podcast', 'title, url')
Episode = namedtuple('Episode', 'title, description, url')

class Library(object):
    def __init__(self):
        #'Read from cache'
        try:
            self.library = pickle.loads(resources.user.read('library.db'))
        except TypeError:
            #new library
            self.library = []
        logging.debug('init Library, currently: %r', self.library)

        """
        for (i,z) in enumerate(self.library):
            if z.title is None:
                del(self.library[i])
        self.save()
        """
                

    def save(self):
        'Save self.library to cache'
        return resources.user.write('library.db', pickle.dumps(self.library))

    def add(self, resource):
        'Add resource to self.library if it doesnt exist'
        if resource.url in self:    
            return None

        logging.debug('adding resource to ibrary: %r', resource)
        self.library.append(resource)
        return self.save()

    def __contains__(self, url):
        for e in self.library:
            if e.url == url:
                return True
        return False

    @property
    def self(self):
        return self.library
    

class PodcastParser(object):
    def __init__(self, url):
        self.url = url
        # get the 5 last episodes from podcast at url (podcastparser sorts by published date)
        self.pc = podcastparser.parse(self.url, 
                                      stream=urllib.urlopen(self.url),
                                      max_episodes=5)
        self.episodes = []

    def _s(self, s):
        'Normalize and remove any cruft from string'
        return podcastparser.squash_whitespace(podcastparser.remove_html_tags(s))

    def getTitle(self):
        'Get Podcast title'
        return self.pc['title']

    def getEpisodes(self):
        if len(self.episodes) == 0:
            logging.debug('Slurping podcast url: %r', self.url)
            self.episodes =  [Episode(self._s(e['title']),
                                      self._s(e['description']),
                                      e['enclosures'][0]['url']) for e in self.pc['episodes']]
        return self.episodes

class SonosPlayer(object):
    def __init__(self):
        self.players = soco.discover()
        self.default = list(self.players)[0]

    def play(self, episode):
        logging.debug('Playing episode %r on %r', episode, self.default)
        self.default.play_uri(uri=episode.url,
                              #meta= , # DIDL format
                              title=episode.title,
                              start=True)

def chooseFrom(title, prompt, iterable):
    print(colored.blue(title))
    for (idx,e) in enumerate(iterable, start=1):
        print(colored.green('[{}]\t {} '.format(idx, e.title.encode('utf-8'))))

    idx = -1
    while not 0 <= idx < len(iterable):
        try:
            idx = int(input(prompt+'> '))-1 # deduct 1 b/c zero indexing
        except ValueError:
            pass
        except (KeyboardInterrupt, EOFError) as e:
            print('\n')
            sys.exit(1)
    return iterable[idx]


if __name__=='__main__':
    logging.basicConfig(level=logging.WARNING)
    import sys

    from clint.textui import prompt, validators # get `clint` with pip
    from clint import arguments
    args = arguments.Args()

    lib = Library()
    player = SonosPlayer()

    podcasturl = args.get(0)
    if podcasturl is not None: # optional url on command line
        podcasturl = podcastparser.normalize_feed_url(podcasturl)
        if podcasturl is None:
            logging.error('invalid url on command line')
            print('This is not a valid url')
            sys.exit(1)
        logging.debug('Getting podcast url: %r', podcasturl)
        pod = PodcastParser(podcasturl)
        lib.add(Podcast(pod.getTitle(), podcasturl))
    else:
        # no podcast url on command line, get a list from library
        pc = chooseFrom('Podcasts in library', 'Choose podcast', lib.self)
        pod = PodcastParser(pc.url)

    eps = pod.getEpisodes() 
    logging.debug('Got episodes : %r', eps)

    playthis = chooseFrom('Available episodes', 'Which episode to play', eps)
    logging.debug('Got episode %r from user input', playthis)

    player.play(playthis)

