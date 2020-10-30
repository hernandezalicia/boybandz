'''
Functions to scrape ranker to gather boyband list as well as to scrape
Genuis API to generate lyric data set.
'''
from bs4 import BeautifulSoup
import os
import pandas as pd
import re
import requests

from tokens import *

#ranker url where we found top 25 boybands
ranker_url = 'https://www.ranker.com/list/boy-band-bands-and-musicians/reference?ref=browse_list&l=1'

def scrape_ranker(url):
	'''
	scrapes input url from ranker and returns a dictionary
	where keys are the ranks and values as the associated
	band names
	'''
	page = requests.get(url)
	html = BeautifulSoup(page.text, "html.parser")

	table = html.find_all("div", class_ = "gridItem_itemContent__2PCCh")

	band_names = {}

	for band in table:
		name = band.find('a').contents[0]
		ban_names[rank] = name

		rank += 1

	return band_names

def _check_genius_result(json):
	return len(json['response']['hits']) > 0

def gather_song_info(artist_names, song_limit = 100):
	all_songs = []

	for artist in artist_names:
		artist_info = pd.DataFrame(_get_artist_info(artist, song_limit))
		all_songs.append(artist_info)

	all_songs = pd.concat(all_songs)

	return all_songs

def _get_artist_info(artist, song_limit):
	base_url = 'https://api.genius.com'
	headers = {'Authorization': 'Bearer ' + API_KEY}
	data = {'q': artist}

	page = 1
	keep_going = True

	artist_results = []

	while keep_going:
	    search_url = base_url + '/search?per_page=10&page=' + str(page)
	    response = requests.get(search_url, data = data, headers = headers)
	    
	    json = response.json()
	    if not _check_genius_result(json):
	        break
	    
	    for song in json['response']['hits']:
	        song_results = {}

	        if song['type'] != 'song':
	            print(song['type'])
	            continue

	        #checking to make sure this is a song by the artist we are looking for
	        if artist not in song['result']['primary_artist']['name']:
	            continue

	        song_results['id'] = song['result']['id']
	        song_results['artist'] = song['result']['primary_artist']['name']
	        song_results['name'] = song['result']['title']
	        song_results['url'] = song['result']['url']
	        song_results['pageviews'] = song['result']['stats']['pageviews'] if 'pageviews' in song['result']['stats'] else None
	        song_results['search_artist'] = artist
	        artist_results.append(song_results)

	    page += 1
	        
	    if len(artist_results) >= song_limit or page > 20:
	        keep_going = False

	return artist_results

def scrape_genius(artist_info):
	'''
	scrapes lyrics from urls in dataframe and writes to text files
	each text file will be written in a directory of the artist's name
	'''
	#make directories for artists we are interested in
	for artist in artist_info['search_artist'].unique():
		try:
			os.mkdir('data/' + artist.replace(' ', '_').lower())
		except FileExistsError:
			pass

	for index, song in artist_info.iterrows():
		url = song['url']
		artist_name = song['search_artist'].replace(' ', '_').lower()
		song_id = song['id']

		#checking if we have this file already so we can skip it
		if _check_songfile_exists('data/' + artist_name + '/{}.txt'.format(song_id)):
			continue

		page = requests.get(url)
		html = BeautifulSoup(page.text, "html.parser") # Extract the page's HTML as a string

		# Scrape the song lyrics from the HTML
		lyrics = html.find("div", class_="lyrics").get_text()

		#write the song to a text file
		file = open('data/' + artist_name + '/{}.txt'.format(song_id), 'w', encoding = 'utf-8')
		file.write(lyrics)
		file.close()

	print("Finished scraping {} songs.".format(len(artist_info)))


def _check_songfile_exists(path):
	return os.path.exists(path)

