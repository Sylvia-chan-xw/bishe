import time
import requests
import csv
import os
from datetime import datetime

def init():
    if not os.path.exists('./articleComments.csv'):
        with open('./articleComments.csv','w',encoding='utf-8',newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([
                'articleId',
                'created_at',
                'likes_counts',
                'region',
                'content',
                'authorName',
                'authorGender',
                'authorAddress',
                'authorAvatar'
            ])

def writerRow(row):
    with open('./articleComments.csv', 'a', encoding='utf-8', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)

def get_data(url,params):
    headers = {
        'Cookie':'PC_TOKEN=e8f2bdaeb7; WBStorage=4d96c54e|undefined; SINAGLOBAL=8707205607029.68.1693375563555; ULV=1693375563566:1:1:1:8707205607029.68.1693375563555:; wb_view_log=1920*10801; XSRF-TOKEN=v6MbU3TtyRErw4dTkmJD7pWD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5V8K5qGyCrwGNY_OGZyV-n5JpX5KMhUgL.FoMEe0n0ehB0S0n2dJLoIERLxK.L1KnLB.qLxK-L1K2LBKnLxKBLBonL12BLxK-L1K5L1heLxK.LBo2LB.Sk; ALF=1695967692; SSOLoginState=1693375692; SCF=AsgHzaOR1bpjw8Hrr2jBXHXlx-poji6oDUSYps9xJdaN3iqbtx8OIimXs9wsFdoLEB5C5LA3bMVehzzGW3tSbWk.; SUB=_2A25J6qycDeRhGeFM6FoS8CrPzDSIHXVqgZlUrDV8PUNbmtANLVPzkW9NQMc5ghrEQBWqrYhCTNcAsEDf6E7Qns1z; WBPSESS=Dt2hbAUaXfkVprjyrAZT_CLHJT-RbIb0ACukleLGAmetJ4tIFM0-WB1ziDMLeurvim5uxeNjI41uIdBrdutdhLJFGSOgRK2326Iec4vJJButSBFTrwHoOwuXMerZFH-5vEwbm6svTfVr8QmWSUagI6ZfzGnhsjcgr9hUriG7I9zW0Ji4Dyz8rc4LZM8ILboGbq1qLPd1iEuO5AtE3nRbig==',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()['data']
    else:
        return None

def getAllArticleList():
    artileList = []
    with open('./articleData.csv','r',encoding='utf-8') as reader:
        readerCsv = csv.reader(reader)
        next(reader)
        for nav in readerCsv:
            artileList.append(nav)
    return artileList

def parse_json(response,artileId):
    for comment in response:
        created_at = datetime.strptime(comment['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
        likes_counts = comment['like_counts']
        try:
            region = comment['source'].replace('来自', '')
        except:
            region = '无'
        content = comment['text_raw']
        authorName = comment['user']['screen_name']
        authorGender = comment['user']['gender']
        authorAddress = comment['user']['location']
        authorAvatar = comment['user']['avatar_large']
        writerRow([
            artileId,
            created_at,
            likes_counts,
            region,
            content,
            authorName,
            authorGender,
            authorAddress,
            authorAvatar
        ])

def start():
    commentUrl = 'https://weibo.com/ajax/statuses/buildComments'
    init()
    articleList = getAllArticleList()
    for article in articleList:
        articleId = article[0]
        print('正在爬取id值为%s的文章评论' % articleId)
        time.sleep(2)
        params = {
            'id':int(articleId),
            'is_show_bulletin':2
        }
        response = get_data(commentUrl,params)
        parse_json(response,articleId)



if __name__ == '__main__':
    start()








