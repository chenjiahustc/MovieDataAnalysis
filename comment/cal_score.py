# -*- coding: utf-8 -*-
import wordDivision
import codecs
import os

def get_data(filepath):
    fileHandler = open(filepath)
    data = fileHandler.read()
    if data[:3] == codecs.BOM_UTF8:
        data = data[3:]
    if data[-1] == '\n':
        data = data[:-1]
    _data = data.decode('utf-8').split('\n')
    data = []
    for word in _data:
        if word != u'':
            data.append(word)
    return data

path = os.path.dirname(os.path.abspath(__file__))

# 导入 sentiment dictionary，情感极性词
posdict = get_data(
    path + '/sentiment dictionary/positive and negative dictionary/posdict.txt')  # 肯定极性，如：爱，安，好，帮，多，产量多
negdict = get_data(
    path + '/sentiment dictionary/positive and negative dictionary/negdict.txt')  # 否定极性，如：矮，悲，笨，差，少，少烦我

posMVdict = get_data(path + '/sentiment dictionary/positive and negative dictionary/positive star.txt')  # 肯定极性：客流量少
negMVdict = get_data(path + '/sentiment dictionary/positive and negative dictionary/negative star.txt')  # 否定极性，客流量多
posdaoyandict = get_data(path + '/sentiment dictionary/positive and negative dictionary/positive star.txt')  # 肯定极性，娱乐设施有趣
negprodict = get_data(path + '/sentiment dictionary/positive and negative dictionary/negative star.txt')  # 否定极性，娱乐设施无趣
posstardict = get_data(path + '/sentiment dictionary/positive and negative dictionary/positive star.txt')  # 肯定极性，娱乐设施状况好
negstardict = get_data(path + '/sentiment dictionary/positive and negative dictionary/negative star.txt')  # 否定极性，娱乐设施状况差

disstatusdict=get_data(path + '/sentiment dictionary/disturb dictionary/disturb status.txt')


# 导入 adverbs of degree dictionary,程度副词
mostdict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/most.txt')  # 最高级，如：极，极尽，极端，充分，绝顶，，正面因子2.5，反转因子-0.5
verydict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/very.txt')  # 很高级，如：over，过度，过,很，老，不为过，正面因子2.0，反转因子-0.2
moredict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/more.txt')  # 较高级，如：大不了，更，越加，越，但是，足足，正面因子1.5
ishdict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/ish.txt')  # 次高级：如：一点儿，一些，比较，怪，好生，正面因子0.5
insufficientdict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/insufficiently.txt')  # 略高级：如：半点儿，微，略，不怎么，正面因子0.3
ordinarydict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/ordinary.txt')  # 普通级：只有一个词：一般，正面因子0.2
advicedict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/advice.txt')  # 建议级：有四个：希望，建议，可以，应该，正面因子-0.2
inversedict = get_data(
    path + '/sentiment dictionary/adverbs of degree dictionary/inverse.txt')  # 否定级，如：不，没，无，非，不然，正面因子-1.0

# 导入 dynamic dictionary，一些常要结合语境判断的特殊词
dynamic_sentiment = get_data(
    path + '/sentiment dictionary/dynamic dictionary/dynamic sentiment.txt')  # 结合语境的情感极性词，有：大，小，高，低，多，少，紧，浓，淡
dynamic_inverse = get_data(
    path + '/sentiment dictionary/dynamic dictionary/dynamic inverse.txt')  # 结合特殊极性词后与常规极性相反的词，有：价格，人，油烟，烟尘，商业，票价，和dynamic_sentiment的词相结合时，极性逆转
dynamic_remove = get_data(
    path + '/sentiment dictionary/dynamic dictionary/dynamic remove.txt')  # 结合特殊极性词后无意义的词，有：山，爬山，时间（我觉得这个地方最后的时间应该是爬山时间之类的，而不能仅仅是时间）
dynamic_property = get_data(
    path + '/sentiment dictionary/dynamic dictionary/dynamic property.txt')  # 同时是副词也是极性词的词，如：老，好，没多大，贼，没有等

#计算pos/neg的参数
most_para = 2.5
most_inverse = -0.5
very_para = 2.0
very_inverse = -0.2
more_para = 1.5
ish_para = 0.5
insufficient_para = 0.3

#计算score的参数
average_score = 6.5
max_score = 10.0
min_score = 0.0
root_para = 0.6
multi_para = 1.7
advice_para = - 0.2
inverse_para = - 1.0
ordinary_para = 0.2
neg_reduce = 1

