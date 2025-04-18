import time
import requests
import csv
import os
from datetime import datetime

def init():
    if not os.path.exists('./articleData.csv'):
        with open('./articleData.csv','w',encoding='utf-8',newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([
                'id',
                'likeNum',
                'commentsLen',
                'reposts_count',
                'region',
                'content',
                'contentLen',
                'created_at',
                'type',
                'detailUrl',# followBtnCode>uid + mblogid
                'authorAvatar',
                'authorName',
                'authorDetail',
                'isVip' # v_plus
            ])

def writerRow(row):
    with open('./articleData.csv', 'a', encoding='utf-8', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)

def get_data(url,params):
    headers = {
        'Cookie':'PC_TOKEN=e8f2bdaeb7; WBStorage=4d96c54e|undefined; SINAGLOBAL=8707205607029.68.1693375563555; ULV=1693375563566:1:1:1:8707205607029.68.1693375563555:; wb_view_log=1920*10801; XSRF-TOKEN=v6MbU3TtyRErw4dTkmJD7pWD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5V8K5qGyCrwGNY_OGZyV-n5JpX5KMhUgL.FoMEe0n0ehB0S0n2dJLoIERLxK.L1KnLB.qLxK-L1K2LBKnLxKBLBonL12BLxK-L1K5L1heLxK.LBo2LB.Sk; ALF=1695967692; SSOLoginState=1693375692; SCF=AsgHzaOR1bpjw8Hrr2jBXHXlx-poji6oDUSYps9xJdaN3iqbtx8OIimXs9wsFdoLEB5C5LA3bMVehzzGW3tSbWk.; SUB=_2A25J6qycDeRhGeFM6FoS8CrPzDSIHXVqgZlUrDV8PUNbmtANLVPzkW9NQMc5ghrEQBWqrYhCTNcAsEDf6E7Qns1z; WBPSESS=Dt2hbAUaXfkVprjyrAZT_CLHJT-RbIb0ACukleLGAmetJ4tIFM0-WB1ziDMLeurvim5uxeNjI41uIdBrdutdhLJFGSOgRK2326Iec4vJJButSBFTrwHoOwuXMerZFH-5vEwbm6svTfVr8QmWSUagI6ZfzGnhsjcgr9hUriG7I9zW0Ji4Dyz8rc4LZM8ILboGbq1qLPd1iEuO5AtE3nRbig==',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()['statuses']
    else:
        return None

def getAllTypeList():
    typeList = []
    with open('./navData.csv','r',encoding='utf-8') as reader:
        readerCsv = csv.reader(reader)
        next(reader)
        for nav in readerCsv:
            typeList.append(nav)
    return typeList

def parse_json(response,type):
    for artice in response:
        id = artice['id']
        likeNum = artice['attitudes_count']
        commentsLen = artice['comments_count']
        reposts_count = artice['reposts_count']
        try:
            region = artice['region_name'].replace('发布于 ', '')
        except:
            region = '无'
        content = artice['text_raw']
        contentLen = artice['textLength']
        created_at = datetime.strptime(artice['created_at'],'%a %b %d %H:%M:%S %z %Y').strftime('%Y-%m-%d')
        type = type
        try:
            detailUrl = 'https://weibo.com/' + str(artice['id']) + '/' + str(artice['mblogid'])
        except:
            detailUrl = '无'
        authorAvatar = artice['user']['avatar_large']
        authorName = artice['user']['screen_name']
        authorDetail = 'https://weibo.com/u/' + str(artice['user']['id'])
        isVip = artice['user']['v_plus']
        writerRow([
            id,
            likeNum,
            commentsLen,
            reposts_count,
            region,
            content,
            contentLen,
            created_at,
            type,
            detailUrl,
            authorAvatar,
            authorName,
            authorDetail,
            isVip
        ])

def start(typeNum=3,pageNum=2):
    articleUrl = 'https://weibo.com/ajax/feed/hottimeline'
    init()
    typeList = getAllTypeList()
    typeNumCount = 0
    for type in typeList:
        if typeNumCount > typeNum:return
        time.sleep(2)
        for page in range(0,pageNum):
            print('正在爬取的类型：%s 中的第%s页文章数据' % (type[0],page + 1))
            time.sleep(1)
            parmas = {
                'group_id':type[1],
                'containerid':type[2],
                'max_id':page,
                'count':10,
                'extparam':'discover|new_feed'
            }
            response = get_data(articleUrl,parmas)
            parse_json(response,type[0])
        typeNumCount += 1

if __name__ == '__main__':
    start()








