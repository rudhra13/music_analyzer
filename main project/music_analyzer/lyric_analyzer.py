import json
import urllib2
def hit_api_lyrics(artist_name,song):
	artist_name = artist_name.replace(' ','%20')
	song = song.replace(' ','%20')
	url = 'http://lyric-api.herokuapp.com/api/find/'+artist_name+'/'+song
	data = json.load(urllib2.urlopen(url))
	print '--------******-------'
	return data['lyric']