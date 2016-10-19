# -*- coding: utf-8 -*-
import re  # 模块re：包含正则表达式的所有方法
from cal_score import sentimentScore #模块cal_score:提供计算分数的函数方法
from cal_score import sentimentScoreStar
import os  # 模块os：提供了一个统一的操作系统接口函数
import codecs  # 模块codecs：编码转换

# 将filepath文件中的内容，分成行，并去掉其中空行后，加到data
def get_data(filepath):
    fileHandler = open(filepath)  # 对象fileHanlder：打开文件filepath，读取到fileHandler
    data = fileHandler.read()  # data：一次读取fileHandler全部内容到data
    if data[:3] == codecs.BOM_UTF8:  # 某些软件，如notepad，在保存一个以UTF-8编码的文件时，会在文件开始的地方插入三个不可见的字符（0xEF 0xBB 0xBF，即BOM)，若有，去除这三个字符
        data = data[3:]
    if data[-1] == '\n':
        # 除去最后一个换行符#
        data = data[:-1]
    print data
    _data = data.decode('utf-8').split('\n')  # 列表_data:将data用utf-8编码后按行分割，存储到_data
    data = []  # data：赋为空
    for word in _data:  # 将_data中的空行去掉，然后赋给data(此处只能去掉空行，而不能去掉有几个空格组成的行)
        if word != u'':
            # 添加元素#
            data.append(word)
    return data  # 返回data


classification = []  # classfication:对应评分项，顺序自己定
classification2 = [] # classfication2:对应关键词，顺序自己定
classification3 = [] # classfication3:对应关键词，顺序系统定
indexMV = 0
indexDaoYan = 1
indexLuHan = 2
indexJingBoRan = 3
indexMaSiChun = 4
indexTeXiao = 5
indexJuBen = 6
indexSheYing = 7
indexYinYue = 8                 

kw_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       'keywords')  # 获取当前脚本文件路径并在其后加上\keywords
# os.listdir 获得当前目录中的内容#
for kw_file in os.listdir(kw_path):  # 获取kw_path目录下所有文件，并将每个文件变成列表data模式，然后再添加到列表classfication
    classification3.append(get_data(os.path.join(kw_path, kw_file)))

for category in classification3:
    if category[0] == u'演技':
        classification2.append(category)
        classification.append([u'演技评分'])
        break

for category in classification3:
    if category[0] == u'台词':
        classification2.append(category)
        classification.append([u'台词评分'])
        break

for category in classification3:
    if category[0] == u'马思纯':
        classification2.append(category)
        classification.append([u'马思纯评分'])
        break

for category in classification3:
    if category[0] == u'服装':
        classification2.append(category)
        classification.append([u'服装评分'])
        break

    
'''    
for category in classification3:
    if category[0] == u'演技':
        classification2.append(category)
        classification.append([u'演技评分'])      
        break

for category in classification3:
    if category[0] == u'服装':
        classification2.append(category)
        classification.append([u'服装评分'])
        break

for category in classification3:
    if category[0] == u'马思纯':
        classification2.append(category)
        classification.append([u'马思纯评分'])      
        break
        
for category in classification3:
    if category[0] == u'台词':
        classification2.append(category)
        classification.append([u'台词评分'])      
        break
        
for category in classification3:
    if category[0] == u'颜':
        classification2.append(category)
        classification.append([u'颜评分'])      
        break

for category in classification3:
    if category[0] == u'摄影':
        classification2.append(category)
        classification.append([u'摄影评分'])      
        break
        
for category in classification3:
    if category[0] == u'特效':
        classification2.append(category)
        classification.append([u'特效评分'])      
        break

for category in classification3:
    if category[0] == u'南派三叔':
        classification2.append(category)
        classification.append([u'南派三叔评分'])      
        break

for category in classification3:
    if category[0] == u'导演':
        classification2.append(category)
        classification.append([u'导演评分'])      
        break
'''        


classification.append([u'总评', u''])  # classfication里添加总评和空字符


path = os.path.dirname(os.path.abspath(__file__))

posMVdict = get_data(path + '/sentiment dictionary/positive and negative dictionary/positive star.txt')  # 肯定极性
negMVdict = get_data(path + '/sentiment dictionary/positive and negative dictionary/negative star.txt')  # 否定极性
posdaoyandict = get_data(path + '/sentiment dictionary/positive and negative dictionary/positive star.txt')  # 肯定极性
negdaoyandict = get_data(path + '/sentiment dictionary/positive and negative dictionary/negative star.txt')  # 否定极性
posstardict = get_data(path + '/sentiment dictionary/positive and negative dictionary/positive star.txt')  # 肯定极性
negstardict = get_data(path + '/sentiment dictionary/positive and negative dictionary/negative star.txt')  # 否定极性



disstatusdict=get_data(path + '/sentiment dictionary/disturb dictionary/disturb status.txt')
diskeydict=get_data(path + '/sentiment dictionary/disturb dictionary/disturb keyword.txt')


classification2.append(diskeydict)

