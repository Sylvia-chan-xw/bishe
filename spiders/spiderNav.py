import requests
import csv
import numpy as np
import os

def init():
    if not os.path.exists('./navData.csv'):
        with open('./navData.csv','w',encoding='utf-8',newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow([
                'typeName',
                'gid',
                'containerid'
            ])

def writerRow(row):
    with open('./navData.csv', 'a', encoding='utf-8', newline='') as csvFile:
        writer = csv.writer(csvFile)
        writer.writerow(row)

def get_data(url):
    headers = {
        'Cookie':'PC_TOKEN=e8f2bdaeb7; WBStorage=4d96c54e|undefined; SINAGLOBAL=8707205607029.68.1693375563555; ULV=1693375563566:1:1:1:8707205607029.68.1693375563555:; wb_view_log=1920*10801; XSRF-TOKEN=v6MbU3TtyRErw4dTkmJD7pWD; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5V8K5qGyCrwGNY_OGZyV-n5JpX5KMhUgL.FoMEe0n0ehB0S0n2dJLoIERLxK.L1KnLB.qLxK-L1K2LBKnLxKBLBonL12BLxK-L1K5L1heLxK.LBo2LB.Sk; ALF=1695967692; SSOLoginState=1693375692; SCF=AsgHzaOR1bpjw8Hrr2jBXHXlx-poji6oDUSYps9xJdaN3iqbtx8OIimXs9wsFdoLEB5C5LA3bMVehzzGW3tSbWk.; SUB=_2A25J6qycDeRhGeFM6FoS8CrPzDSIHXVqgZlUrDV8PUNbmtANLVPzkW9NQMc5ghrEQBWqrYhCTNcAsEDf6E7Qns1z; WBPSESS=Dt2hbAUaXfkVprjyrAZT_CLHJT-RbIb0ACukleLGAmetJ4tIFM0-WB1ziDMLeurvim5uxeNjI41uIdBrdutdhLJFGSOgRK2326Iec4vJJButSBFTrwHoOwuXMerZFH-5vEwbm6svTfVr8QmWSUagI6ZfzGnhsjcgr9hUriG7I9zW0Ji4Dyz8rc4LZM8ILboGbq1qLPd1iEuO5AtE3nRbig==',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
    }
    params = {
        'is_new_segment':1,
        'fetch_hot':1
    }
    response = requests.get(url,headers=headers,params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def parse_json(response):
    navList = np.append(response['groups'][3]['group'],response['groups'][4]['group'])
    for nav in navList:
        navName = nav['title']
        gid = nav['gid']
        containerid = nav['containerid']
        writerRow([
            navName,
            gid,
            containerid
        ])


if __name__ == '__main__':
    init()
    url = 'https://weibo.com/ajax/feed/allGroups'
    response = get_data(url)
    parse_json(response)