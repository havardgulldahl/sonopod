# sonopod
A simple command line podcast player for Sonos

## examples

### help text
```bash
$ ./sonopod.py --help
SonoPod is a command line client to feed your Sonos with podcasts
Copyright 2016 <havard@gulldahl.no>, GPLv3 licensed
Usage: sonopod.py [-h|--help] [--setsonos] [podcast_url]
    [-h|--help]		This help text
    [--setsonos]	Set default Sonos speaker
    [podcast_url]	Add a new podcast series to the library

    If run without arguments, presents a list of podcasts in the library
```

### set Sonos speaker

```bash
$ ./sonopod.py --setsonos
Choose a Sonos speaker
[1]	 Arbeidsrom
[2]	 Stue
Set default>
```

### add podcast series

```bash
$ ./sonopod.py http://www.thenakedscientists.com/naked_scientists_podcast.xml
Available episodes
[1]	 Cambridge Science Festival: Battle of the Brains
[2]	 The A - Zika of viruses: Preventing Pandemics
[3]	 Gravitational Waves: Discovery of the Decade?
[4]	 Could The Internet Die?
[5]	 Rules of Attraction: The Science of Sex
Which episode to play>
```


### listen to podcast from library

```bash
$ ./sonopod.py
Podcasts in library
[1]	 NRK – 200 år på 200 minutter
[2]	 NRK – Einstein – på sporet av den tøyde tid
[3]	 Everyday Einstein's Quick and Dirty Tips for Making Sense of Science
[4]	 NRK – Nyhetsmorgen
[5]	 Freakonomics Radio
[6]	 Valebrokk og Co.
[7]	 NRK – Ekko - et aktuelt samfunnsprogram
[8]	 NRK – Ytring
Choose podcast> 6
Available episodes
[1]	 Her bor fremtidens boligvinnere
[2]	 Må vaskehjelpen subsidieres for å få kvinner i full jobb?
[3]	 Lakselus til tross, vi har så vidt sett starten på lakseeventyret
[4]	 Økonomisk toppmøte: Èn ting er mer verdt enn oljen
[5]	 Hvor ille kan oljebremsen bli? Vi har spurt industritoppene før sentralbanksjefens årstale
Which episode to play> 2
```


