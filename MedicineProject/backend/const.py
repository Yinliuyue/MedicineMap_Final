# backend/const.py

# 节点类型
NODE_SLEEP_DISORDER = "SleepDisorder"
NODE_SYMPTOM = "Symptom"
NODE_DIAGNOSTIC_STANDARD = "DiagnosticStandard"
NODE_TEST = "Test"
NODE_TREATMENT = "Treatment"
NODE_RISKS = "Risks"
NODE_RELATED_DISEASE = "RelatedDisease"
NODE_COMPLICATION = "Complication"

# 关系类型
RELATIONSHIP_ASSOCIATED_WITH = "ASSOCIATED_WITH"  # Symptom -> SleepDisorder 或其他
RELATIONSHIP_DIAGNOSED_BY = "DIAGNOSED_BY"        # SleepDisorder -> DiagnosticStandard
RELATIONSHIP_RECOMMENDED_FOR = "RECOMMENDED_FOR"  # SleepDisorder -> Treatment
RELATIONSHIP_INFLUENCES_RISK_OF = "INFLUENCES_RISK_OF"  # SleepDisorder -> Risks 或 RelatedDisease
RELATIONSHIP_COOCCURS_WITH = "COOCCURS_WITH"      # SleepDisorder -> Complication

# 问题类型
QUESTION_TYPE_SYMPTOM_SELECTION = "symptom_selection"  # 症状选择阶段
QUESTION_TYPE_DIAGNOSIS = "diagnosis"  # 诊断阶段
QUESTION_TYPE_DISEASE_DETAIL = "disease_detail" # 疾病详细信息
QUESTION_TYPE_SUMMARY = "summary" # 匹配到的疾病总结
QUESTION_TYPE_FILTERED_SUMMARY = "filtered_summary" # 过滤后的疾病总结

# API响应常量
ERROR_INVALID_PARAMS = {
    "status": "fail",
    "errorCode": 1,
    "errorMessage": "Invalid parameters"
}

ERROR_PROCESSING = {
    "status": "fail",
    "errorCode": 2,
    "errorMessage": "Processing error"
}

ERROR_UNKNOWN = {
    "status": "fail",
    "errorCode": 3,
    "errorMessage": "Unknown error"
}

DEFAULT_ANSWER = "抱歉，我无法理解您的问题。请尝试其他方式表达。"
