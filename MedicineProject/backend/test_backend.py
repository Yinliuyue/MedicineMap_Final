# backend/test_backend.py

import unittest
from app import app
import json

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_health_check(self):
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"status": "up"})

    def test_get_answer_invalid_params(self):
        response = self.app.post('/getAnswer', json={"invalid": "data"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "fail")
        self.assertEqual(response.get_json()["errorCode"], 1)
        self.assertEqual(response.get_json()["errorMessage"], "缺少问题参数。")

    def test_initial_symptom_selection(self):
        # 模拟用户发送初始问题
        response = self.app.post('/getAnswer', json={"question": "开始诊断"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["data"]["answer"]["type"], "symptom_selection")
        self.assertIn("symptoms", data["data"]["answer"])
        self.assertIsInstance(data["data"]["answer"]["symptoms"], list)
        self.assertTrue(len(data["data"]["answer"]["symptoms"]) > 0)

        # 验证每个症状包含 'name' 和 'description'
        for symptom in data["data"]["answer"]["symptoms"]:
            self.assertIn("name", symptom, "症状项目不包含 'name'")
            self.assertIn("description", symptom, "症状项目不包含 'description'")

        # 保存初始症状列表供后续测试使用
        self.initial_symptoms = data["data"]["answer"]["symptoms"]

    def test_select_symptom_single_with_message(self):
        # 使用保存的初始症状列表
        if not hasattr(self, 'initial_symptoms'):
            self.test_initial_symptom_selection()
        initial_symptoms = self.initial_symptoms

        with self.app as client:
            # 用户选择一个症状
            selected_symptom = initial_symptoms[0]['name']
            response_select = client.post('/getAnswer', json={"question": selected_symptom})
            self.assertEqual(response_select.status_code, 200)
            data_select = response_select.get_json()
            self.assertEqual(data_select["status"], "success")

            answer_type = data_select["data"]["answer"]["type"]
            self.assertIn(answer_type, ["symptom_selection", "diagnosis_result", "message"])

            if answer_type == "symptom_selection":
                # 有相关症状供选择
                self.assertIn("symptoms", data_select["data"]["answer"])
                related_symptoms = data_select["data"]["answer"]["symptoms"]
                self.assertTrue(len(related_symptoms) > 0)
                for symptom in related_symptoms:
                    self.assertIn("name", symptom)
                    self.assertIn("description", symptom)
            elif answer_type == "diagnosis_result":
                # 直接进入诊断
                self.assertIn("matched_diseases", data_select["data"]["answer"])
                diagnosis = data_select["data"]["answer"]["matched_diseases"]
                self.assertTrue(len(diagnosis) > 0)
                for disease in diagnosis:
                    self.assertIn("disease", disease)
                    self.assertIn("probability", disease)
                    self.assertIn("abbreviation", disease)
                    self.assertIn("description", disease)
                    self.assertIn("diagnostic_standards", disease)
                    self.assertIn("treatments", disease)
                    self.assertIn("risks", disease)
                    self.assertIn("related_diseases", disease)
                    self.assertIn("complications", disease)
                    self.assertIn("preventive_advice", disease)
            elif answer_type == "message":
                # 处理无效或不完整输入
                self.assertIn("content", data_select["data"]["answer"])
            else:
                self.fail("Unexpected answer type in single symptom selection.")

    def test_select_symptom_multiple(self):
        # 使用保存的初始症状列表
        if not hasattr(self, 'initial_symptoms'):
            self.test_initial_symptom_selection()
        initial_symptoms = self.initial_symptoms

        with self.app as client:
            # 用户选择多个症状
            if len(initial_symptoms) >= 2:
                selected_symptoms = ','.join(symptom['name'] for symptom in initial_symptoms[:2])
            else:
                selected_symptoms = initial_symptoms[0]['name']
            response_select = client.post('/getAnswer', json={"question": selected_symptoms})
            self.assertEqual(response_select.status_code, 200)
            data_select = response_select.get_json()
            self.assertEqual(data_select["status"], "success")

            answer_type = data_select["data"]["answer"]["type"]
            self.assertIn(answer_type, ["symptom_selection", "diagnosis_result", "message"])

            if answer_type == "symptom_selection":
                # 有相关症状供选择
                self.assertIn("symptoms", data_select["data"]["answer"])
                related_symptoms = data_select["data"]["answer"]["symptoms"]
                self.assertTrue(len(related_symptoms) > 0)
                for symptom in related_symptoms:
                    self.assertIn("name", symptom)
                    self.assertIn("description", symptom)
            elif answer_type == "diagnosis_result":
                # 直接进入诊断
                self.assertIn("matched_diseases", data_select["data"]["answer"])
                diagnosis = data_select["data"]["answer"]["matched_diseases"]
                self.assertTrue(len(diagnosis) > 0)
                for disease in diagnosis:
                    self.assertIn("disease", disease)
                    self.assertIn("probability", disease)
                    self.assertIn("abbreviation", disease)
                    self.assertIn("description", disease)
                    self.assertIn("diagnostic_standards", disease)
                    self.assertIn("treatments", disease)
                    self.assertIn("risks", disease)
                    self.assertIn("related_diseases", disease)
                    self.assertIn("complications", disease)
                    self.assertIn("preventive_advice", disease)
            elif answer_type == "message":
                # 处理无效或不完整输入
                self.assertIn("content", data_select["data"]["answer"])
            else:
                self.fail("Unexpected answer type in multiple symptom selection.")

    def test_diagnosis_stage_with_end(self):
        # 测试完整的诊断流程，包括输入 '结束'
        with self.app as client:
            # 使用保存的初始症状列表
            if not hasattr(self, 'initial_symptoms'):
                self.test_initial_symptom_selection()
            initial_symptoms = self.initial_symptoms

            # 用户选择多个症状
            selected_symptoms = ','.join(symptom['name'] for symptom in initial_symptoms[:2])
            response_select = client.post('/getAnswer', json={"question": selected_symptoms})
            self.assertEqual(response_select.status_code, 200)
            data_select = response_select.get_json()
            self.assertEqual(data_select["status"], "success")

            answer_type = data_select["data"]["answer"]["type"]
            self.assertIn(answer_type, ["symptom_selection", "diagnosis_result", "message"])

            if answer_type == "symptom_selection":
                # 有更多相关症状供选择
                self.assertIn("symptoms", data_select["data"]["answer"])
                related_symptoms = data_select["data"]["answer"]["symptoms"]
                self.assertTrue(len(related_symptoms) > 0)
                for symptom in related_symptoms:
                    self.assertIn("name", symptom)
                    self.assertIn("description", symptom)

                # 用户选择 '结束' 以完成选择
                response_end = client.post('/getAnswer', json={"question": "结束"})
                self.assertEqual(response_end.status_code, 200)
                data_end = response_end.get_json()
                self.assertEqual(data_end["status"], "success")
                self.assertEqual(data_end["data"]["answer"]["type"], "diagnosis_result")
                diagnosis = data_end["data"]["answer"]["matched_diseases"]
                self.assertTrue(len(diagnosis) > 0)
                for disease in diagnosis:
                    self.assertIn("disease", disease)
                    self.assertIn("probability", disease)
                    self.assertIn("abbreviation", disease)
                    self.assertIn("description", disease)
                    self.assertIn("diagnostic_standards", disease)
                    self.assertIn("treatments", disease)
                    self.assertIn("risks", disease)
                    self.assertIn("related_diseases", disease)
                    self.assertIn("complications", disease)
                    self.assertIn("preventive_advice", disease)
            elif answer_type == "diagnosis_result":
                # 直接返回诊断结果，无需进一步操作
                self.assertIn("matched_diseases", data_select["data"]["answer"])
                diagnosis = data_select["data"]["answer"]["matched_diseases"]
                self.assertTrue(len(diagnosis) > 0)
                for disease in diagnosis:
                    self.assertIn("disease", disease)
                    self.assertIn("probability", disease)
                    self.assertIn("abbreviation", disease)
                    self.assertIn("description", disease)
                    self.assertIn("diagnostic_standards", disease)
                    self.assertIn("treatments", disease)
                    self.assertIn("risks", disease)
                    self.assertIn("related_diseases", disease)
                    self.assertIn("complications", disease)
                    self.assertIn("preventive_advice", disease)
            elif answer_type == "message":
                # 处理无效或不完整输入
                self.assertIn("content", data_select["data"]["answer"])
            else:
                self.fail("Unexpected answer type in diagnosis stage.")

    def test_diagnosis_no_match(self):
        # 测试无匹配疾病的情况
        with self.app as client:
            # 初始阶段
            response_initial = client.post('/getAnswer', json={"question": "开始诊断"})
            self.assertEqual(response_initial.status_code, 200)
            data_initial = response_initial.get_json()
            self.assertEqual(data_initial["status"], "success")
            self.assertEqual(data_initial["data"]["answer"]["type"], "symptom_selection")
            initial_symptoms = data_initial["data"]["answer"]["symptoms"]
            self.assertTrue(len(initial_symptoms) > 0)

            # 用户选择一个不存在的症状
            selected_symptom = "不存在的症状"
            response_select = client.post('/getAnswer', json={"question": selected_symptom})
            self.assertEqual(response_select.status_code, 200)
            data_select = response_select.get_json()
            self.assertEqual(data_select["status"], "success")
            self.assertEqual(data_select["data"]["answer"]["type"], "message")  # 因为症状无效，返回提示信息

            # 用户发送 '结束' 来完成选择
            response_finish = client.post('/getAnswer', json={"question": "结束"})
            self.assertEqual(response_finish.status_code, 200)
            data_finish = response_finish.get_json()

            # 应返回未选择任何症状的信息
            self.assertEqual(data_finish["status"], "success")
            self.assertEqual(data_finish["data"]["answer"]["type"], "message")
            self.assertEqual(data_finish["data"]["answer"]["content"], "抱歉，您尚未选择任何症状，无法进行诊断。")

    def test_submit_feedback_invalid_params(self):
        response = self.app.post('/submitFeedback', json={})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "fail")
        self.assertEqual(response.get_json()["errorCode"], 1)
        self.assertEqual(response.get_json()["errorMessage"], "缺少反馈参数。")

    def test_submit_feedback_success(self):
        feedback_payload = {
            "user_id": "user123",
            "rating": 5,
            "comment": "非常好！"
        }
        response = self.app.post('/submitFeedback', json=feedback_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["status"], "success")
        self.assertEqual(response.get_json()["data"]["message"], "反馈提交成功，谢谢您的宝贵意见！")

if __name__ == '__main__':
    unittest.main()