def score_trans(num):  #对(poscount-negcount)进行处理，得到分数
    if num > 0:
        sgn = 1
    else:
        sgn = -1
    score = abs(num) ** root_para * sgn * multi_para + average_score
    if score > max_score:
        score = max_score  #(score - 6)
    if score < min_score:
        score = min_score
    return score

def score_trans2(count):  #通过对(poscount-negcount)进行处理，得到分数
    if count < -3:
        score = 8 / ( abs(count) - 1 )
    elif count < 0:
        score = 7 + count
    elif count < 1:
        score = 7 + count
    elif count < 3:
        score = 7.5 + count * 0.5
    else:
        score = 10 - 1 / ( count - 2 )
    return score

def wordCal(word, sentiment_value, inver_num):  #根据情感词之前的程度副词对pos/neg_temp进行处理
    if word in mostdict:
        if inver_num == 1:
            sentiment_value *= most_inverse
        else:
            sentiment_value *= most_para
    elif word in verydict:
        if inver_num == 1:
            sentiment_value *= very_inverse
        else:
            sentiment_value *= very_para
    elif word in moredict:
        sentiment_value *= more_para
    elif word in ishdict:
        sentiment_value *= ish_para
    elif word in insufficientdict:
        sentiment_value *= insufficient_para
    elif word in inversedict:
        sentiment_value *= inverse_para
        inver_num += 1
    elif word in advicedict:
        sentiment_value *= advice_para
    return sentiment_value, inver_num

def wordMatch_s(words,paraposdict,paranegdict):  #判断words中是否包含程度副词，如果包含则返回该程度副词(此处也可以将posdict和negdict拆分成所有的极性词典)
    for word in disstatusdict:                  #凡干扰词项加在这里
        if words.find(word) != -1 and '' != word:
            return word
    for word in paraposdict:
        if words.find(word) != -1 and '' != word:
            return word
    for word in paranegdict:
        if words.find(word) != -1 and '' != word:
            return word
    return 0
    
def wordMatch_d(words):  #判断words中是否包含极性词或者干扰词，且干扰词优先，如果包含则返回该词
    for word in mostdict:
        if words.find(word) != -1 and '' != word:
            return word
    for word in verydict:
        if words.find(word) != -1 and '' != word:
            return word
    for word in moredict:
        if words.find(word) != -1 and '' != word:
            return word
    for word in ishdict:
        if words.find(word) != -1 and '' != word:
            return word
    for word in insufficientdict:
        if words.find(word) != -1 and '' != word:
            return word
    for word in advicedict:
        if words.find(word) != -1 and '' != word:
            return word
    for word in inversedict: 
        if words.find(word) != -1 and '' != word:
            return word
    return 0
    
