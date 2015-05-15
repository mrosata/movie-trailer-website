#!/usr/bin/python
__author__ = 'Michael Rosata mrosata1984@gmail.com'
__package__ = ''

import webbrowser
import xml.dom.minidom


class Video():
    """Video is the base class of TvShow and Movie. While you could create a
    video by simply doing the following:
        video = Video()
    The Video class offers a method to parse XML containing attributes of a
    typical Video, a minimal Video XML has attribute "title" on its root
    element and contains following elements ["story", "time", "stars", "date",
    "image", "category"]
    """
    type = 'video'

    def __init__(self):
        """Sets all the base properties or defaults"""
        self.title = 'Untitled'
        self.story = ''
        self.time = '0 min'
        self.rating = 0.0
        self.category = 'Mystery'
        self.date = ''
        self.rated = 'NR'
        self.image = ''
        self.stars = ''

    def parse_xml(self, _ml):
        """Parse properties of a video from an xml collection, basically this
        will just go through all the common properties to a Video object, ones
        that are shared between all instances of Video, look in __init__ for
        full list. Children of Video may call the parent class __init__ or just
        use this method to finish parsing any xml data.
        """
        try:
            self.story = _ml.getElementsByTagName('story')[0].childNodes[0].data
            self.time = _ml.getElementsByTagName('time')[0].childNodes[0].data
            self.stars = _ml.getElementsByTagName('stars')[0].childNodes[0].data
            self.category = \
                _ml.getElementsByTagName('category')[0].childNodes[0].data
            self.date = _ml.getElementsByTagName('date')[0].childNodes[0].data
            self.image = _ml.getElementsByTagName('image')[0].childNodes[0].data
            self.rating = float(
                _ml.getElementsByTagName('rating')[0].childNodes[0].data)
            self.rated = _ml.getElementsByTagName('rated')[0].childNodes[0].data
            self.date = _ml.getElementsByTagName('date')[0].childNodes[0].data
        except AttributeError:
            print "What did you do???"


class Movie(Video):
    """
    This class defines a movie and holds the properties that define a movie
    """
    VALID_RATINGS = ["NR", "G", "PG", "PG-13", "R"]
    type = 'movie'

    def __init__(self, title, _ml):
        """Initialize movie, pass in a title and XML collection that has the
        base requirements of a Video and also an image and youtube video link
        """
        self.title = title
        self.youtube = _ml.getElementsByTagName('youtube')[0].childNodes[0].data
        # use the parent Video method parse_xml to find common Video properties
        self.parse_xml(_ml)

    def show_trailer(self):
        """Opens a webbrowser with the preview for the current movie on youtube.
        Lucky for us we have the JavaScript to load videos right on page so we
        probably could remove this
        """
        webbrowser.open(self.youtube)


class TvShow(Video):
    """
    This class defines a movie and holds the properties that define a movie
    """
    VALID_RATINGS = ["NR", "TV-PG", "TV-MA"]
    type = 'tv-show'

    def __init__(self, title, _ml):
        """Initialize movie, pass in title and xml with season, station, as well
        as the base Video XML elements
        """
        self.title = title
        self.season = _ml.getElementsByTagName('season')[0].childNodes[0].data
        self.station = _ml.getElementsByTagName('station')[0].childNodes[0].data
        # use the parent Video method parse_xml to find common Video properties
        self.parse_xml(_ml)