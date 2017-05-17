from nltk.sentiment.vader import SentimentIntensityAnalyzer
import numpy as np
def sentiment_analyzer(sentences):
	sid = SentimentIntensityAnalyzer()
	# print sid
	scores_list_com = []
	if sentences == []:
		return [0,0]
	else:
		for i, sentence in enumerate(sentences):
			#print sentence
			ss = sid.polarity_scores(sentence)
			#print ss
			scores_list_com.append(float(ss['compound']))
	 	print "----****----" 
		return np.array(scores_list_com)
		# "\n\n\nTotal sentiment-->",np.mean(np.array(scores_list_com)) 