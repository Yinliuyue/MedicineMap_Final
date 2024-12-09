# backend/questionParser.py

from utils import logMessage
from const import (
    NODE_SLEEP_DISORDER,
    NODE_SYMPTOM,
    QUESTION_TYPE_SYMPTOM_SELECTION,
    QUESTION_TYPE_DIAGNOSIS,
    QUESTION_TYPE_DISEASE_DETAIL,
    QUESTION_TYPE_SUMMARY,
    QUESTION_TYPE_FILTERED_SUMMARY,
)

class QuestionParser:
    '''构建实体节点字典'''
    def buildEntityDict(self, symptoms):
        """
        构建实体节点字典。

        参数:
            symptoms (list): 用户选择的症状列表。

        返回:
            dict: 实体节点字典。
        """
        entityDict = {NODE_SYMPTOM: []}
        for symptom in symptoms:
            entityDict[NODE_SYMPTOM].append(symptom)
        return entityDict

    '''解析主函数'''
    def parserMain(self, selected_symptoms, user_state):
        """
        解析用户选择的症状，并生成相应的查询参数。

        参数:
            selected_symptoms (list): 用户选择的症状列表。
            user_state (dict): 用户的当前状态。

        返回:
            list: 查询参数的列表。
        """
        sqls = []

        if not selected_symptoms:
            logMessage("没有选择任何症状。")
            return sqls

        # 构建参数字典
        params = {f"symptom_{i}": symptom for i, symptom in enumerate(selected_symptoms)}
        sqls.append({'type': 'matched_diseases', 'params': params})

        return sqls