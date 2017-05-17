import numpy as np
import matplotlib.pyplot as plt


def plotter(artist_name, views, like_ratio, repeat_ratio, songs_list):
	# Views are form youtube; like_ratio = (likes-dislikes)/likes; repear_ratio = count_played/listeners
	n_groups = len(like_ratio)
	# fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.2
	opacity = 0.4
	rects1 = plt.bar(index, views, bar_width,
					alpha=opacity,
					color='b',
					label='Views')
	rects2 = plt.bar(index + bar_width, like_ratio, bar_width,
					 alpha=opacity,
					 color='r',
					 label='Like Ratio')
	rects1 = plt.bar(index+ 2 *bar_width, repeat_ratio, bar_width,
					alpha=opacity,
					color='g',
					label='Repeat Ratio')
	plt.xlabel('Tracks')
	plt.ylabel('Scores')
	plt.xticks(index + bar_width, tuple(songs_list), rotation='vertical')
	plt.legend(loc=2,prop={'size':10})
	plt.savefig('figures/'+str(artist_name)+'.png',bbox_inches='tight')
	plt.show()


def popularity_graph(dic):
	for artist in dic:
		views = []
		like_ratio = []
		repeat_ratio = []
		tracks_list = []
		for each_song in dic[artist]:
			views.append(float(each_song['views'])/10000000)
			like_ratio.append((float(each_song['likes'])-float(each_song['dislikes']))/float(each_song['likes']))
			repeat_ratio.append(float(each_song['playcount'])/float(each_song['listeners']))
			tracks_list.append(each_song['name'])
		plotter(artist, tuple(views), tuple(like_ratio), tuple(repeat_ratio), tuple(tracks_list))
	return views,like_ratio,repeat_ratio


def plote(senti):
	# Views are from youtube; like_ratio = (likes-dislikes)/likes; repear_ratio = count_played/listeners
	n_groups = len(senti)
	fig, ax = plt.subplots()
	index = np.arange(n_groups)
	bar_width = 0.2
	opacity = 0.4
	# rects1 = plt.bar(index, views, bar_width,
	# 				alpha=opacity,
	# 				color='b',
	# 				label='Views')

	plt.plot(index,np.array(senti))
	plt.xlabel('commments')
	plt.ylabel('Scores')
	# plt.savefig('figures/'+str(artist_name)+'.png',bbox_inches='tight')

	#plt.xticks(index + bar_width, tuple(songs_list), rotation='vertical')
	# plt.legend(loc=2,prop={'size':10})
	# plt.savefig('figures/songs'+str(artist_name)+'.png',bbox_inches='tight')
	plt.show()