def divContent(content,paraposdict,paranegdict):
    seg_content = list(wordDivision.cut(content))
    n = len(seg_content)
    i = 0
    while (i<n):				#执行完这个循环以后，按结巴分词所分的词组成的列表seg_content会变成程度副词，极性词，以及包含程度副词的词再分割的程度副词和前缀后缀组成的列表
        words =  seg_content[i]	#words为分词后的每个词
        if not(words in mostdict or words in verydict or words in moredict or words in ishdict or
               words in insufficientdict or words in inversedict or words in posdict or words in negdict or words in paraposdict or words in paranegdict): #如果words本身就是程度副词或极性词，则跳过，若不在词库中，再继续分析,此处posdict和negdict必须包含所有的极性词（包括干扰词）(此处也可以将posdict和negdict拆分成所有的极性词典)
            if wordMatch_s(words,paraposdict,paranegdict)!= 0:  #判断分词后的每个词是否包含极性词，若包含，往下
                word = wordMatch_s(words,paraposdict,paranegdict)	#返回这个匹配到的极性词
                preword ,postword = words.split(word,1)		#分词后的词再根据这个程度分词分成前后两部分，分别赋给前缀preword和后缀postword
                del seg_content[i]					#从分词后的所有词当中删除这个词
                if preword != '':					#如果前缀不为空
                    seg_content.insert(i, preword)	#用这个前缀代替分词后的那个词，并将标号和长度都加1
                    i += 1
                    n += 1
                seg_content.insert(i, word)			#其后插入程度副词
                i += 1
                if postword != '':					
                    seg_content.insert(i, postword)   	#后缀加到seg_content里面，并把总长度加1
                    n += 1
        i+=1 
    n = len(seg_content)
    i = 0    
    while (i<n):				#执行完这个循环以后，按结巴分词所分的词组成的列表seg_content会变成程度副词，极性词，以及包含程度副词的词再分割的程度副词和前缀后缀组成的列表
        words =  seg_content[i]	#words为分词后的每个词
        if not(words in mostdict or words in verydict or words in moredict or words in ishdict or
               words in insufficientdict or words in inversedict or words in posdict or words in negdict or words in paraposdict or words in paranegdict): #如果words本身就是程度副词或极性词，则跳过，若不在词库中，再继续分析,此处posdict和negdict必须包含所有的极性词（包括干扰词）(此处也可以将posdict和negdict拆分成所有的极性词典)           
            if wordMatch_d(words)!= 0:  #判断分词后的每个词是否包含程度副词，若包含，往下
                word = wordMatch_d(words)	#返回这个匹配到的程度副词
                preword ,postword = words.split(word,1)		#分词后的词再根据这个程度分词分成前后两部分，分别赋给前缀preword和后缀postword
                if postword in posdict or postword in negdict or preword in posdict or preword in negdict: #如果后缀是情感极性词,这里应还该考虑前缀，比如多一些
                    del seg_content[i]					#从分词后的所有词当中删除这个词
                    if preword != '':					#如果前缀不为空
                        seg_content.insert(i, preword)	#用这个前缀代替分词后的那个词，并将标号和长度都加1
                        i += 1
                        n += 1
                    seg_content.insert(i, word)			#其后插入程度副词
                    i += 1
                    if postword != '':					
                        seg_content.insert(i, postword)   	#后缀加到seg_content里面，并把总长度加1
                        n += 1
        i += 1												#循环到下一个
        
    n = len(seg_content)
    i = 0
    while (i<n):				#执行完这个循环以后，按结巴分词所分的词组成的列表seg_content会变成程度副词，极性词，以及包含程度副词的词再分割的程度副词和前缀后缀组成的列表
        words =  seg_content[i]	#words为分词后的每个词
        if not(words in mostdict or words in verydict or words in moredict or words in ishdict or
               words in insufficientdict or words in inversedict or words in posdict or words in negdict or words in paraposdict or words in paranegdict): #如果words本身就是程度副词或极性词，则跳过，若不在词库中，再继续分析

            if wordMatch_d(words)!= 0:  #判断分词后的每个词是否包含程度副词，若包含，往下
                word = wordMatch_d(words)	#返回这个匹配到的程度副词
                preword ,postword = words.split(word,1)		#分词后的词再根据这个程度分词分成前后两部分，分别赋给前缀preword和后缀postword
                if postword in posdict or postword in negdict or preword in posdict or preword in negdict: #如果后缀是情感极性词
                    del seg_content[i]					#从分词后的所有词当中删除这个词
                    if preword != '':					#如果前缀不为空
                        seg_content.insert(i, preword)	#用这个前缀代替分词后的那个词，并将标号和长度都加1
                        i += 1
                        n += 1
                    seg_content.insert(i, word)			#其后插入程度副词
                    i += 1
                    if postword != '':					
                        seg_content.insert(i, postword)   	#后缀加到seg_content里面，并把总长度加1
                        n += 1
        i += 1												#循环到下一个
        
    n = len(seg_content)
    i = 0
    while (i<n-1):				
        words =  seg_content[i]
        words_next = seg_content[i+1]
        if (words in paraposdict or words in paranegdict)and(words_next!= u'，'):
            seg_content.insert(i+1, u'，')
            i+=1
            n+=1
        i+=1
            
    
    print '/'.join(seg_content)  #test
     
    return seg_content

