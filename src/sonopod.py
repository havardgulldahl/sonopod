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

if __name__=='__main__':
    logging.basicConfig(level=logging.DEBUG)
    import sys
    import argparse
    parser = argparse.ArgumentParser(
        description='Play podcasts on you Sonos from the command line')
    parser.add_argument('podcasturl', help='The url of the podcast')
    args = parser.parse_args()

    logging.debug('Getting podcast url: %r', args.podcasturl)
    pods = SimplePodcasts(args.podcasturl)
    eps = pods.getEpisodes() 
    logging.debug('Got episodes : %r', eps)

    for (idx,ep) in enumerate(eps, start=1):
        print('[{}]\t {} - {} '.format(idx, ep.title, ep.url))




    
    
    


