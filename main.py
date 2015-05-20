__author__ = 'Michael Rosata'
"""
To make this project, we will satisfy the following:

Create a data structure
    - Video -->  Movie | TvShow
    - Create multiple instances and display in html
    - Be able to click Movie and see trailer. (TV Shows no)

Create a simple filtering drop-down to toggle movies/tvshows
Create a slider that sorts by ratings.
Make free-search input
"""
# flask to serve files
from flask import Flask, render_template, request

# collection contains all the Python Video instances, TvShow and Movie
from media_entries import collection

import movies

# setup globals
omdb = "http://www.omdbapi.com/"
youtube = "https://www.youtube.com/"
imdb = "http://www.imdb.com/"


# Initial the application
app = Flask(__name__)


# All Routing for Movie Website
@app.route('/')
def main_page():
    # Grab the media instances from collection
    media = get_media()
    # render the main/and only page
    return render_template('main.html',
                           media=media)

@app.route('/add/',methods=['GET','POST'])
def add_movie():
    form_data = request.form
    data = []
    if form_data:
        search_dict = {"t":form_data['movie'],"r":"json","plot":"short"}
        result = movies.search(omdb,search_dict,True)
        result['ytID'] = movies.get_trailer(result['Title'])
        result['Metascore'] = int(result['Metascore'])
        result['imdbRating'] = float(result['imdbRating'])
        result['add'] = True
        # result is something like 
        # {u'Plot': u"Katniss Everdeen voluntarily takes her younger sister's
        #  place in the Hunger Games, a televised fight to the death in which
        #   two teenagers from each of the twelve Districts of Panem are chosen
        #    at random to compete.",
        #     u'Rated': u'PG-13',
        #      u'Response': u'True',
        #      u'Language': u'English',
        #       u'Title': u'The Hunger Games',
        #        u'Country': u'USA',
        #         u'Writer': u'Gary Ross (screenplay), 
        #         Suzanne Collins (screenplay), 
        #         Billy Ray (screenplay), 
        #         Suzanne Collins (novel)', 
        #         u'Metascore': u'67', 
        #         u'imdbRating': u'7.3', 
        #         u'Director': u'Gary Ross',
        #          u'Released': u'23 Mar 2012', 
        #          u'Actors': u'Stanley Tucci, 
        #          Wes Bentley, Jennifer Lawrence, 
        #          Willow Shields', 
        #          u'Year': u'2012', 
        #          u'Genre': u'Adventure, Sci-Fi',
        #           u'Awards': u'Nominated for 1 Golden Globe. 
        #           Another 32 wins & 40 nominations.',
        #            u'Runtime': u'142 min', 
        #            u'Type': u'movie', 
        #            u'Poster': u'http://ia.media-imdb.com/xxx.jpg', 
        #            u'imdbVotes': u'609997', u'imdbID': u'tt1392170'}
        print result
        return render_template('add.html',data=result)
    else:
        return render_template('add.html')

@app.route('/add_this/<imdbID>')
def add_this(imdbID=None):
    return imdbID


# Grab the Video instances in collection
def get_media():
    if collection:
        return collection
    else:
        return []


# Don't need a secret, but secrets are fun.. shhhh
app.secret_key = 'ZaR%tC3SzAw48vm2./2!'
if __name__ == '__main__':
    app.debug = True
    app.run()