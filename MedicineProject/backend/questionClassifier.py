# backend/questionClassifier.py

import os
import ahocorasick
from utils import logMessage
from const import (
    NODE_SLEEP_DISORDER,
    NODE_SYMPTOM,
    NODE_DIAGNOSTIC_STANDARD,
    NODE_TEST,
    NODE_TREATMENT,
    NODE_RISKS,
    NODE_RELATED_DISEASE,
    NODE_COMPLICATION,

    QUESTION_TYPE_SYMPTOM_SELECTION,  # 用于症状选择阶段
)

def openUTF8(path):
    """以UTF-8编码打开文件"""
    try:
        return open(path, encoding='utf-8')
    except Exception as e:
        logMessage(f"无法打开文件 {path}，原因：{e}")
        return []

class QuestionClassifier:
    def __init__(self):
        # 初始化文件路径
        curDir = os.path.abspath(os.path.dirname(__file__))
        FILE_LAST_DIR = 'dict'  # 文件夹名称

        # 初始化各类特征词文件路径
        self.sleepDisorderFilePath = os.path.join(curDir, FILE_LAST_DIR, "SleepDisorder.txt")
        self.symptomFilePath = os.path.join(curDir, FILE_LAST_DIR, "Symptom.txt")
        self.diagnosticStandardFilePath = os.path.join(curDir, FILE_LAST_DIR, "DiagnosticStandard.txt")
        self.testFilePath = os.path.join(curDir, FILE_LAST_DIR, "Test.txt")
        self.risksFilePath = os.path.join(curDir, FILE_LAST_DIR, "Risks.txt")
        self.relatedDiseaseFilePath = os.path.join(curDir, FILE_LAST_DIR, "RelatedDisease.txt")
        self.preventionFilePath = os.path.join(curDir, FILE_LAST_DIR, "Treatment.txt")
        self.complicationFilePath = os.path.join(curDir, FILE_LAST_DIR, "Complication.txt")
        
        # 加载特征词
        logMessage("加载问题分类模型的特征词")
        self.sleepDisorderWords = [i.strip() for i in openUTF8(self.sleepDisorderFilePath) if i.strip()]
        self.symptomWords = [i.strip() for i in openUTF8(self.symptomFilePath) if i.strip()]
        self.diagnosticStandardWords = [i.strip() for i in openUTF8(self.diagnosticStandardFilePath) if i.strip()]
        self.testWords = [i.strip() for i in openUTF8(self.testFilePath) if i.strip()]
        self.risksWords = [i.strip() for i in openUTF8(self.risksFilePath) if i.strip()]
        self.relatedDiseaseWords = [i.strip() for i in openUTF8(self.relatedDiseaseFilePath) if i.strip()]
        self.preventionWords = [i.strip() for i in openUTF8(self.preventionFilePath) if i.strip()]
        self.complicationWords = [i.strip() for i in openUTF8(self.complicationFilePath) if i.strip()]
        
        logMessage(f"Loaded SleepDisorderWords: {self.sleepDisorderWords}")
        logMessage(f"Loaded SymptomWords: {self.symptomWords}")
        logMessage(f"Loaded DiagnosticStandardWords: {self.diagnosticStandardWords}")
        logMessage(f"Loaded TestWords: {self.testWords}")
        logMessage(f"Loaded RisksWords: {self.risksWords}")
        logMessage(f"Loaded RelatedDiseaseWords: {self.relatedDiseaseWords}")
        logMessage(f"Loaded PreventionWords: {self.preventionWords}")
        logMessage(f"Loaded ComplicationWords: {self.complicationWords}")
        
        # 合并所有关键词
        self.regionWords = set(
            self.sleepDisorderWords + 
            self.symptomWords + 
            self.diagnosticStandardWords + 
            self.testWords +
            self.risksWords +
            self.relatedDiseaseWords +
            self.preventionWords +
            self.complicationWords
        )
        logMessage(f"Total unique keywords: {self.regionWords}")
        
        # 构建Aho-Corasick自动机
        logMessage("构建Aho-Corasick自动机以加速关键词匹配")
        self.regionACTree = self.buildACTree(list(self.regionWords))
        
        # 构建词类型字典
        logMessage("构建词类型字典")
        self.wordTypeDict = self.buildWordTypeDict()
        
        logMessage("问题分类模型初始化成功")
    
    '''构造词对应的类型字典'''
    def buildWordTypeDict(self):
        """
        构建词类型字典，将每个关键词映射到其对应的节点类型。
        
        返回:
            dict: 关键词到节点类型的映射字典。
        """
        wordDict = dict()
        for word in self.regionWords:
            wordDict[word] = []
            if word in self.sleepDisorderWords:
                wordDict[word].append(NODE_SLEEP_DISORDER)
            if word in self.symptomWords:
                wordDict[word].append(NODE_SYMPTOM)
            if word in self.diagnosticStandardWords:
                wordDict[word].append(NODE_DIAGNOSTIC_STANDARD)
            if word in self.testWords:
                wordDict[word].append(NODE_TEST)
            if word in self.risksWords:
                wordDict[word].append(NODE_RISKS)
            if word in self.relatedDiseaseWords:
                wordDict[word].append(NODE_RELATED_DISEASE)
            if word in self.preventionWords:
                wordDict[word].append(NODE_TREATMENT)
            if word in self.complicationWords:
                wordDict[word].append(NODE_COMPLICATION)
        logMessage(f"Word Type Dictionary: {wordDict}")
        return wordDict
    
    '''构造Aho-Corasick自动机'''
    def buildACTree(self, wordList):
        """
        构建Aho-Corasick自动机，用于高效的多模式关键词匹配。
        
        参数:
            wordList (list): 关键词列表。
        
        返回:
            ahocorasick.Automaton: 构建好的Aho-Corasick自动机。
        """
        ACTree = ahocorasick.Automaton()
        for index, word in enumerate(wordList):
            ACTree.add_word(word, (index, word))
        ACTree.make_automaton()
        logMessage("Aho-Corasick自动机构建完成")
        return ACTree
    
    '''问句过滤'''
    def checkMedical(self, question):
        """
        从用户问题中提取相关的医疗关键词，过滤掉重叠的关键词。
        
        参数:
            question (str): 用户输入的问题。
        
        返回:
            dict: 关键词到节点类型的映射字典。
        """
        regionWords = []
        # 使用Aho-Corasick自动机进行多模式匹配
        logMessage(f"开始关键词匹配，用户输入：{question}")
        for item in self.regionACTree.iter(question):
            word = item[1][1]
            regionWords.append(word)
            logMessage(f"匹配到关键词: {word}")
        stopWords = []
        
        # 移除包含关系，避免子词被重复记录
        regionWords = sorted(regionWords, key=len)
        length = len(regionWords)
        for i in range(length):
            word1 = regionWords[i]
            for j in range(i + 1, length):
                word2 = regionWords[j]
                if word1 in word2 and word1 != word2:
                    stopWords.append(word1)
        
        # 保留不在stopWords中的词
        finalWords = [i for i in regionWords if i not in stopWords]
        finalWords = list(set(finalWords))
        logMessage(f"移除停用词后，最终匹配到的关键词: {finalWords}")
        
        # 将关键词映射到其对应的类型
        finalDict = {i: self.wordTypeDict.get(i) for i in finalWords}
        logMessage(f"关键词映射字典: {finalDict}")
        return finalDict
    
    '''分类主函数'''
    def classify(self, question):
        """
        分类用户的问题，返回包含关键词和问题类型的信息。
        
        参数:
            question (str): 用户输入的问题。
        
        返回:
            dict: 包含关键词和问题类型的字典。
        """
        data = {}
        medicalDict = self.checkMedical(question)
        if not medicalDict:
            logMessage("没有匹配到任何关键词。")
            return {}
        data['args'] = medicalDict
        
        # 判断是否为症状输入
        matched_symptoms = [word for word in medicalDict.keys() if NODE_SYMPTOM in medicalDict[word]]
        if matched_symptoms:
            logMessage(f"匹配到的症状: {matched_symptoms}")
            data['questionTypes'] = [QUESTION_TYPE_SYMPTOM_SELECTION]
        else:
            data['questionTypes'] = []
        
        return data