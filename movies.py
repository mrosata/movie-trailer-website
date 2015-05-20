# #Description#
# Command Line Tool for Movie Project of
# the Udacity Full Stack Web Developer Nano Degree
#
# With this Programm it is possible to search for Movies and add them 
# to a Favorites Databse. The whole Programm works from your commandline.
# 
# Once you are done collecting your videos you can hit the "s" key 
# (for show) and a stand alone HTML Page will be generated with 
# the content of the DB. Media Resources will be fetched from the web.

# #License#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# #Author#
# ToM Krickl

# #Date#
# Last Update 18 May 2015
#
# Please see GitHub changelog

# #Technical#
# 1. When called from the Commandline the Program is looking for a db in the, 
# local folder. If it does not exist it creates one and generates the table
# needed.
# 2. The Programm goes into the main communication loop, lists the main usage
# paramenters and waits for a input.

# ### input is a movie name ###
# 1. with the input a GET request is sent to omdbapi.com and the result is
# displayed to the user for selection.
# 2. the id of the selection is used to send another GET request to collect
# the whole data from omdbapi
# 3. the movie trailer is collected form youtube by selecting the first 
# search result with a regex expression. to get the right trailer 
# "official trailer" is added to the movies title for search
# 4. the later needed data is stored to the db. 

# ### input is l > LIST ###
# a list of all entries in the database is printed out to the commandline

# ### input is d > DELETE ###
# a list of all entries is printed to the commandline. the user can select
# one of the entries to delete it.

# ### input is q > QUIT ###
# the program breaks the main communication loop, closes the connection to 
# the database and ends

# ### input is s > SHOW ###
# all data is fetched from the db as a list of dicts, converted into a list
# of movie objects and then sent to the fresh_tomatoes.py (provided by 
# Udacity) to generate a html page from the content. 
# this html page is then opend in your web browser

## main program

# Import Modules
import urllib
import json
import re
import os
import sqlite3
import sys
# import fresh_tomatoes

# Setup program wide variables
omdb = "http://www.omdbapi.com/"
youtube = "https://www.youtube.com/"
imdb = "http://www.imdb.com/"

### serach
# Send GET request to URL with Parameters in dic_query
# if response is json you can get a dict from it back by setting 
# return_dict to True
def search (url,dic_query,return_dict=False):
	'''search (url,dic_query[,return_dict=False])

	sends a GET request to the url and returns the fetched data.
	if the response is a json you can set return_dict True to convert
	the response to a python dictionary

	url: the url to connect to 
		e.g.: https://www.youtube.com/result
	dic_query: the GET parameters to be sent e.g.: 
		s = what to search > {"s":"what to search"}
	return_dict: if the feedback from the website is a json
		you can get back a dict if you set this to true.
	'''
	search = urllib.urlopen(url+"?"+urllib.urlencode(dic_query))
	result = search.read()
	search.close()
	if return_dict:
		# generate dict from json result and return it
		return json.loads(result)
	else:
		return result


### main communication loop
def user_com(DB):
	'''main command line user communication. 
	this schould be startet after the db is inizialised.

	the database must be given as object
	'''
	# main communication look, is left if user input is q
	while 1:
		print '\nUSAGE: \nq to quit, \ns for show website,\n',\
				'l for list entries, \nd for deleting items,\n',\
				'in seach result 0 for new search\n'

		search_input = raw_input("What movie do you like best? \n")

		# end the programm
		if search_input == "q":
			break

		# create a list of movie objects then generate the stand alone
		# website with the fresh_tomatoes module
		elif search_input == "s":
			lst_movies = DB.get_list()
			movies = []
			for elem in lst_movies:
				movies.append(movie(elem))
			fresh_tomatoes.open_movies_page(movies)

		# print a list of all entries in the database
		elif search_input == "l":
			print "Movies currently in DB"
			DB.print_list()
		
		# delete one of the entries in the database
		elif search_input == "d":
			print "Movies currently in DB"
			DB.print_list()
			del_input = raw_input(
						"Which one would you like to delete? 0 for none \n")
			if del_input != "0":
				# catch of false user input
				try: 
					#if user input is a valid number delete the movie from db
					DB.delete_entry(int(del_input))
				except:
					print "\nIMPORTANT: Please enter only one of the ID's.\n"
		else:
			# get the search result from omdb
			search_dict = {"s":search_input}
			result = search(omdb,search_dict,True)

			if "Search" in result:
				count = 1
				for elem in result["Search"]:
					print count, elem["Title"], elem["Year"], elem["Type"]
					count += 1

				question = "Which movie did you mean? "+\
							"Please enter the Index Number: "
				movie_selected = raw_input(question)
				if movie_selected == "0":
					pass
				else:
					# catch for false user input
					try:
						# if user input is a valid number get the movie data
						dic_movie = get_movie_data(result["Search"]\
							[int(movie_selected)-1]["imdbID"])
						# then write the data to db
						DB.new_entry(dic_movie)
					except:
						print "\nIMPORTANT: Please enter only one of",\
								"the Numbers.\n"
					
			else:
				print "Sorry no result. Please try again."
	return