def sentimentScore(content):  #计算content的整体情感分数
    i = 0  # word position counter
    a = 0  # sentiment word position
    poscount = 0  # count a positive word
    negcount = 0  # count a negative word


    seg_content=divContent(content,posdict,negdict)
    for word in seg_content:
        '''
        if word in dynamic_property and i!= len(seg_content)-1:
            if seg_content[i+1] != u'，':
                i += 1
                continue
        '''
        if word in dynamic_property:  #判断动态词性的词是情感词还是程度副词，比如 “老”，“好”，如果是，再详细判断
            k = i + 1
            flag = 0
            for postword in seg_content[k:]:  #对这个词后的所有词扫描
                if postword == u'，' or postword == u'的':  #如果先发现“，”或者“的”，说明这个词是情感极性词。跳出扫描
                    break
                if postword in posdict or postword in negdict:  #如果先发现有词语在极性词当中，说明这个词是程度副词，重新扫描下一个词
                    flag = 1
            if flag == 1:
                i += 1
                continue
        if word in posdict:  #如果是极性词的肯定词
            #print 'pos',word #test
            pos_temp = 1
            inver_num = 0  #记录反转词的个数
            t = i - 1
            while (seg_content[t] != u'，' and t > -1):  #如果这个词不是第一个词，前面也不是“，”，就一直向前找到seg_content[t]为逗号或者t=-1为止
                t -= 1
            if i > 0 and t + 1 > a:
                a = t + 1
            for w in seg_content[a:i]:
                # print w+str(a)+str(i)
                pos_temp, inver_num = wordCal(w, pos_temp, inver_num)  #
                # print str(pos_temp),str(inver_num)
            if word in dynamic_sentiment:
                for w in seg_content[a:i]:
                    #print w
                    if w in dynamic_inverse:
                        pos_temp *= -1
                    if w in dynamic_remove:
                        pos_temp = 0
            a = i + 1
            poscount += pos_temp
            # print poscount      #test
        elif word in negdict:
            #print 'neg',word #test
            neg_temp = 1
            if word in ordinarydict:
                neg_temp *= ordinary_para
            inver_num = 0
            t = i - 1
            while (seg_content[t] != u'，' and t > -1):
                t -= 1
            if i > 0 and t + 1 > a:
                a = t + 1
            #print i,t,a #test
            for w in seg_content[a:i]:
                neg_temp, inver_num = wordCal(w, neg_temp, inver_num)  #
                #print w,neg_temp ,inver_num #test
            if word in dynamic_sentiment:
                for w in seg_content[a:i]:
                    if w in dynamic_inverse:
                        neg_temp *= -1
                    if w in dynamic_remove:
                        neg_temp = 0
            a = i + 1
            negcount += neg_temp
        i += 1
    return score_trans2(poscount - negcount)
    '''
    if poscount < 0:
        poscount *= neg_reduce
    if negcount > 0:
        negcount *= neg_reduce
    return score_trans(poscount - negcount)
    '''

def sentimentScoreStar(content):  #计算content的娱乐程度分数

    i = 0  # word position counter
    a = 0  # sentiment word position
    poscount = 0  # count a positive word
    negcount = 0  # count a negative word
    poscountlist=[0]
    negcountlist=[0]


    seg_content=divContent(content,posstardict,negstardict)

    for word in seg_content:
        '''
        if word in dynamic_property and i!= len(seg_content)-1:
            if seg_content[i+1] != u'，':
                i += 1
                continue
        '''
        if word in dynamic_property:  #判断动态词性的词是情感词还是程度副词，比如 “老”，“好”，如果是，再详细判断
            k = i + 1
            flag = 0
            for postword in seg_content[k:]:  #对这个词后的所有词扫描
                if postword == u'，' or postword == u'的':  #如果先发现“，”或者“的”，说明这个词是情感极性词。跳出扫描
                    break
                if postword in posdict or postword in negdict:  #如果先发现有词语在极性词当中，说明这个词是程度副词，重新扫描下一个词
                    flag = 1
            if flag == 1:
                i += 1
                continue
        if word in posstardict:  #如果是极性词的肯定词
            #print 'pos', word  #test
            pos_temp = 1
            inver_num = 0  #记录反转词的个数
            t = i - 1
            while (seg_content[t] != u'，' and t > -1):  #如果这个词不是第一个词，前面也不是“，”，就一直向前找到seg_content[t]为逗号或者t=-1为止
                t -= 1
            if i > 0 and t + 1 > a:
                a = t + 1
            for w in seg_content[a:i]:
                #print w + str(a) + str(i)
                pos_temp, inver_num = wordCal(w, pos_temp, inver_num)  #
                #print str(pos_temp), str(inver_num)
            a = i + 1
            poscountlist.append(pos_temp)
            # print poscount      #test
        elif word in negstardict:
            #print 'neg', word  #test
            neg_temp = 1
            if word in ordinarydict:
                neg_temp *= ordinary_para
            inver_num = 0
            t = i - 1
            while (seg_content[t] != u'，' and t > -1):
                t -= 1
            if i > 0 and t + 1 > a:
                a = t + 1
            print i, t, a  #test
            for w in seg_content[a:i]:
                neg_temp, inver_num = wordCal(w, neg_temp, inver_num)  #
                #print w, neg_temp, inver_num  #test
            a = i + 1
            negcountlist.append(neg_temp)
            #print "negcount=" + str(negcount)
        i += 1
	poscountSorted=sorted(poscountlist)
	negcountSorted=sorted(negcountlist)
    poscount=poscountSorted[-1]+poscountSorted[0]
    negcount=negcountSorted[-1]+negcountSorted[0]
    return score_trans2(poscount - negcount)