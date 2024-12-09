from const import (
    DEFAULT_ANSWER, 
    QUESTION_TYPE_SYMPTOM_SELECTION, 
    QUESTION_TYPE_DIAGNOSIS,
    NODE_SLEEP_DISORDER,
    NODE_SYMPTOM,
    NODE_DIAGNOSTIC_STANDARD,
    NODE_TEST,
    NODE_TREATMENT,
    NODE_RISKS,
    NODE_RELATED_DISEASE,
    NODE_COMPLICATION,
    RELATIONSHIP_ASSOCIATED_WITH,
    RELATIONSHIP_DIAGNOSED_BY,
    RELATIONSHIP_RECOMMENDED_FOR,
    RELATIONSHIP_INFLUENCES_RISK_OF,
    RELATIONSHIP_COOCCURS_WITH,

    QUESTION_TYPE_SYMPTOM_SELECTION,
    QUESTION_TYPE_DIAGNOSIS,
    QUESTION_TYPE_DISEASE_DETAIL,
    QUESTION_TYPE_SUMMARY,
    QUESTION_TYPE_FILTERED_SUMMARY,
)
from utils import wrapSuccess, wrapFailData, logMessage
from flask import jsonify, request

def processQuestion(handle, question, session):
    """
    处理用户的问题，管理会话状态，返回响应。

    参数:
        handle (dict): 处理器字典，包含 'questionClassifier', 'questionParser', 'answerSearcher'。
        question (str): 用户输入的问题。
        session (dict): 用户会话数据。

    返回:
        dict: API响应。
    """
    logMessage(f"当前 Session 数据: {session}")
    logMessage(f"Handle received in processQuestion: {handle}")  # 添加日志
    # 初始化用户状态，添加 'presented_symptoms' 键
    user_state = session.get('user_state', {
        'stage': 'initial',
        'selected_symptoms': [],
        'matched_diseases': [],
        'presented_symptoms': []
    })
    selected_symptoms = user_state.get('selected_symptoms', [])
    matched_diseases = user_state.get('matched_diseases', [])
    presented_symptoms = user_state.get('presented_symptoms', [])
    stage = user_state.get('stage', 'initial')
    logMessage(f"当前用户状态: {user_state}")
    logMessage(f"接收到的问题: {question}")

    # 检查 'question' 参数是否存在且为非空字符串
    if not question:
        logMessage("Missing question parameter.")
        return wrapFailData(**{
            "status": "fail",
            "errorCode": 1,
            "errorMessage": "缺少问题参数。"
        })

    # 检查 'question' 是否为字符串且长度合理
    if not isinstance(question, str) or len(question) > 500:
        logMessage("Invalid question input.")
        return wrapFailData(**{
            "status": "fail",
            "errorCode": 3,
            "errorMessage": "问题输入无效。"
        })

    result = {
        "answer": {"message": DEFAULT_ANSWER}  # 默认回答
    }

    def get_symptom_description(symptom_name):
        """
        根据症状名称获取其描述，如果没有描述，则使用名称作为描述。

        参数:
            symptom_name (str): 名称。

        Returns:
            str: 描述。
        """
        # 使用 handle['answerSearcher'].node_name_map 访问节点数据
        symptom_node = handle['answerSearcher'].node_name_map.get(symptom_name)
        if symptom_node:
            return symptom_node['properties'].get('description', symptom_name)
        else:
            return symptom_name  # 如果找不到节点，默认使用名称

    if question.strip() == '开始诊断' and stage == 'initial':
        # 初始阶段，提供固定的症状选项
        fixed_symptom_names = ["白天嗜睡", "注意力不集中", "疲劳","夜间觉醒","不自主肢体运动","发作性","醒后不能回忆发作过程","身体摇摆型节律性运动","刻板性","反复性","其他类型节律性运动","摇头型节律性运动","混合型节律性运动"]

        # 为每个症状添加描述
        fixed_symptoms_with_desc = [
            {
                "name": sym,
                "description": get_symptom_description(sym)
            }
            for sym in fixed_symptom_names
        ]

        result['answer'] = {
            "type": "symptom_selection",
            "symptoms": fixed_symptoms_with_desc,
            "message": "请选择您正在经历的症状（可以选择多个）："
        }
        # 更新 'presented_symptoms'
        user_state['presented_symptoms'].extend(fixed_symptom_names)
        session['user_state'] = user_state
        logMessage(f"Initial symptom selection provided: {fixed_symptoms_with_desc}")
        return wrapSuccess(result)

    elif stage == 'initial':
        if question.strip() == '开始诊断':
            # 用户已经在初始阶段，避免重复处理
            result['answer'] = {
                "type": "message",
                "content": "您已经在诊断过程中，请选择症状。"
            }
            return wrapSuccess(result)

        # 用户在初始阶段，处理选择的症状
        selected_input = [sym.strip() for sym in question.split(',') if sym.strip()]
        logMessage(f"用户选择的症状: {selected_input}")

        if not selected_input:
            # 用户没有输入任何症状，提示重新输入
            result['answer'] = {
                "type": "message",
                "content": "请按照提示选择症状（可以选择多个）。"
            }
            return wrapSuccess(result)

        # 通过分类器检查哪些症状是有效的
        medicalDict = handle['questionClassifier'].classify(','.join(selected_input))
        args = medicalDict.get('args', {})
        valid_symptoms = [sym for sym in selected_input if sym in args and NODE_SYMPTOM in args[sym]]
        invalid_symptoms = [sym for sym in selected_input if sym not in args or NODE_SYMPTOM not in args[sym]]

        logMessage(f"Valid symptoms to add: {valid_symptoms}")
        logMessage(f"Invalid symptoms: {invalid_symptoms}")

        if invalid_symptoms:
            # 告知用户输入了无效的症状
            result['answer'] = {
                "type": "message",
                "content": f"以下症状未能识别：{', '.join(invalid_symptoms)}。请重新输入有效的症状。"
            }
            logMessage(f"Invalid symptoms entered: {invalid_symptoms}")
            return wrapSuccess(result)

        # 更新已选择的有效症状列表
        selected_symptoms.extend(valid_symptoms)
        selected_symptoms = list(dict.fromkeys(selected_symptoms))  # 去重并保持顺序
        user_state['selected_symptoms'] = selected_symptoms

        # 更新用户状态为 'select_symptom'
        user_state['stage'] = 'select_symptom'
        session['user_state'] = user_state
        logMessage(f"累计选择的有效症状: {selected_symptoms}")
        logMessage(f"用户状态更新为 'select_symptom' 阶段")

        # 获取相关的其他症状
        related_symptoms = handle['answerSearcher'].get_related_symptoms(selected_symptoms)

        # 排除已展示过的症状
        all_previously_presented_symptoms = user_state.get('presented_symptoms', []) + user_state.get('selected_symptoms', [])
        related_symptoms = [
            sym for sym in related_symptoms
            if sym not in all_previously_presented_symptoms
        ]

        logMessage(f"Related symptoms extracted after exclusion: {related_symptoms}")

        if related_symptoms:
            # 获取相关症状的描述
            related_symptoms_with_desc = [
                {
                    "name": sym,
                    "description": get_symptom_description(sym)
                }
                for sym in related_symptoms
            ]

            result['answer'] = {
                "type": "symptom_selection",
                "symptoms": related_symptoms_with_desc,
                "message": "基于您选择的症状，以下是可能相关的其他症状。请选择您还正在经历的症状（可以选择多个），若没有症状可点击 '结束' 以完成选择："
            }
            # 更新 'presented_symptoms'
            user_state['presented_symptoms'].extend(related_symptoms)
            session['user_state'] = user_state
            logMessage(f"Symptom selection phase initiated with symptoms: {related_symptoms_with_desc}")
        else:
            # 无更多相关症状，进入诊断阶段
            return processQuestion(handle, '结束', session)

        return wrapSuccess(result)

    elif stage == 'select_symptom':
        if question.strip() == '开始诊断':
            # 重置会话状态
            session.pop('user_state', None)
            logMessage("Session reset due to '开始诊断' input in select_symptom stage.")
            return processQuestion(handle, question, session)

        # 用户在症状选择阶段，处理选择的症状
        selected_input = [sym.strip() for sym in question.split(',') if sym.strip()]
        if '结束' in selected_input:
            selected_input.remove('结束')
            finish_selection = True
        else:
            finish_selection = False

        logMessage(f"用户选择的症状: {selected_input}")

        if not selected_input and not finish_selection:
            # 用户没有输入任何有效症状，提示重新输入或结束
            result['answer'] = {
                "type": "message",
                "content": "请按照提示选择症状，或输入 '结束' 以完成选择。"
            }
            logMessage("User did not input any valid symptoms or '结束'.")
            return wrapSuccess(result)

        # 通过分类器检查哪些症状是有效的
        medicalDict = handle['questionClassifier'].classify(','.join(selected_input))
        args = medicalDict.get('args', {})
        valid_symptoms = [sym for sym in selected_input if sym in args and NODE_SYMPTOM in args[sym]]
        invalid_symptoms = [sym for sym in selected_input if sym not in args or NODE_SYMPTOM not in args[sym]]

        logMessage(f"Valid symptoms to add: {valid_symptoms}")
        logMessage(f"Invalid symptoms: {invalid_symptoms}")

        if invalid_symptoms and not finish_selection:
            # 告知用户输入了无效的症状
            result['answer'] = {
                "type": "message",
                "content": f"以下症状未能识别：{', '.join(invalid_symptoms)}。请重新输入有效的症状，或输入 '结束' 以完成选择。"
            }
            logMessage(f"Invalid symptoms entered: {invalid_symptoms}")
            return wrapSuccess(result)

        # 更新已选择的有效症状列表
        selected_symptoms.extend(valid_symptoms)
        selected_symptoms = list(dict.fromkeys(selected_symptoms))  # 去重并保持顺序
        user_state['selected_symptoms'] = selected_symptoms
        session['user_state'] = user_state

        logMessage(f"累计选择的有效症状: {selected_symptoms}")

        if finish_selection:
            # 用户选择结束，进入诊断阶段
            if not selected_symptoms:
                # 返回预期的错误消息
                result['answer'] = {
                    "type": "message",
                    "content": "抱歉，您尚未选择任何症状，无法进行诊断。"
                }
                logMessage("User chose to finish without selecting any symptoms.")
                return wrapSuccess(result)

            # 生成诊断查询
            sqls = handle['questionParser'].parserMain(selected_symptoms, user_state)
            logMessage(f"Generated diagnosis queries: {sqls}")

            # 搜索答案
            answers = handle['answerSearcher'].searchMain(sqls)
            logMessage(f"Search results: {answers}")

            if answers:
                # 处理 matched_diseases 类型的回答
                matched_diseases = []
                for ans in answers:
                    if ans['type'] == "matched_diseases":
                        matched_diseases = ans.get('matched_diseases', [])
                        logMessage(f"Matched diseases: {matched_diseases}")  # 添加日志
                        break
                user_state['matched_diseases'] = matched_diseases
                user_state['stage'] = 'diagnosis'
                session['user_state'] = user_state
                logMessage(f"User state updated to diagnosis stage: {user_state}")

                if not matched_diseases:
                    # 无匹配疾病，提示用户
                    result['answer'] = {
                        "type": "message",
                        "content": "抱歉，根据您提供的症状，未能匹配到相关的睡眠障碍疾病。请尝试提供更多症状。"
                    }
                    logMessage("No matching diseases found.")
                    return wrapSuccess(result)

                # 提供诊断结果
                diagnosis_results = matched_diseases  # 已经是所需的格式

                result['answer'] = {
                    "type": "diagnosis_result",
                    "matched_diseases": diagnosis_results,
                    "message": "基于您提供的所有症状，以下是最有可能的睡眠障碍疾病及其预防建议："
                }
                logMessage(f"Final diagnosis_result: {result['answer']}")
                user_state['stage'] = 'diagnosis'
                session['user_state'] = user_state

            else:
                # 查询出错或未返回结果
                result['answer'] = {
                    "type": "message",
                    "content": "抱歉，进行诊断时发生了错误。请稍后再试。"
                }
                logMessage("No answers returned from search.")
                return wrapSuccess(result)

            return wrapSuccess(result)

        else:
            # 用户未选择“结束”，继续症状选择阶段
            if valid_symptoms:
                # 获取相关的其他症状
                related_symptoms = handle['answerSearcher'].get_related_symptoms(selected_symptoms)

                # 排除已展示过的症状
                all_previously_presented_symptoms = user_state.get('presented_symptoms', []) + user_state.get('selected_symptoms', [])
                related_symptoms = [
                    sym for sym in related_symptoms
                    if sym not in all_previously_presented_symptoms
                ]

                logMessage(f"Related symptoms extracted after exclusion: {related_symptoms}")

                if related_symptoms:
                    # 获取相关症状的描述
                    related_symptoms_with_desc = [
                        {
                            "name": sym,
                            "description": get_symptom_description(sym)
                        }
                        for sym in related_symptoms
                    ]

                    result['answer'] = {
                        "type": "symptom_selection",
                        "symptoms": related_symptoms_with_desc,
                        "message": "基于您选择的症状，以下是可能相关的其他症状。请选择您还正在经历的症状（可以选择多个），若没有症状可点击 '结束' 以完成选择："
                    }
                    # 更新 'presented_symptoms'
                    user_state['presented_symptoms'].extend(related_symptoms)
                    user_state['stage'] = 'select_symptom'
                    session['user_state'] = user_state
                    logMessage(f"Symptom selection phase initiated with symptoms: {related_symptoms_with_desc}")
                else:
                    # 无更多相关症状，进入诊断阶段
                    return processQuestion(handle, '结束', session)
            else:
                # 用户未选择任何有效症状
                if not finish_selection:
                    result['answer'] = {
                        "type": "message",
                        "content": "请继续选择症状，或输入 '结束' 以完成选择。"
                    }
                    logMessage("User did not input any valid symptoms.")
                elif finish_selection and not selected_symptoms:
                    # 用户选择“结束”但未选择任何症状
                    result['answer'] = {
                        "type": "message",
                        "content": "抱歉，您尚未选择任何症状，无法进行诊断。"
                    }
                    logMessage("User chose to finish without selecting any symptoms.")
                return wrapSuccess(result)

    else:
        # 如果在其他阶段收到 '开始诊断'，重置会话
        if question.strip() == '开始诊断':
            session.pop('user_state', None)
            logMessage("Session reset due to '开始诊断' input in other stage.")
            return processQuestion(handle, question, session)
        else:
            result['answer'] = {
                "type": "message",
                "content": "抱歉，我无法理解您的输入。请输入 '开始诊断' 开始新的诊断。"
            }
            return wrapSuccess(result)

    return wrapSuccess(result)
