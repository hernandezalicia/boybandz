'''
processing song files
'''
from nltk.corpus import stopwords
import numpy as np
import os
from string import punctuation
import re


def read_file(file):
	f = open(file, 'r', encoding = 'utf-8')
	lines = f.readlines()
	f.close()
	return lines

def clean_lyrics(file):
	song_id = file.split('\\')[-1].split('.txt')[0]
	lines = read_file(file)

	lyrics = ''

	for line in lines:
		lyrics += line

	stoppers = stopwords.words('english')
	stoppers.extend(["i'm", "i'll", "i've", ""])

	#remove section headers and extra newline characters
	all_words = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
	# all_words = all_words.translate(str.maketrans('', '', punctuation))
	all_words = os.linesep.join([s for s in all_words.splitlines() if s])
	all_words = all_words.replace('\r\n', ' ').split(' ')

	#removing stopwords
	all_words = [x.lower() for x in all_words if x.lower() not in stoppers]

	#removing remaning punctuation
	clean_words = [''.join(c for c in s if c not in punctuation) for s in all_words]

	#one more sweep to ensure we've caught all stopwords
	clean_words = [x.lower() for x in clean_words if x.lower() not in stoppers]

	return song_id, clean_words

def get_song_stats(files):
	all_data = []

	for file in files:
		song_info = {}

		song_id, c_lyrics = clean_lyrics(file)

		#skipping over the song if there is nothing left in the file after cleaning
		if len(c_lyrics) == 0:
			continue

		song_info['song_id'] = int(song_id)
		song_info['unique_words'] = len(np.unique(c_lyrics))
		song_info['total_words'] = len(c_lyrics)
		song_info['clean_lyrics'] = c_lyrics
		song_info['lexical_diversity'] = song_info['unique_words']/song_info['total_words']
		all_data.append(song_info)

	return all_data

