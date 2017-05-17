import urllib
from bs4 import BeautifulSoup
import re, json, requests
import urllib2, httplib2, os, sys
import numpy as np
from comment_downloader import main_function
from nltk.sentiment.vader import SentimentIntensityAnalyzer
#from pymongo import MongoClient
from matplotlib import pyplot as plt
from bar_graph_creator import plotter, popularity_graph, plote
from comment_sentiment import sentiment_analyzer
# from lyric_analyzer import hit_api_lyrics

# add = 'localhost'
# port = 27017
# objectMongo = MongoClient(add,port)quer
# db_name = "Artist_Details"
# db = objectMongo[db_name]

# def _tags_collector(page_source):
# 	tags = []
# 	for tag in re.findall(r'href="/tag/(.*?)"',page_source,re.IGNORECASE):
# 		tags.append(tag.replace('+',' '))
# 	return tags

# def _details_query(page_source):
# 	for each in re.findall(r'<title .+>(.*?)</title>',page_source, re.IGNORECASE):
# 		word = each.decode('ascii','ignore').encode('utf-8')
# 		toQuery = re.findall(r'(.*?) Listen.*',word,re.IGNORECASE)[0]
# 	return toQuery 



# def _scrap_lyrics(artist_name,song):

#  	artist_name = artist_name.replace(' ','')
#  	song = song.replace(' ','')
#  	url = "http://www.azlyrics.com/lyrics/"+artist_name.lower()+'/'+ song.lower()+ ".html"
#  	response = urllib2.urlopen(url)
#  	page_source = response.read()
# # 	print page_source
# # 	lyrics = re.findall(r'Sorry about that. -->(.*?)<!-- MxM banner -->',page_source,re.IGNORECASE)
# 	lyrics=re.findall(r'prohibited by our licensing by our licensing agreement/. Sorry about that/. -->(.*?)</div>',page_source,re.IGNORECASE)
# 	return lyrics

# def _track_search(input_artist, api_key):
# 	url = "http://ws.audioscrobbler.com/2.0/?method=track.search&track="+input_artist+"&api_key="+api_key+"&format=json"
# 	outjson = requests.get(url).json()
# 	# top_artists = list(set([each['artist'] for each in outjson['results']['trackmatches']['track']]))
# 	toptracks = artist_top_tracks(input_artist, api_key)
# 	return toptracks



# def get_top_artist_tag(api_key,tag):
# 	url='http://ws.audioscrobbler.com/2.0/?method=tag.gettopartists&tag='+tag+'&api_key='+api_key+'&format=json'
# 	response=requests.get(url).json()
# 	return [dic['name'] for i,dic in enumerate(response['topartists']['artist']) if i < 1]

# def get_all_songs_from_tags(tags):
# 	all_songs_for_each_tag = {}
# 	for each_tag in tags:
# 		top_artists = get_top_artist_tag(api_key,each_tag)
# 		top_tracks = artist_top_tracks(top_artists, api_key)
# 		all_songs_for_each_tag[each_tag] = top_tracks
# 	return all_songs_for_each_tag

# def reformat_dict(dic):
# 	for each_tag in dic:
# 		for each_artist in dic[each_tag]:
# 			for i, each_dic in enumerate(dic[each_tag][each_artist]):
# 				_id = each_tag+'+'+each_artist+'+'+each_dic['name']
# 				doc = each_dic
# 				doc['_id'] = _id
# 				doc['tag'] = each_tag
# 				doc['artist'] = each_artist
# 				print each_artist
# 				_push_mongo("Formatted Details", doc)

# def _push_mongo(collection_name, doc):
# 	db[collection_name].insert(doc)



# def user_recent_tracks(User_Name,Api_Key):
# 	url= "http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user="+User_Name+"&api_key="+Api_Key+"&format=json"
# 	outjson=requests.get(url).json()
# 	#recent_tracks=list(set([each{'text':'artist[text]', 'name':'name'} for each in outjson['recenttracks']['track']]))
# 	#print recent_tracks
# 	dict = []
# 	for i in outjson['recenttracks']['track']:
# 		# if j<5:
# 		dict.append(({'artist':(i['artist']['#text']).encode('ascii','ignore').decode('utf-8'),
# 			'song':(i['name']).encode('ascii','ignore').decode('utf-8')}))
# 	return dict

# def _user_recent_tracks(user_name,api_key)
# 	url="http://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user="+user_name+"&api_key="+api_key+"&format=json"
# 	outjson=requests.get(url).json()
# 	user_artists=list()


