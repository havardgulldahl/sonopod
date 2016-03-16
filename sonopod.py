#!/usr/bin/env python2.7

#stdlib
import sys
import os.path
import urllib
import logging
from collections import namedtuple
from builtins import input

Podcast = namedtuple('Podcast', 'title, url')
Episode = namedtuple('Episode', 'title, description, url')

"""
try:
    import cPickle as pickle
except ImportError:
    import pickle
"""
import pickle

# imports, see requirements.txt
import podcastparser # get `podcastparser` with pip
import soco # get `soco` with pip
from clint import resources # get `clint` with pip
from clint.textui import colored  # get `clint` with pip
resources.init('lurtgjort.no', 'SonoPod')

class Library(object):
    def __init__(self):
        #'Read from cache'
        logging.info('read lib from %r', resources.user)
        try:
            self.podcasts = [Podcast(**e) for e in pickle.loads(resources.user.read('podcasts.db'))]
        except TypeError as e:
            #new library
            logging.exception(e)
            self.podcasts = []
        logging.info('init podcasts Library, currently: %r', self.podcasts)

        """
        for (i,z) in enumerate(self.podcasts):
            if z.title is None:
                del(self.podcasts[i])
        self.save()
        """

    def save(self):
        'Save self.podcasts to cache'
        prepared = [dict(vars(p)) for p in self.podcasts]
        logging.info('pik: %r', prepared)
        return resources.user.write('podcasts.db', pickle.dumps(prepared, protocol=2))

    def add(self, resource):
        'Add resource to self.podcasts if it doesnt exist'
        if resource.url in self:    
            return None

        logging.debug('adding resource to ibrary: %r', resource)
        self.podcasts.append(resource)
        return self.save()

    def __contains__(self, url):
        for e in self.podcasts:
            if e.url == url:
                return True
        return False

    @property
    def self(self):
        return self.podcasts
    

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
        if len(self.players) == 0:
            raise Exception('No Sonos players found')
            
        self.default = list(self.players)[0]

    def play(self, episode):
        logging.debug('Playing episode %r on %r', episode, self.default)
        self.default.play_uri(uri=episode.url,
                              #meta= , # DIDL format
                              title=episode.title,
                              start=True)

def chooseFrom(title, prompt, iterable):
    'Helper function to interactively choose one item from an iterable'
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

def main():
    'Main function. '
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

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    main()
