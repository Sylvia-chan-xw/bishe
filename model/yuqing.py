from snownlp import SnowNLP
import csv
import os
from utils.getPublicData import getAllCommentsData

def targetFile():
    targetFile = 'target.csv'
    commentsList = getAllCommentsData()

    rateData = []
    good = 0
    bad = 0
    middle = 0

    for index,i in enumerate(commentsList):
        value = SnowNLP(i[4]).sentiments
        if value > 0.5:
            good+=1
            rateData.append([i[4],'正面'])
        elif value == 0.5:
            middle+=1
            rateData.append([i[4],'中性'])
        elif value < 0.5:
            bad+=1
            rateData.append([i[4],'负面'])

    for i in rateData:
        with open(targetFile,'a+',encoding='utf8',newline='') as f:
            writer = csv.writer(f)
            writer.writerow(i)

def main():
    targetFile()

if __name__ == '__main__':
    main()