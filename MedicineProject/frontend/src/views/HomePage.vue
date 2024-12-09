<template>
  <div class="container">
    <h1>欢迎来到AI问答诊断系统</h1>

    <!-- 开始按钮 -->
    <div v-if="!question && !message" class="start-btn-container">
      <button @click="startChat">开始诊断</button>
    </div>

    <!-- 显示问题和选项 -->
    <div v-if="question && !message" class="question-container">
      <p class="question">{{ question }}</p>
      <div v-for="(option, index) in options" :key="index" class="option-item">
        <label class="option-label">
          <input 
            type="checkbox" 
            :value="option.name" 
            v-model="selectedOptions" 
            class="option-checkbox"
          /> 
          {{ option.description }}
        </label>
      </div>
      <!-- 确认按钮 -->
      <button @click="confirmSelection" class="confirm-btn">确认</button>
      <!-- 结束按钮 -->
      <button @click="stopSelection" class="stop-btn">结束</button>
    </div>

    <!-- 诊断结果展示 -->
    <div v-if="message" class="result-container">
      <h2>诊断结果</h2>
      <p>{{ message }}</p>
      <div v-for="(matched_disease, index) in matched_diseases" :key="index" class="disease-item">
        <div class="disease-card">
          <h3>{{ matched_disease.disease }}</h3> <!-- 显示疾病名称 -->
          <p><strong>简称:</strong> {{ matched_disease.abbreviation || '暂无简称' }}</p> <!-- 显示简称 -->
          <p><strong>描述:</strong> {{ matched_disease.description || '暂无描述' }}</p> <!-- 显示描述 -->
          <p><strong>概率:</strong> {{ matched_disease.probability }}</p> <!-- 显示概率 -->
        </div>
      </div>
      <h3>点击结束重新开始</h3>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'HomePage',
  data() {
    return {
      question: '',  // 存储问题
      options: [],   // 存储选项
      selectedOptions: [],  // 存储用户选择的选项
      inSession: false, // 是否处于诊断会话中
      message: '',  // 存储诊断结果消息
      matched_diseases: [],  // 存储匹配的疾病信息
    };
  },
  methods: {
    startChat() {
      this.inSession = true; // 开始会话
      this.getAnswer('开始诊断');
    },
    getAnswer(question) {
      axios.post(
        'http://127.0.0.1:5000/getAnswer', 
        { question },
        { withCredentials: true }
      )
      .then((response) => {
        const answerData = response.data.data;
        if (answerData.answer.type === 'diagnosis_result') {
          this.message = answerData.answer.message;
          this.matched_diseases = answerData.answer.matched_diseases;
          this.$router.push({
            name: 'RecordPage',
            query: {
              message: this.message,
              matched_diseases: JSON.stringify(this.matched_diseases),
            },
          });
          this.inSession = false;
        }
        else{
          this.question = answerData.answer.message || "结束";
          this.options = answerData.answer.symptoms || [];
          this.selectedOptions = [];
        }
      })
      .catch((error) => {
        console.error("Error fetching answer:", error);
      });
    },
    confirmSelection() {
      if (this.selectedOptions.length === 0) {
        alert("请至少选择一个选项！");
        return;
      }

      const selectedNames = this.selectedOptions.join(',');
      const payload = { question: selectedNames };

      axios.post(
        'http://127.0.0.1:5000/getAnswer', 
        payload,
        { withCredentials: true }
      )
      .then((response) => {
        const answerData = response.data.data;
        if (answerData.answer.type === 'diagnosis_result') {
          this.message = answerData.answer.message;
          this.matched_diseases = answerData.answer.matched_diseases;
          this.$router.push({
            name: 'RecordPage',
            query: {
              message: this.message,
              matched_diseases: JSON.stringify(this.matched_diseases),
            },
          });
          this.inSession = false;
        }
        else{
          this.question = answerData.answer.message || "结束";
          this.options = answerData.answer.symptoms || [];
          this.selectedOptions = [];
        }
      })
      .catch((error) => {
        console.error("Error confirming selection:", error);
      });
    },
    stopSelection() {
      this.getAnswer('结束');
    },
  }
};
</script>

<style scoped>
  /* 页面全局布局 */
  .container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    font-family: 'Arial', sans-serif;
    background-color: #f4f7fb;
  }

  /* 标题样式 */
  h1 {
    font-size: 30px;
    color: #4CAF50;
    margin-bottom: 20px;
    text-align: center;
  }

  /* 开始按钮 */
  .start-btn-container button {
    padding: 15px 30px;
    font-size: 18px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s;
  }

  .start-btn-container button:hover {
    background-color: #45a049;
  }

  /* 问题和选项容器 */
  .question-container {
    text-align: center;
    background-color: #fff;
    padding: 20px;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 95%; /* 增宽问答部分 */
    max-width: 800px; /* 设置最大宽度 */
  }


  /* 问题样式 */
  .question {
    font-size: 18px;
    color: #555;
    margin-bottom: 20px;
    font-weight: bold; /* 加粗问题文本 */
  }

  /* 选项样式 */
  .option-item {
    margin-bottom: 15px;
    text-align: left; /* 使选项左对齐 */
  }

  .option-checkbox {
    margin-right: 10px;
  }

  .option-label {
    font-size: 16px;
    color: #333;
    display: inline-block;
    text-align: left; /* 强制标签文本左对齐 */
    margin-left: 20px; /* 增加左边距，以便文本不会紧挨着复选框 */
  }

  /* 确认和结束按钮 */
  button {
    padding: 12px 25px;
    font-size: 16px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: background-color 0.3s;
    margin: 10px;
  }

  button:hover {
    background-color: #45a049;
  }

  /* 诊断结果容器 */
  .result-container {
    text-align: center;
    padding: 30px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    width: 80%;
    max-width: 600px;
  }

  .disease-card {
    background-color: #f9f9f9;
    padding: 15px;
    border-radius: 8px;
    margin-top: 10px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  }

  .disease-card h3 {
    font-size: 20px;
    color: #333;
  }

  .disease-card p {
    font-size: 14px;
    color: #555;
    margin: 5px 0;
  }

  h3 {
    margin-top: 20px;
    font-size: 20px;
    color: #333;
  }
</style>
