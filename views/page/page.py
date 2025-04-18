from flask import Flask,session,render_template,redirect,Blueprint,request
from snownlp import SnowNLP
from utils.getHomePageData import *
from utils.getHotWordPageData import *
from utils.getTableData import *
from utils.getPublicData import getAllHotWords
from utils.getEchartsData import *
pb = Blueprint('page',__name__,url_prefix='/page',template_folder='templates')

@pb.route('/home')
def home():
    username = session.get('username')
    articleLenMax,likeCountMaxAuthorName,cityMax = getHomeTagsData()
    commentsLikeCountTopFore = getHomeCommentsLikeCountTopFore()
    xData,yData = getHomeArticleCreatedAtChart()
    typeChart = getHomeTypeChart()
    createAtChart = getHomeCommentCreatedChart()
    # getUserNameWordCloud()
    return render_template('index.html',
                           username=username,
                           articleLenMax=articleLenMax,
                           likeCountMaxAuthorName=likeCountMaxAuthorName,
                           cityMax=cityMax,
                           commentsLikeCountTopFore=commentsLikeCountTopFore,
                           xData=xData,
                           yData=yData,
                           typeChart=typeChart,
                           createAtChart=createAtChart
                           )

@pb.route('/hotWord')
def hotWord():
    username = session.get('username')
    hotWordList = getAllHotWords()
    defaultHotWord = hotWordList[0][0]
    if request.args.get('hotWord'):defaultHotWord = request.args.get('hotWord')
    hotWordLen = getHotWordLen(defaultHotWord)
    xData,yData = getHotWordPageCreatedAtCharData(defaultHotWord)
    sentences = ''
    value = SnowNLP(defaultHotWord).sentiments
    if value == 0.5:
        sentences = '中性'
    elif value > 0.5:
        sentences = '正面'
    elif value < 0.5:
        sentences = '负面'

    comments = getCommentFilterData(defaultHotWord)
    return render_template('hotWord.html',
                           username=username,
                           hotWordList=hotWordList,
                           defaultHotWord=defaultHotWord,
                           hotWordLen=hotWordLen,
                           sentences=sentences,
                           xData=xData,
                           yData=yData,
                           comments=comments
                           )

@pb.route('/tableData')
def tableData():
    username = session.get('username')
    defaultFlag = False
    if request.args.get('flag'):defaultFlag = True
    tableData = getTableDataList(defaultFlag)
    return render_template('tableData.html',
                           username=username,
                           tableData=tableData,
                           defaultFlag=defaultFlag
                           )

@pb.route('/articleChar')
def articleChar():
    username = session.get('username')
    typeList = getTypeList()
    defaultType = typeList[0]
    if request.args.get('type'): defaultType = request.args.get('type')
    xData,yData = getArticleCharLikeCount(defaultType)
    x1Data,y1Data = getArticleCharCommentsLen(defaultType)
    x2Data,y2Data = getArticleCharRepotsLen(defaultType)
    return render_template('articleChar.html',
                           username=username,
                           typeList=typeList,
                           defaultType=defaultType,
                           xData=xData,
                           yData=yData,
                           x1Data=x1Data,
                           y1Data=y1Data,
                           x2Data=x2Data,
                           y2Data=y2Data
                           )

@pb.route('/ipChar')
def ipChar():
    username = session.get('username')
    articleRegionData = getIPCharByArticleRegion()
    commentRegionData = getIPCharByCommentsRegion()
    return render_template('ipChar.html',
                           username=username,
                           articleRegionData=articleRegionData,
                           commentRegionData=commentRegionData
                           )

@pb.route('/commentChar')
def commentChar():
    username = session.get('username')
    xData,yData = getCommentCharDataOne()
    genderPieData = getCommentCharDataTwo()
    return render_template('commentChar.html',
                           username=username,
                           xData=xData,
                           yData=yData,
                           genderPieData=genderPieData
                           )

@pb.route('/yuqingChar')
def yuqingChar():
    username = session.get('username')
    xData,yData,bieData = getYuQingCharDataOne()
    bieData1,bieData2 = getYuQingCharDataTwo()
    x1Data,y1Data = getYuQingCharDataThree()
    return render_template('yuqingChar.html',
                           username=username,
                           xData=xData,
                           yData=yData,
                           bieData=bieData,
                           bieData1=bieData1,
                           bieData2=bieData2,
                           x1Data=x1Data,
                           y1Data=y1Data
                           )

@pb.route('/articleCloud')
def articleCloud():
    username = session.get('username')
    return render_template('articleContentCloud.html',
                           username=username
                           )
