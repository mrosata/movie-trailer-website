# (Udacity) Movie Trailer Website

What this program will do:

 * Show Videos, movies and tvshows in Pinterest style grid
 * Allow user to view youtube trailer on movies (not tvshows)
 * Allow filtering of videos by type, title, and star rating on imdb.com
 * Check out how it looks in this [youtube video](https://www.youtube.com/watch?v=Z6wOsNLxM3c)!  :+1:


### Requirements and setup
This application requires python 2.7 and the Flask package. It has been tested in Chrome only. If you have virtualenv, that would great as well. To install flask and start the webserver, just follow the steps below.

```sh
# Execute these 2 commands and then open a web browser (Chrome) to http://127.0.0.1:5000 or http://localhost:5000
$ pip install flask
$ python main.py
```

### Add your own Videos using XML
The video objects Movie and TvShow are written in Python, but they get their information from an easy to read, easy to edit .xml file cleverly named `movies.xml`. If you want to add your own videos to this website, just add them one at a time to the file using this format:
```xml
<collection type="media">
	<!-- Nest videos inside the element <collection...-->
	<movie title="Still Alice">
        <date>2014</date>
        <time>101</time>  <!-- Time is in min, don't add prefix -->
        <category>Drama</category>
        <rating>7.5</rating>
        <rated>PG-13</rated>
        <story>A linguistics professor and her family find their bonds tested when she is diagnosed with Alzheimer's Disease.</story>
        <image>still_alice.jpg</image>  <!-- Images can be local references, or external links-->
        <stars>Julianne Moore, Alec Baldwin, Kristen Stewart</stars>
        <youtube>ZrXrZ5iiR0o</youtube>  <!-- find id # in url youtube.com/watch?v=########## -->
    </movie>
    
    <!-- This is an example of a TV Show, which doesn't have a trailer -->
    <tv-show title="Modern Family">
        <date>13 May 2015</date>
        <time>22</time>
        <category>Comedy</category>
        <rating>9.7</rating>
        <rated>TV-PG</rated>
        <story>As Gloria tries to ruin Manny's sentimental life, Claire doubts about her professional career and Alex skips day</story>
        <image>modern_family_ver11.jpg</image>
        <stars>Ed O'Neill, Sofía Vergara, Julie Bowen</stars>
        <season>6</season>
        <episode>22 - Crying Out Loud</episode>
        <station>ABC</station>
    </tv-show>
```
In the JavaScript, I've made it possible for users to filter the html containers of each video by `title`, `rating` and `type`. The `title` and `rating` values, which are parsed from this `movies.xml` file by Python are also written as data-* attributes into the html containers and then tacked onto the JavaScript Object version of each video. If you want to create a new filter for another attribute such as `time`, all the information is already in a JavaScript object set up just for you! All you need to do is reference the JS variable `videotiles` which holds a copy of every video object Python created on the page, and references to their html and jQuery representation of the its `.video-tile` on the page. Each JavaScript Video object has the following properties and methods.
```js
category:      // str, comma seperated video categories eg: "Drama"
classes:       // str, classList, this is needed for some tricky stuff
date: "2014"   // int, year video was released
onShelf: true  // bool, whether the .video-tile is still on the page
rated: "PG-13" // str, Video rating
rating: 7.5    // float, imdb.com rating
time: "101"    // int, length in minutes
title:         // str, Title of video
type:          // str, "movie" or "tv-show"
elm:           // HTMLElement, vanilla JS of HTML .video-tile
$:             // jQuery object, jQuery ref to .video-tile (can use any jQuery method on it)
removeVideo: function () {... // will remove the video-tile from grid if it is present
appendVideo: function () {... // will return the html video-tile to grid only if not present
```

### Change is good
Feel free to play around with the code and make something cool, but don't run into the dungeon without your torch unless you like bumping into walls and breaking things. Uncomment the line `# app.debug = True` and take advantage of Flasks amazing debug feature which will print Exception stack traces straight out to the browser! (Unless you crash the application completely) It even reloads files and modules when they are changed, so you don't get stuck doing this:
```
while 1 > 0:
    scratch_head()
    change_something()
    CTRL+C
    python main.py
```
    
If for some reason you don't want to run the application from the default port, you can change this at the bottom of the file `main.py`. By default it will attempt to handle requests on localhost:5000. Maybe we want to use something more familiar like:
```py
if __name__ == '__main__':
    # app.debug = True    <--- uncomment this when making any changes!
    # app.run()           <--- Default port 5000
    app.run(port=8080) #  <--- Define your own port instead

```

There are many other options you can pass into the Flask app and I encourage you to [learn more about Flask here](http://flask.pocoo.org/docs/0.10/quickstart/). Any questions about this project can be directed towards [mike@stayshine.com](mike@stayshine.com).

### Credit to give where credit is due:


 * [PyCharm IDE (Free!)](https://www.jetbrains.com/pycharm/download/) for the awesome syntax-highlighted editor.
 * [imdb.com](http://imdb.com) where I ctrl+c'ed all my movie information.
 * [Movie Poster Awards](http://www.impawards.com/) where the higher res movie poster were found.
 * [youtube video](https://www.youtube.com/watch?v=Z6wOsNLxM3c) where the movie trailers live.
 * [Udacity Full Stack Nanodegree](http://udacity.com/course/nd004), for those who want to learn concepts from this. project.
 * [Pinterest style jQuery plugin](http://www.bootsnipp.com/snippets/featured/pinterest-like-responsive-grid)
 * [Bootstrap](http://getbootstrap.com/)
 * [jQuery](http://jquery.com)
 * [markdown-it](https://github.com/markdown-it/markdown-it) for Markdown parsing.
