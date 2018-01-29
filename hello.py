import requests
import dateutil.parser
from datetime import datetime
import pandas as pd
import sys


if(len(sys.argv) != 4):
    print("Enter twitch video id, client id, and bucket/interval in seconds")

#convert string to datetime object
def parse_timestamp(value: str) -> datetime:
    return dateutil.parser.parse(value)
#return commment data
def GetTimeStamps(videoid: str, params, headers: dict):
    url='https://api.twitch.tv/v5/videos/{}/comments'.format(videoid)
    r = requests.get(url, params=params,headers=headers)
    return r
#calling GetTimeStamps
def CommentFragment(videoid: str, cursor: str, headers: dict):
    return GetTimeStamps(videoid, {'cursor': cursor}, headers=headers).json()

#parses through twitch api cursors next chunk of data until no more
#pull start time of VOD before grabbing comments and subtracting original time
#comment_creation - VOD start time to get time from start
def GetChat(videoid: str,clientid: str):
    #print(len(comments))
    #client ID required in header
    headers = {'Client-ID':clientid}
    vid_url='https://api.twitch.tv/v5/videos/{}'.format(videoid)
    vid_r=requests.get(vid_url, headers = headers)
    initialTime = parse_timestamp(vid_r.json()['created_at'])
    fragment: dict = {'_next': ''}
    while '_next' in fragment:
        fragment = CommentFragment(videoid, fragment['_next'], headers)
        for comment in fragment['comments']:
            yield parse_timestamp(comment['created_at'])-initialTime
#credit to Petter Kraabol as I used pieces of his twitch code to pull
#comments from twitch api
##iterate value seconds
#Goal here is to create time buckets/intervals of user's choice
#the purpose is to check if there is correlation between volume of comments in a time period to "plays"
def CountValues(videoid: str, clientid: str, iteratInterval: int):
    test = GetChat(videoid, clientid)
    iterateValue = int(iteratInterval)
    value=[iterateValue]
    count=[0]
    countIter=0
    videoTime=['0h:0m:0s']
    for x in test:
        if x.seconds < value[countIter]:
            count[countIter]+=1
        else:
            countIter+=1
            value.append(iterateValue*(countIter+1))
            count.append(1)
            m, s = divmod(value[countIter], 60)
            h, m = divmod(m, 60)
            videoTime.append('{}h:{}m:{}s'.format(h,m,s))

    return count,value, videoTime

countz, valuez,videoTime = CountValues(str(sys.argv[1]),str(sys.argv[2]), sys.argv[3])

testDF = pd.DataFrame(
    {'count': countz,
     'valueSeconds': valuez,
     'StringTime': videoTime
    })

print('Saving csv file to ~/Downloads/vod{}chatdata.csv...')
testDF.to_csv('~/Downloads/vod{}chatdata.csv'.format(sys.argv[1]), sep=',')