### get movie data from ombd with the given imdbID
def get_movie_data(imdbID,trailer=True):
	'''function to get movie data from the open movie database based
	on a given imdb id.

	returns a dict with a data to the movie including the youtube trailor
	and the imdb link.
	
	fields included are:
	Plot, Rated, tomatoImage, Title, DVD, tomatoMeter, Writer,
	tomatoUserRating, Production, Actors, tomatoFresh, Type, imdbVotes, 
	Website, tomatoConsensus, Poster, tomatoRotten, Director, Released, 
	tomatoUserReviews, Awards, Genre, tomatoUserMeter, imdbRating, 
	Language, Country, BoxOffice, Runtime, tomatoReviews, imdbID, Metascore,
	Response, tomatoRating, Year, Trailer, imdbURL
	'''
	search_string = {"i":imdbID,"plot":"short","tomatoes":"true"}
	result = search(omdb,search_string,True)

	if trailer:
		yt_id = get_trailer(result["Title"]+" "+result["Year"])

		result["Trailer"] = yt_id

	result["imdbURL"] = imdb +'title/'+imdbID

	return result

### get trailer from youtube serarch result
def get_trailer(movie):
	'''searches youtube for movie name plus "trailer official" and 
	returns the id of the first search result
	'''
	search_text = movie+" trailer official"
	search_string = {"search_query":search_text}
	result = search(youtube+'results',search_string)

	# part of youtube website we want to search for
	# regex search for: 
	# "yt-lockup-title"><a href="/watch?v=GWU-xLViib0"
	# we want to extract the id after /watch?v=

	match = re.search('\"yt-lockup-title\"\>\<a href=\"\/watch\?v\=([\w|\d|-|_]+)\"\s',result)
	if match:
		return match.group(1)
	else:
		return None

### Database Class
class db():
	'''class for the database methods.
	on init a database file and table will be generated if it doesn't exist. 

	main methods are:
	new_entry(dic_movie) dic_movie should be generated from get_movie_data
		and must include: Title, Plot, Rated, Poster, Trailer, tomatoRating,
		imdbRating, imdbURL
	get_list() returns a list of movies as dictionary
	delete_entry(id) deletes the movie with the given id from db 
	close() closes the connection to the database
	'''
	# ###db init###
	def	__init__(self):
		# search current folder and if db does not exist allready, create one
		create_db = True
		for l_file in os.listdir("./"):
			if l_file == "movies.db":
				create_db = False

		self.con = sqlite3.connect("movies.db")
		self.c = self.con.cursor()
		self.nextid = 1
		if create_db:
			self.c.execute('''CREATE TABLE movies
	         	(id INTEGER,
	         	Title text, 
	         	Plot text, 
	         	Rated text, 
	         	Poster text,
	         	Trailer text, 
	         	tomatoRating text, 
	         	imdbRating text,
	         	imdbURL text)''')
			self.con.commit()
		else:
			count = self.c.execute('SELECT * FROM movies').fetchall()
			self.nextid = count[-1][0]+1

	# close the connection to the db object
	def close(self):
		self.con.close()

	# create now db entry with the given dict 
	# in the dict there can be much more but we just take the elements
	# that we want to store for later usage
	def new_entry(self,dict_movie):
		insert = (self.nextid,
			dict_movie["Title"],
			dict_movie["Plot"],
			dict_movie["Rated"],
			dict_movie["Poster"],
			dict_movie["Trailer"],
			dict_movie["tomatoRating"],
			dict_movie["imdbRating"],
			dict_movie["imdbURL"])
		self.c.execute('INSERT INTO movies VALUES (?,?,?,?,?,?,?,?,?)',insert)
		self.con.commit()
		self.nextid += 1

	# print a list of elements in the db
	def print_list(self):
		list_entries = self.get_list()
		for elem in list_entries:
			print '#'+str(elem["id"])+" "+elem["Title"]

	# return a list of dicts of all elements in db
	def get_list(self):
		db_entries = self.get_entries()
		list_entries = []
		for elem in db_entries:
			dic_elem={}
			dic_elem["id"] = elem[0]
			dic_elem["Title"] = elem[1]
			dic_elem["Plot"] = elem[2]
			dic_elem["Rated"] = elem[3]
			dic_elem["Poster"] = elem[4]
			dic_elem["Trailer"] = elem[5]
			dic_elem["tomatoRating"] = elem[6]
			dic_elem["imdbRating"] = elem[7]
			dic_elem["imdbURL"] = elem[8]
			list_entries.append(dic_elem)
		return list_entries

	# return a list of tuples of all elements in the db
	def get_entries(self):
		result = self.c.execute('SELECT * FROM movies').fetchall()
		return result

	# delete the element with the given id
	def delete_entry(self,elem_id):
		result = self.c.execute('DELETE FROM movies WHERE "id" = ?',str(elem_id))
		return result

### Movie Class
# creates a movie object with the given dict
class movie():
	''' just creates an object of a movie '''
	def __init__(self,dict_movie):
		self.id = dict_movie["id"]
		self.title = dict_movie["Title"]
		self.plot = dict_movie["Plot"]
		self.rated = dict_movie["Rated"]
		self.poster = dict_movie["Poster"]
		self.trailer = dict_movie["Trailer"]
		self.tomatoRating = dict_movie["tomatoRating"]
		self.imdbRating = dict_movie["imdbRating"]
		self.imdbURL = dict_movie["imdbURL"]

	# the representation of one movie object is it's id and the title 
	def __repr__(self):
		repr = "#"+str(self.id)+" "+self.Title
		return repr

if __name__ == "__main__":
	# if startet form command line
	#
	# 1. setup database and set Index
	# 2. start user communication
	# 3. if finished close connection and end programm
	DB = db()
	user_com(DB)
	DB.close()