# backend/answerSearch.py

import os
import json
import math  # 引入 math 模块用于计算
from utils import logMessage


class AnswerSearcher:
    def __init__(self):
        # 加载节点和关系数据
        nodes_file = os.path.join(os.path.dirname(__file__), 'nodes.json')
        relationships_file = os.path.join(os.path.dirname(__file__), 'relationships.json')

        # 加载 nodes.json
        try:
            with open(nodes_file, 'r', encoding='utf-8') as f:
                nodes_data = json.load(f)
            logMessage("成功加载 nodes.json")
        except Exception as e:
            logMessage(f"加载 nodes.json 时出错: {e}")
            nodes_data = []

        # 加载 relationships.json
        try:
            with open(relationships_file, 'r', encoding='utf-8') as f:
                relationships_data = json.load(f)
            logMessage("成功加载 relationships.json")
        except Exception as e:
            logMessage(f"加载 relationships.json 时出错: {e}")
            relationships_data = []

        # 构建节点列表和关系列表
        self.nodes = self.build_nodes(nodes_data)
        self.relationships = self.build_relationships(relationships_data)

        logMessage(f"总节点数: {len(self.nodes)}")
        logMessage(f"总关系数: {len(self.relationships)}")

        # 构建从节点名称到节点的映射，仅包含标签为 'SleepDisorder' 的节点
        self.node_name_map = {
            node['properties']['name']: node
            for node in self.nodes
            if 'SleepDisorder' in node.get('labels', [])
        }

        logMessage(f"SleepDisorder 节点数: {len(self.node_name_map)}")

        # 检查 node_name_map 是否正确
        for name in self.node_name_map:
            logMessage(f"映射的疾病名称: {name}")

        # 构建关系映射，以便快速查询
        self.build_relationship_maps()

        logMessage("JSON 数据加载并处理成功")

    def build_nodes(self, nodes_data):
        nodes = []
        for item in nodes_data:
            node = item.get('n', {})
            if node:
                nodes.append(node)
            else:
                logMessage(f"节点数据格式错误: {item}")
        return nodes

    def build_relationships(self, relationships_data):
        relationships = []
        for item in relationships_data:
            relationship = item.get('p', {})
            if relationship:
                relationships.append(relationship)
            else:
                logMessage(f"关系数据格式错误: {item}")
        return relationships

    def build_relationship_maps(self):
        # 构建关系映射，方便查询疾病与症状、治疗等的关联
        self.disease_symptom_map = {}
        self.symptom_disease_map = {}
        self.disease_related_info = {}

        for relationship in self.relationships:
            start_node = relationship.get('start', {})
            end_node = relationship.get('end', {})
            segments = relationship.get('segments', [])
            if not segments:
                logMessage(f"关系缺少 segments: {relationship}")
                continue
            relationship_type = segments[0].get('relationship', {}).get('type', '')
            if not relationship_type:
                logMessage(f"关系缺少 type: {relationship}")
                continue

            # 保留关系类型的原始大小写
            # 如果需要，可以根据具体情况转换，例如全部小写
            # relationship_type = relationship_type.lower()

            # 获取节点名称和标签
            start_name = start_node.get('properties', {}).get('name', '')
            end_name = end_node.get('properties', {}).get('name', '')
            start_labels = start_node.get('labels', [])
            end_labels = end_node.get('labels', [])

            # 处理 'ASSOCIATED_WITH' 类型关系，症状关联疾病
            if relationship_type == 'ASSOCIATED_WITH':
                if 'SleepDisorder' in end_labels and 'Symptom' in start_labels:
                    # 症状关联疾病
                    disease_name = end_name
                    symptom_name = start_name

                    self.disease_symptom_map.setdefault(disease_name, set()).add(symptom_name)
                    self.symptom_disease_map.setdefault(symptom_name, set()).add(disease_name)

            # 构建疾病相关信息映射
            if 'SleepDisorder' in start_labels:
                disease_name = start_name
                related_node_name = end_name
                related_node_label = end_node.get('labels', [])[0] if end_node.get('labels') else ''
                self.add_disease_related_info(disease_name, relationship_type, related_node_name, related_node_label)
            elif 'SleepDisorder' in end_labels:
                disease_name = end_name
                related_node_name = start_name
                related_node_label = start_node.get('labels', [])[0] if start_node.get('labels') else ''
                self.add_disease_related_info(disease_name, relationship_type, related_node_name, related_node_label)

    def add_disease_related_info(self, disease_name, relationship_type, related_node_name, related_node_label):
        if disease_name not in self.disease_related_info:
            self.disease_related_info[disease_name] = {
                'diagnostic_standards': set(),
                'treatments': set(),
                'risks': set(),
                'related_diseases': set(),
                'complications': set(),
                'related_symptoms': set()
            }

        if relationship_type == 'DIAGNOSED_BY' and related_node_label == 'DiagnosticStandard':
            self.disease_related_info[disease_name]['diagnostic_standards'].add(related_node_name)
        elif relationship_type == 'RECOMMENDED_FOR' and related_node_label == 'Treatment':
            self.disease_related_info[disease_name]['treatments'].add(related_node_name)
        elif relationship_type == 'INFLUENCES_RISK_OF':
            if related_node_label == 'Risks':
                self.disease_related_info[disease_name]['risks'].add(related_node_name)
            elif related_node_label == 'RelatedDisease':
                self.disease_related_info[disease_name]['related_diseases'].add(related_node_name)
        elif relationship_type == 'COOCCURS_WITH' and related_node_label == 'Complication':
            self.disease_related_info[disease_name]['complications'].add(related_node_name)
        elif relationship_type == 'ASSOCIATED_WITH' and related_node_label == 'Symptom':
            self.disease_related_info[disease_name]['related_symptoms'].add(related_node_name)

    def searchMain(self, sqls):
        """
        执行查询并处理结果。

        参数:
            sqls (list): 查询参数的列表。

        返回:
            list: 查询结果的列表。
        """
        finalAnswers = []
        for sql_entry in sqls:
            query_type = sql_entry.get('type')
            params = sql_entry.get('params', {})
            try:
                if query_type == 'matched_diseases':
                    matched_diseases = self.find_matched_diseases(params)
                    finalAnswers.append({'type': 'matched_diseases', 'matched_diseases': matched_diseases})
                    logMessage(f"Processed matched_diseases: {matched_diseases}")
            except Exception as e:
                logMessage(f"查询失败：{e}")
                continue
        return finalAnswers

    def find_matched_diseases(self, params):
        """
        根据症状查找匹配的疾病。

        参数:
            params (dict): 查询参数，包括症状列表。

        返回:
            list: 匹配的疾病列表。
        """
        selected_symptoms = [value for key, value in params.items()]
        logMessage(f"Selected symptoms: {selected_symptoms}")

        # 找到可能的疾病集合
        possible_diseases = set()
        for symptom in selected_symptoms:
            diseases = self.symptom_disease_map.get(symptom, set())
            possible_diseases.update(diseases)

        logMessage(f"Possible diseases: {possible_diseases}")

        # 收集每个疾病的得分
        disease_scores = []
        for disease_name in possible_diseases:
            matched_symptoms = set(selected_symptoms) & self.disease_symptom_map.get(disease_name, set())
            total_symptoms = self.disease_symptom_map.get(disease_name, set())

            # 计算 Precision 和 Recall
            precision = len(matched_symptoms) / len(selected_symptoms) if len(selected_symptoms) > 0 else 0
            recall = len(matched_symptoms) / len(total_symptoms) if len(total_symptoms) > 0 else 0

            # 计算 F1 Score
            if precision + recall > 0:
                f1_score = 2 * precision * recall / (precision + recall)
            else:
                f1_score = 0

            disease_scores.append((disease_name, f1_score, matched_symptoms, total_symptoms))

        logMessage(f"Disease scores: {disease_scores}")

        # 使用 Softmax 将 F1 Scores 转换为概率
        k = 8  # 调整 k 值来控制概率的分布，k 越大，概率差异越明显
        exp_scores = [
            (disease_name, math.exp(f1_score * k), matched_symptoms, total_symptoms)
            for (disease_name, f1_score, matched_symptoms, total_symptoms) in disease_scores
        ]
        total_exp = sum([score for (_, score, _, _) in exp_scores])

        logMessage(f"Total exp scores: {total_exp}")

        # 避免除零错误
        if total_exp == 0:
            total_exp = 1

        matched_diseases = []
        for disease_name, exp_score, matched_symptoms, total_symptoms in exp_scores:
            # 计算归一化概率
            probability = (exp_score / total_exp) * 100

            disease_node = self.node_name_map.get(disease_name, {})
            if not disease_node:
                logMessage(f"未找到疾病节点: {disease_name}")
                abbreviation = '暂无简称'
                description = '暂无描述'
            else:
                properties = disease_node.get('properties', {})
                abbreviation = properties.get('abbreviation', '暂无简称')
                description = properties.get('description', '暂无描述')

                # 检查 description 是否存在
                if 'description' not in properties:
                    logMessage(f"疾病节点 '{disease_name}' 缺少 'description' 字段。")
                if 'abbreviation' not in properties:
                    logMessage(f"疾病节点 '{disease_name}' 缺少 'abbreviation' 字段。")

                logMessage(f"Disease: {disease_name}, Abbreviation: {abbreviation}, Description: {description}")

            # 获取相关信息
            related_info = self.disease_related_info.get(disease_name, {})
            diagnostic_standards = list(related_info.get('diagnostic_standards', []))
            treatments = list(related_info.get('treatments', []))
            risks = list(related_info.get('risks', []))
            related_diseases = list(related_info.get('related_diseases', []))
            complications = list(related_info.get('complications', []))
            preventive_advice = "保持规律的作息时间，减少咖啡因摄入。"  # 可以根据需要修改
            related_symptoms = list(related_info.get('related_symptoms', []))

            matched_diseases.append({
                "disease": disease_name,
                "probability": f"{probability:.1f}%",
                "abbreviation": abbreviation,
                "description": description,
                "diagnostic_standards": diagnostic_standards,
                "treatments": treatments,
                "risks": risks,
                "related_diseases": related_diseases,
                "complications": complications,
                "preventive_advice": preventive_advice,
                "related_symptoms": related_symptoms
            })

        # 按概率排序
        matched_diseases.sort(key=lambda x: float(x['probability'].strip('%')), reverse=True)

        logMessage(f"Matched diseases sorted: {matched_diseases}")

        return matched_diseases

    def get_related_symptoms(self, current_symptoms):
        """
        根据当前症状获取相关的其他症状。

        参数:
            current_symptoms (list): 当前已选择的症状列表。

        返回:
            list: 相关的其他症状列表。
        """
        possible_diseases = set()
        for symptom in current_symptoms:
            diseases = self.symptom_disease_map.get(symptom, set())
            possible_diseases.update(diseases)

        related_symptoms = set()
        for disease in possible_diseases:
            symptoms = self.disease_symptom_map.get(disease, set())
            related_symptoms.update(symptoms)

        # 排除已选择的症状
        related_symptoms = related_symptoms - set(current_symptoms)
        related_symptoms = list(related_symptoms)[:20]
        logMessage(f"Related symptoms: {related_symptoms}")
        return related_symptoms
