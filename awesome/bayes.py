from numpy import *
import numpy as np
import re
import sklearn
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
from nltk.corpus import stopwords as pw
import nltk
import jieba


class Bayes:
    vocabList = None
    p0V, p1V, pSpam = None, None, None

    @classmethod
    def textParse(self, bigString):
        seg_list = jieba.cut(bigString, cut_all=False)
        return [tok for tok in seg_list if len(tok) >= 2]

    @classmethod
    def stopwordslist(self):
        stopwords = [line.strip() for line in open(
            'awesome/data/baidu_stopwords.txt', encoding='utf-8').readlines()]
        return stopwords

    @classmethod
    def createVocabList(self, dataSet):
        vocabSet = set([])
        vocabs = []
        for document in dataSet:
            vocabSet = vocabSet | set(document)
        cacheStopWords = self.stopwordslist()
        for vocab in list(vocabSet):
            if vocab not in cacheStopWords and not vocab.isdigit():
                vocabs.append(vocab)
        return list(vocabs)

    @classmethod
    def bagOfWords2VecMN(self, vocabList, inputSet):
        returnVec = [0] * len(vocabList)
        for word in inputSet:
            if word in vocabList:
                returnVec[vocabList.index(word)] = 1
        return returnVec

    @classmethod
    def trainNB(self, trainMatrix, trainCategory):
        numTrainDocs = len(trainMatrix)
        numWords = len(trainMatrix[0])
        pSpam = 0.5
        p0Num = ones(numWords)
        p1Num = ones(numWords)
        p0Denom = 2.0
        p1Denom = 2.0
        for i in range(numTrainDocs):
            if trainCategory[i] == 1:
                p1Num += trainMatrix[i]
                p1Denom += sum(trainMatrix[i])
            else:
                p0Num += trainMatrix[i]
                p0Denom += sum(trainMatrix[i])
        p1Vect = log(p1Num / p1Denom)
        p0Vect = log(p0Num / p0Denom)
        return p0Vect, p1Vect, pSpam

    @classmethod
    def classifyNB(self, vec2Classify, p0Vec, p1Vec, pClass1):
        p1 = sum(vec2Classify * p1Vec) + log(pClass1)
        p0 = sum(vec2Classify * p0Vec) + log(1 - pClass1)
        if pow(10, p1) / (pow(10, p1) + pow(10, p0)) > 0.5:
            return 1
        else:
            return 0
    @classmethod
    def build(self):
        dataPath = r'awesome/data/dataset.txt'
        jieba.load_userdict(
            'awesome/data/words.txt')
        with open(dataPath, encoding='utf-8') as f:
            txt_list = f.readlines()
        data, classVec, spam_data = [], [], []
        for txt in txt_list:
            txt_list_2 = txt.strip('\n').split('\t')
            if txt_list_2[0] == '0':
                data.append(txt_list_2[-1])
                classVec.append(0)
            elif txt_list_2[0] == '1':
                data.append(txt_list_2[-1])
                classVec.append(1)
                spam_data.append(txt_list_2[-1])

        data_parse, spam_parse, trainMat, trainClasses, trainSet = [], [], [], [], []
        for t in data:
            data_parse.append(self.textParse(t))
        for t in spam_data:
            spam_parse.append(self.textParse(t))
        self.vocabList = self.createVocabList(spam_parse)
        trainSet_ini = np.array((range(4000)))
        randIndex = 0
        trainSet.append(trainSet_ini[:2000])
        for docIndex in trainSet[0]:
            trainMat.append(self.bagOfWords2VecMN(
                self.vocabList, data_parse[docIndex]))
            trainClasses.append(classVec[docIndex])
        self.p0V, self.p1V, self.pSpam = self.trainNB(
            array(trainMat), array(trainClasses))

    @classmethod
    def check(self, sentence):
        wordVector = self.bagOfWords2VecMN(
            self.vocabList, self.textParse(sentence))
        return self.classifyNB(array(wordVector), self.p0V, self.p1V, self.pSpam) == 1 and len(sentence) >= 2