# 类Comment：评价类
class Comment:
    def __init__(self, contents):  #contents:评价内容
        self.contents = contents
        self.score = []  #score：评分
        self.average_score = []  #average_score:平均分
        for category in classification:  #对于keywords里的每个文本变成的data列表给予相应的评分，还有总分也有一个评分
            self.score.append([])
        self.score[-1].append(5)


    def calScore(self):
        line_break = re.compile(u'[\r\n]')  #行分隔是回车\r换行\n符
        delimiter = re.compile(u'[。？！；.?!;~～]')  #符号是。？！；.?!;~～
        sentences = []
        for line in line_break.split(self.contents):  #根据\r\n分段
            #除去前后空格#
            line = line.strip()
            if not line:  #空行，continue
                continue
            for sent in delimiter.split(line):  #根据符号，分句
                sent = sent.strip()  #除去首尾空格
                if not sent:  #空句，continue
                    continue
                sentences.append(sent)  #列表sentences：感受，加入元素是按符号。？！；.?!;~～分割的句子。即长句组成的列表

        for sentence in sentences:  #对于评价内容sentences里的每条长句sentence
            sent_break = re.compile(u'[,， ]')  #sent_break是,，和空格
            preorder = [-1]
            sent = u''  #sent为空
            sentDel=u''
            for sent_d in sent_break.split(sentence):  #根据sent_break将sentence分成短句sent_d
                #print sent_d #test
                #sent_break = sent_d.strip()
                sent_d = sent_d.strip()  #sent_d除去首尾空格
                if not sent_d:  #空短句，continue
                    continue
                order = []
                i = 0
                for category in classification2:  #classfication不带最后的空
                    if category[0] == u'关键字干扰词':
                        for word in category:  #对于文本里的每个关键词word
                            if sent_d.find(word) != -1:  #如果短句里能找到word
                                #print(word+str(i))                #test
                                order.append(100)  #order序列添加i
                                break  #跳出循环
                    
                    else:
                        for word in category:  #对于文本里的每个关键词word
                            if sent_d.find(word) != -1:  #如果短句里能找到word
                                print(word+str(i))                #test
                                order.append(i)  #order序列添加i
                                break  #跳出循环
                    i = i + 1  #每取classification里内容一次，i+1，即i是指示当前所取的classfication的第几个元素
                #print sent_d,order,'!', #test
                if preorder == [
                    -1] or preorder == [] or order == [] or preorder == order:  # or [x for x in preorder if x in order] !=[]: ？？代表意思不一样吧？？
                    sent = sent + u'，' + sent_d  #sent的内容就要加上，短句
                    if preorder == [-1] or preorder == []:
                        preorder = order[:]  #order赋给preorder
                else:
                    # method of dictionary
                    for i in preorder:
                        
                        if i == indexMV:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posMVdict + negMVdict:
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexDaoYan:
                            #print ("llllll"+str(i))
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posdaoyandict + negdaoyandict:
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexLuHan:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posstardict + negstardict:
                                ###  positive convenient.txt  negative convenient.txt  positive amount.txt  negative amount.txt
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexJingBoRan:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posstardict + negstardict:
                                ###  positive convenient.txt  negative convenient.txt  positive amount.txt  negative amount.txt
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexMaSiChun:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posstardict + negstardict:
                                ###  positive convenient.txt  negative convenient.txt  positive amount.txt  negative amount.txt
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexTeXiao:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posstardict + negstardict:
                                ###  positive convenient.txt  negative convenient.txt  positive amount.txt  negative amount.txt
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexJuBen:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posstardict + negstardict:
                                ###  positive convenient.txt  negative convenient.txt  positive amount.txt  negative amount.txt
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexSheYing:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posstardict + negstardict:
                                ###  positive convenient.txt  negative convenient.txt  positive amount.txt  negative amount.txt
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexYinYue:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posstardict + negstardict:
                                ###  positive convenient.txt  negative convenient.txt  positive amount.txt  negative amount.txt
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                    preorder = order[:]
                    sent = sent_d


                for i in preorder:
                        if i == indexMV:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posMVdict + negMVdict:
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexDaoYan:
                            #print ("llllll"+str(i))
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posdaoyandict + negdaoyandict:
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexLuHan:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posstardict + negstardict:
                                ###  positive convenient.txt  negative convenient.txt  positive amount.txt  negative amount.txt
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexJingBoRan:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posstardict + negstardict:
                                ###  positive convenient.txt  negative convenient.txt  positive amount.txt  negative amount.txt
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexMaSiChun:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posstardict + negstardict:
                                ###  positive convenient.txt  negative convenient.txt  positive amount.txt  negative amount.txt
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexTeXiao:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posstardict + negstardict:
                                ###  positive convenient.txt  negative convenient.txt  positive amount.txt  negative amount.txt
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexJuBen:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posstardict + negstardict:
                                ###  positive convenient.txt  negative convenient.txt  positive amount.txt  negative amount.txt
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexSheYing:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posstardict + negstardict:
                                ###  positive convenient.txt  negative convenient.txt  positive amount.txt  negative amount.txt
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                        elif i == indexYinYue:
                            for sent_disturb in disstatusdict:
                                sentDel=sent.replace(sent_disturb,u'')
                            for sentiment_word in posstardict + negstardict:
                                ###  positive convenient.txt  negative convenient.txt  positive amount.txt  negative amount.txt
                                if sentDel.find(sentiment_word) != -1:
                                    sent=sent.replace(sentiment_word,sentiment_word+u'，')
                                    s=sentimentScoreStar(sent)
                                    self.score[i].append(s)
                                    self.score[-1].append(s)
                                    break
                     


    def printScore(self):
        # print self.score  #test
        i = 0
        p = 0
        for i in range(len(classification)):
            if len(self.score[i]):
                p = 1
                self.average_score.append(round(sum(self.score[i]) / len(self.score[i]), 1))
                print classification[i][0] ,str(i),':', round(sum(self.score[i]) / len(self.score[i]), 1)
            else:
                self.average_score.append(-1)
                #print u'整体',round(sentimentScore(self.contents), 1)       #加入整体分数
                #self.average_score.append(round(sentimentScore(self.contents), 1))
