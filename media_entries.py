from media import Movie, TvShow

import xml.dom.minidom

# Open XML document using minidom parser
DOMTree = xml.dom.minidom.parse("movies.xml")
document = DOMTree.documentElement
if document.hasAttribute("shelf"):
    print "Root element : %s" % document.getAttribute("shelf")

# Get all the movies in the document
movies = document.getElementsByTagName("movie")
tv_shows = document.getElementsByTagName("tv-show")

# collection - contains all Video Instances, both Movie and TvShow
collection = []

# Take all the movies and create a new Movie instance
for xml_movie in movies:
    if xml_movie.hasAttribute("title"):
        title = xml_movie.getAttribute("title")
        movie = Movie(title, xml_movie)
        # append the instance to our collection to be used on website
        collection.append(movie)


# Take all the movies and create a new TvShow instance
for xml_show in tv_shows:
    if xml_show.hasAttribute("title"):
        title = xml_show.getAttribute("title")
        show = TvShow(title, xml_show)
        # append the instance to our collection to be used on website
        collection.append(show)
