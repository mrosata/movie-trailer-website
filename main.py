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
from flask import Flask, render_template

# collection contains all the Python Video instances, TvShow and Movie
from media_entries import collection

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


# Grab the Video instances in collection
def get_media():
    if collection:
        return collection
    else:
        return []


# Don't need a secret, but secrets are fun.. shhhh
app.secret_key = 'ZaR%tC3SzAw48vm2./2!'
if __name__ == '__main__':
    # app.debug = True
    app.run()