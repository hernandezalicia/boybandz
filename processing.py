'''
processing song files
'''

def read_file(file):
	f = open(file, 'r', encoding = 'utf-8')
	lines = f.readlines()
	f.close()
	return lines

def clean_lyrics(file):
	song_id = file.split('/')[-1].split('.txt')[0]
	lines = read_file(file)

	lyrics = ''

	for line in lines:
	    lyrics += line

	stoppers = stopwords.words('english')
	stoppers.extend(["i'm", "i'll"])

	#remove section headers and extra newline characters
	all_words = re.sub(r'[\(\[].*?[\)\]]', '', lyrics)
	# all_words = all_words.translate(str.maketrans('', '', punctuation))
	all_words = os.linesep.join([s for s in all_words.splitlines() if s])
	all_words = all_words.replace('\r\n', ' ').split(' ')

	#removing stopwords
	all_words = [x.lower() for x in all_words if x.lower() not in stoppers]

	#removing remaning punctuation
	clean_words = [''.join(c for c in s if c not in punctuation) for s in all_words]

    return song_id, clean_words

def get_songs_stats(files):
	song_data = {}

	for file in files:
		song_info = {}

		song_id, c_lyrics = clean_lyrics(file)
		song_info['song_id'] = int(song_id)
		song_info['unique_words'] = len(np.unique(c_lyrics))
		song_info['total_words'] = len(c_lyrics)

	return song_data