def artist_top_tracks(input_artist, api_key):
	top_tracks_dict = {}
	#for each_artist in artists_list:
	url='http://ws.audioscrobbler.com/2.0/?method=artist.gettoptracks&artist='+input_artist+'&api_key='+api_key+'&format=json'
	response = requests.get(url).json()
	for i,dic in enumerate(response['toptracks']['track']):
		if i < 3:
			print input_artist,dic['name']
			video_id = youtube_id_fetcher(input_artist ,dic['name'])
			(views,likes,dislikes) = youtube_likes_and_dislikes(video_id)
			comments = youtube_comments(video_id)
			sentiment_scores = sentiment_analyzer(comments)
			plote(sentiment_scores)
			sentiment_mean=np.mean(sentiment_scores)

			if input_artist in top_tracks_dict:
				top_tracks_dict[input_artist].append({'name': dic['name'],
												'listeners': dic['listeners'],
												'playcount': dic['playcount'],
												'views': views,
												'likes':likes,
												'dislikes': dislikes})
			else:
				top_tracks_dict[input_artist] = [{'name': dic['name'],
												'listeners': dic['listeners'],
												'playcount': dic['playcount'],
												'views': views,
												'likes':likes,
												'dislikes': dislikes}]
	# print top_tracks_dict
					
	return top_tracks_dict


def youtube_id_fetcher(artist_name,song):
	artist_name = artist_name.replace(' ','+')
	song = song.replace(' ','+')
	query = "https://www.youtube.com/results?search_query="+artist_name+'+'+song
	page_source = get_response(query)
	video_id = return_video_id(page_source)
	return video_id

def get_response(url):
	response = urllib2.urlopen(url)
	page_source = response.read()
	return page_source

def return_video_id(page_source):
	return re.findall(r'data-context-item-id="(.*?)"',page_source,re.IGNORECASE)[0]

def youtube_likes_and_dislikes(video_id):
	url = "https://www.youtube.com/watch?v="+video_id
	response = urllib2.urlopen(url)
	page_source = response.read()
	views = re.findall(r'watch-view-count">(.*?) views' ,page_source,re.IGNORECASE)[0]
	likes = re.findall(r'likes" style="width: (.*?)%',page_source,re.IGNORECASE)[0]
	dislikes = re.findall(r'dislikes" style="width: (.*?)%',page_source,re.IGNORECASE)[0]
	return int(views.replace(',','')),"%.3f" %float(likes),"%.3f" %float(dislikes)

def youtube_comments(video_id):
	return main_function(video_id,50)


if __name__ == '__main__':
	api_key='bf67da43b5a3c4c7f7271620d50c6080'
	artist='linkin park'
	# song='hymn for the missing'
	# tags = ['Blues', 'Hip hop', 'Jazz', 'Pop', 'Rock', 'Metal']
	# overall_dict = get_all_songs_from_tags(tags)
	# reformat_dict(overall_dict)
	


	#1) 
	userinput_artist = artist
	# artist_info = _track_search(userinput_artist, api_key)
	artist_top=artist_top_tracks(userinput_artist,api_key)
	popularity_graph(artist_top)
	
	#2)
	# usr_input_artist=artist
	# usr_input_song=song
	# usr_input_comments_no=50
	# url="http://www.last.fm/music/"+usr_input_artist+"/_/"+usr_input_song#City+Of+Stars
	# #+-+From+%22La+La+Land%22+Soundtrack"
	# page_source = _get_response(url)
	# #print page_source
	# artistNsong = _details_query(page_source)
	# query = "https://www.youtube.com/results?search_query="+'+'.join(artistNsong.split(" "))
	# page_source_youtube = _get_response(query)
	# VIDEO_ID = _return_video_id(page_source_youtube)

	# no_of_comments=usr_input_comments_no
	# comments = main_function(VIDEO_ID,no_of_comments)
	# #print comments
	# senti= _sentiment_analyzer(comments)
	# plote(senti)
	# total_polarity=np.mean(senti)
	# print total_polarity
	## plote(total_polarity)


	
	#3)

	# user_songNartist=user_recent_tracks('rj',api_key)
	# ##print user_songNartist
	# for i in user_songNartist:
	# 	lyrical_sentiment=_hit_api_lyrics(i['artist'],i['song'])
	# 	# print i['artist']
	# 	# print lyrical_sentiment
	# 	print _sentiment_analyzer(lyrical_sentiment)




	#4)
	# lyrical_sentiment=hit_api_lyrics(artist,song)
	# print lyrical_sentiment
	# # #lyrical_sentiment=_scrap_lyrics(artist,song)

	# print lyrical_sentiment
	# print np.mean(_sentiment_analyzer(lyrical_sentiment))