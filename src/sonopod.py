#!/usr/bin/env python2.7

#stdlib
import urllib
import argparse
import logging
from collections import namedtuple

# imports, see requirements.txt
import podcastparser # get it with pip
import soco # get it with pip

Episode = namedtuple('Episode', 'title, description, url')

class SimplePodcasts(object):
    def __init__(self, url):
        self.url = url
        self.episodes = []

    def getEpisodes(self):
        if len(self.episodes) == 0:
            logging.debug('Slurping podcast url: %r', self.url)
            pc = podcastparser.parse(self.url, urllib.urlopen(self.url))
            self.episodes =  [Episode(e['title'], e['description'], e['enclosures'][0]['url']) for e in pc['episodes']]
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

if __name__=='__main__':
    logging.basicConfig(level=logging.INFO)
    import sys
    import argparse
    from builtins import input

    parser = argparse.ArgumentParser(
        description='Play podcasts on you Sonos from the command line')
    parser.add_argument('podcasturl', help='The url of the podcast')
    args = parser.parse_args()

    logging.debug('Getting podcast url: %r', args.podcasturl)
    pods = SimplePodcasts(args.podcasturl)
    eps = pods.getEpisodes() 
    logging.debug('Got episodes : %r', eps)

    for (idx,ep) in enumerate(eps, start=1):
        print('[{}]\t {} '.format(idx, ep.title.encode('utf-8')))

    playthis = -1
    while not 0 < playthis < len(eps):
        try:
            playthis = int(input('Which episode to play> '))-1 # deduct 1 b/c zero indexing
        except ValueError:
            pass
    logging.debug('Got episode index %r from user input', playthis)

    player = SonosPlayer()
    player.play(eps[playthis])

