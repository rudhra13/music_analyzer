import os
import sys
import time
import json
import requests
import argparse
import lxml.html 

from lxml.cssselect import CSSSelector

YOUTUBE_COMMENTS_URL = 'https://www.youtube.com/all_comments?v={youtube_id}'
YOUTUBE_COMMENTS_AJAX_URL = 'https://www.youtube.com/comment_ajax'

USER_AGENT = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36'



def find_value(html, key, num_chars=2):
	pos_begin = html.find(key) + len(key) + num_chars
	pos_end = html.find('"', pos_begin)
	return html[pos_begin: pos_end]


def extract_comments(html):
	tree = lxml.html.fromstring(html)
	item_sel = CSSSelector('.comment-item')
	text_sel = CSSSelector('.comment-text-content')
	time_sel = CSSSelector('.time')
	author_sel = CSSSelector('.user-name')
	for item in item_sel(tree):
		yield {'cid': item.get('data-cid'),
			   'text': text_sel(item)[0].text_content(),
			   'time': time_sel(item)[0].text_content().strip(),
			   'author': author_sel(item)[0].text_content()}


def extract_reply_cids(html):
	tree = lxml.html.fromstring(html)
	sel = CSSSelector('.comment-replies-header > .load-comments')
	return [i.get('data-cid') for i in sel(tree)]


def ajax_request(session, url, params, data, retries=10, sleep=20):
	for _ in range(retries):
		response = session.post(url, params=params, data=data)
		if response.status_code == 200:
			response_dict = json.loads(response.text)
			return response_dict.get('page_token', None), response_dict['html_content']
		else:
			time.sleep(sleep)


def download_comments(youtube_id, no_of_comments,sleep=1):
	session = requests.Session()
	session.headers['User-Agent'] = USER_AGENT

	# Get Youtube page with initial comments
	response = session.get(YOUTUBE_COMMENTS_URL.format(youtube_id=youtube_id))
	html = response.text
	reply_cids = extract_reply_cids(html)

	ret_cids = []
	for comment in extract_comments(html):
		ret_cids.append(comment['cid'])
		yield comment

	page_token = find_value(html, 'data-token')
	session_token = find_value(html, 'XSRF_TOKEN', 4)
	first_iteration = True
	count = 0
	iterations = 0
	count_comments=no_of_comments
	# Get remaining comments (the same as pressing the 'Show more' button)
	while page_token and count < count_comments and iterations < 10:
		iterations += 1
		data = {'video_id': youtube_id,
				'session_token': session_token}

		params = {'action_load_comments': 1,
				  'order_by_time': True,
				  'filter': youtube_id}

		if first_iteration:
			params['order_menu'] = True
		else:
			data['page_token'] = page_token

		response = ajax_request(session, YOUTUBE_COMMENTS_AJAX_URL, params, data)
		if not response:
			break

		page_token, html = response

		reply_cids += extract_reply_cids(html)
		for comment in extract_comments(html):
			if comment['cid'] not in ret_cids:
				count += 1
				ret_cids.append(comment['cid'])
				yield comment

		first_iteration = False
		time.sleep(sleep)

def main_function(_id,no_of_comments):
	try:
		youtube_id = _id
		if not youtube_id:
			raise ValueError('you need to specify a Youtube ID and an output filename')
			# return download_comments()
			
		return [every['text'] for every in download_comments(youtube_id,no_of_comments)]
	except Exception as e:
		print 'Error:', str(e)
		sys.exit(1)