#import grequests
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import threading
from queue import Queue
import time

SEARCH_QUERY = "healthy living"
data = pd.read_csv('D:\Scrapping programs\healthy+living_urls.csv')
data = np.array(data)

urls = data[:,1]

dataset=[]
lock = threading.Lock()
q = Queue()

def myJob(url):
		
	datapoint_dict = {}
	single_soup = BeautifulSoup(requests.get(url, timeout=5).content,'html.parser')
	#print("Object created")
	# NO_OF_COMMENTS = single_soup.find(id="watch-discussion")
	# print(NO_OF_COMMENTS)
	YOUTUBE_CATEGORY = single_soup.find(class_="content watch-info-tag-list").findChildren("a")[0].text
	channel_tag = single_soup.find(class_="yt-user-info").findChildren("a")[0]
	PUBLISH_DATE = single_soup.find(class_="watch-time-text").text
	DESCRIPTION = single_soup.find(id="eow-description").text
	VIDEO_TITLE = single_soup.find("span", class_="watch-title").text.strip()
	VIDEO_VIEWS = single_soup.find("div", class_="watch-view-count").text
	try:
		LIKES = single_soup.find('button', {"title": "I like this"}).findChildren("span")[0].text
	except:
		LIKES = "0"
	try:	
		DISLIKES = single_soup.find('button', {"title": "I dislike this"}).findChildren("span")[0].text
	except:
		DISLIKES = "0"
	CHANNEL_NAME = channel_tag.text.strip()
	datapoint_dict['channel_name'] = CHANNEL_NAME
	#datapoint_dict['total_subscribers'] = SUBCRIBER_COUNT
	datapoint_dict['video_url'] = url
	datapoint_dict['video_title'] = VIDEO_TITLE
	datapoint_dict['video_views'] = VIDEO_VIEWS
	datapoint_dict['likes'] = LIKES
	datapoint_dict['dislikes'] = DISLIKES
	datapoint_dict['description'] = DESCRIPTION
	datapoint_dict['published_date'] = PUBLISH_DATE
	datapoint_dict['youtube_category'] = YOUTUBE_CATEGORY
	with lock:
		dataset.append(datapoint_dict)
		print(f"Video URL :- {url}")
		print(f"Channel name: {CHANNEL_NAME}")
		#print(f"Subscriber count: {SUBCRIBER_COUNT}")
		print(f"Video Title: {VIDEO_TITLE}")
		print(f"No of views= {VIDEO_VIEWS}")
		print(f"Likes: {LIKES}")
		print(f"Dislikes: {DISLIKES}")
		print(f"Description: {DESCRIPTION}")
		print(f"Published on: {PUBLISH_DATE}")
		print(f"Youtube category: {YOUTUBE_CATEGORY}")
		print(len(dataset))
		print("--------------------------------------------------------")

		
def threader():
	while True:
		url = q.get()
		myJob(url)
		q.task_done()

for x in range(10): 
	t = threading.Thread(target = threader)
	t.daemon = True
	t.start()

for url in urls:
	q.put(url)

q.join()
print(len(dataset))
data = pd.DataFrame(dataset)
data.to_csv(f'{SEARCH_QUERY}_dataset.csv')