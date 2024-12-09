<template>
  <div>
    <h1>诊断结果</h1>

    <!-- 添加柱状图 -->
    <div v-if="matched_diseases.length" class="chart-container">
      <h3>疾病概率柱状图</h3>
      <Bar :data="chartData" :options="chartOptions" />
    </div>

    <!-- 诊断结果展示 -->
    <div v-if="message">
      <h2>诊断结果</h2>
      <p>{{ message }}</p>
      <div v-for="(matched_disease, index) in matched_diseases" :key="index">
        <div>
          <h3>{{ matched_disease.disease }}</h3> <!-- 显示疾病名称 -->
          <p><strong>简称:</strong> <span class="left-align">{{ matched_disease.abbreviation || '暂无简称' }}</span></p> <!-- 显示简称 -->
          <p><strong>描述:</strong> <span class="left-align">{{ matched_disease.description }}</span></p> <!-- 显示描述 -->
          <p><strong>概率:</strong> <span class="left-align">{{ matched_disease.probability }}</span></p> <!-- 显示概率 -->
          
          <!-- 控制展开/收起按钮 -->
          <button @click="toggleDetails(index)" class="toggle-details-btn">
            {{ matched_disease.isExpanded ? '收起详情' : '展开详情' }}
          </button>
          
          <!-- 展开后显示的更多内容 -->
          <div v-if="matched_disease.isExpanded" class="expanded-content">
            <div v-if="matched_disease.complications.length">
              <h4 class="left-align">并发症:</h4>
              <p class="inline-list">
                <span v-for="(complication, index) in matched_disease.complications" :key="index">
                  {{ complication }}<span v-if="index < matched_disease.complications.length - 1">, </span>
                </span>
              </p>
            </div>

            <div v-if="matched_disease.related_diseases.length">
              <h4 class="left-align">相关疾病:</h4>
              <p class="inline-list">
                <span v-for="(related_disease, index) in matched_disease.related_diseases" :key="index">
                  {{ related_disease }}<span v-if="index < matched_disease.related_diseases.length - 1">, </span>
                </span>
              </p>
            </div>

            <div v-if="matched_disease.related_symptoms.length">
              <h4 class="left-align">相关症状:</h4>
              <p class="inline-list">
                <span v-for="(related_symptom, index) in matched_disease.related_symptoms" :key="index">
                  {{ related_symptom }}<span v-if="index < matched_disease.related_symptoms.length - 1">, </span>
                </span>
              </p>
            </div>

            <div v-if="matched_disease.risks.length">
              <h4 class="left-align">风险因素:</h4>
              <p class="inline-list">
                <span v-for="(risk, index) in matched_disease.risks" :key="index">
                  {{ risk }}<span v-if="index < matched_disease.risks.length - 1">, </span>
                </span>
              </p>
            </div>

            <div v-if="matched_disease.treatments.length">
              <h4 class="left-align">治疗方法:</h4>
              <p class="inline-list">
                <span v-for="(treatment, index) in matched_disease.treatments" :key="index">
                  {{ treatment }}<span v-if="index < matched_disease.treatments.length - 1">, </span>
                </span>
              </p>
            </div>

            <div v-if="matched_disease.diagnostic_standards.length">
              <h4 class="left-align">诊断标准:</h4>
              <p class="inline-list">
                <span v-for="(standard, index) in matched_disease.diagnostic_standards" :key="index">
                  {{ standard }}<span v-if="index < matched_disease.diagnostic_standards.length - 1">, </span>
                </span>
              </p>
            </div>

            <div v-if="matched_disease.preventive_advice">
              <h4 class="left-align">预防建议:</h4>
              <p class="inline-list">{{ matched_disease.preventive_advice }}</p>
            </div>

          </div>
        </div>
        <hr />
      </div>
    </div>
    <!-- 填写信息的调查问卷 -->
    <div class="survey-container">
      <h3>用户反馈</h3>
      <form @submit.prevent="submitFeedback">
        <div class="form-group">
          <label for="user_id">名称:</label>
          <input type="text" id="user_id" v-model="feedback.user_id" placeholder="请输入用户ID" required />
        </div>

        <div class="form-group">
          <label for="rating">评分:<span class="required">*</span></label>
          <div class="rating-options">
            <label>
              <input type="radio" v-model="feedback.rating" value="1" /> 1
            </label>
            <label>
              <input type="radio" v-model="feedback.rating" value="2" /> 2
            </label>
            <label>
              <input type="radio" v-model="feedback.rating" value="3" /> 3
            </label>
            <label>
              <input type="radio" v-model="feedback.rating" value="4" /> 4
            </label>
            <label>
              <input type="radio" v-model="feedback.rating" value="5" /> 5
            </label>
          </div>
        </div>

        <div class="form-group">
          <label for="comment">评价:<span class="required">*</span></label>
          <div class="options">
            <label>
              <input type="radio" v-model="feedback.comment" value="毫无帮助" /> 毫无帮助
            </label>
            <label>
              <input type="radio" v-model="feedback.comment" value="帮助不大" /> 帮助不大
            </label>
            <label>
              <input type="radio" v-model="feedback.comment" value="有点帮助" /> 有点帮助
            </label>
            <label>
              <input type="radio" v-model="feedback.comment" value="帮助很多" /> 帮助很多
            </label>
            <label>
              <input type="radio" v-model="feedback.comment" value="非常有帮助" /> 非常有帮助
            </label>
          </div>
        </div>

        <div class="form-group">
          <label for="feedback_type">建议:<span class="required">*</span></label>
          <div class="options">
            <label>
              <input type="radio" v-model="feedback.feedback_type" value="功能问题" /> 功能问题
            </label>
            <label>
              <input type="radio" v-model="feedback.feedback_type" value="错误报告" /> 错误报告
            </label>
            <label>
              <input type="radio" v-model="feedback.feedback_type" value="体验不好" /> 体验不好
            </label>
            <label>
              <input type="radio" v-model="feedback.feedback_type" value="性能问题" /> 性能问题
            </label>
            <label>
              <input type="radio" v-model="feedback.feedback_type" value="其他" /> 其他
            </label>
          </div>
        </div>

        <div class="form-group">
          <label for="contact_info">联系邮箱:</label>
          <input type="email" v-model="feedback.contact_info" id="contact_info" placeholder="请输入邮箱" required />
        </div>

        <div class="form-group">
          <label for="privacy_policy_accepted">接受隐私政策:<span class="required">*</span></label>
          <input type="checkbox" v-model="feedback.privacy_policy_accepted" id="privacy_policy_accepted" required />
        </div>

        <button @click="submit_feedback">提交反馈</button>
      </form>
    </div>
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';
import { Chart as ChartJS, Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale } from 'chart.js';

// 注册 Chart.js 模块
ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale);

import axios from 'axios';

export default {
  name: 'RecordPage',
  components: {
    Bar
  },
  data() {
    return {
      message: '', // 诊断结果信息
      matched_diseases: [], // 匹配的疾病信息
      feedback: {
        user_id: "",
        rating: 0,
        comment: "",
        feedback_type: "",
        contact_info: "",
        privacy_policy_accepted: false
      },
      chartData: {
        labels: [], // 疾病名称
        datasets: [
          {
            label: '疾病概率',
            data: [], // 概率值
            backgroundColor: '#4CAF50', // 柱状图颜色
            borderRadius: 5
          }
        ]
      },
      chartOptions: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          tooltip: {
            callbacks: {
              label: function(tooltipItem) {
                return `${tooltipItem.label}: ${tooltipItem.raw}%`;
              }
            }
          }
        },
        scales: {
          x: {
            beginAtZero: true
          },
          y: {
            beginAtZero: true,
            max: 100, // 设置最大值为100，表示百分比
            ticks: {
              stepSize: 10
            }
          }
        }
      }
    };
  },
  mounted() {
    // 从路由的 query 中获取数据
    const { message, matched_diseases } = this.$route.query;
    this.message = message || '';
    this.matched_diseases = matched_diseases ? JSON.parse(matched_diseases) : [];

    // 初始化每个疾病的 isExpanded 状态
    this.matched_diseases.forEach(disease => {
      disease.isExpanded = false;
    });

    // 检查 matched_diseases 是否为空
    if (this.matched_diseases.length > 0) {
      // 填充柱状图的数据
      this.updateChartData();
    } else {
      console.error("没有匹配的疾病数据！");
    }
  },
  methods: {
    updateChartData() {
      // 提取疾病名称和概率值，并确保概率值是数字类型
      const diseaseNames = this.matched_diseases.map(disease => disease.disease); // 疾病名称
      const probabilities = this.matched_diseases.map(disease => {
        // 如果是字符串，尝试将其转换为数字
        return parseFloat(disease.probability); 
      });

      // 更新 chartData
      this.chartData.labels = diseaseNames;
      this.chartData.datasets[0].data = probabilities;
    },
    toggleDetails(index) {
      // 切换该疾病的 isExpanded 状态
      this.matched_diseases[index].isExpanded = !this.matched_diseases[index].isExpanded;
    },
    submit_feedback() {
      // 检查用户ID、邮箱是否为空，如果为空，则设置为 "none"
      if (!this.feedback.user_id) {
        this.feedback.user_id = "none";
      }
      if (!this.feedback.contact_info) {
        this.feedback.contact_info = "none";
      }

      // 验证评分、评论和接受隐私政策字段是否已填写
      if (!this.feedback.rating || !this.feedback.comment || !this.feedback.feedback_type || !this.feedback.privacy_policy_accepted) {
        alert('评分、评论、建议和隐私政策接受为必填项，请填写完整！');
        return;
      }

      // 如果隐私政策没有同意，提示并阻止提交
      if (!this.feedback.privacy_policy_accepted) {
        alert('请同意隐私政策以继续提交反馈');
        return;
      }

      // 输出 feedback 对象进行检查
      console.log("当前反馈数据：", this.feedback);

      // 发送反馈请求
      axios.post(
        'http://127.0.0.1:5000/submitFeedback', 
        { feedback: this.feedback },  // 将问题作为 JSON 发送
        { withCredentials: true }  // 启用跨域支持
      )
      .then(response => {
        console.log('反馈提交成功:', response.data);
        alert('反馈提交成功，谢谢您的宝贵意见！');
      })
      .catch(error => {
        console.error('提交反馈失败:', error);
        alert('提交反馈失败，请稍后再试！');
      });
    }
  }
};
</script>

<style scoped>

  /* 使小标题左对齐 */
  .left-align {
    text-align: left;
    margin-bottom: 5px; /* 小标题和内容之间的间距 */
  }

  /* 将内容横向排列并换行 */
  .inline-list {
    display: flex;
    flex-wrap: wrap; /* 允许换行 */
    gap: 8px; /* 每个项之间的间距 */
    font-size: 14px; /* 设置字体大小，方便阅读 */
    word-break: break-word; /* 防止内容过长不换行 */
  }

  /* 每个项的格式 */
  .inline-list span {
    white-space: nowrap; /* 防止内容内部换行 */
  }



  /* 整体页面布局 */
  body {
    font-family: 'Arial', sans-serif;
    background-color: #f4f7fa; /* 背景颜色 */
    margin: 0;
    padding: 0;
  }

  h1 {
    font-size: 36px;
    color: #4CAF50;
    margin-bottom: 20px;
    text-align: center;
    text-shadow: 1px 1px 5px rgba(0, 0, 0, 0.1);
  }

  /* 内容容器 */
  .container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  }
  
  .chart-container {
    width: 80%;
    height: 600px;
    margin: 0 auto;
    padding-bottom: 20px;  /* 增加图表容器顶部间距 */
  }

  .chart-container h3 {
    text-align: center;
    margin-bottom: 0px;
    font-size: 24px;
    color: #333;
  }

  /* 反馈表单 */
  .survey-container {
    margin: 40px auto;  /* 使反馈表单居中 */
    padding: 20px;
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
    width: 80%;  /* 设置表单宽度 */
    max-width: 800px;  /* 限制最大宽度 */
  }

  .survey-container h3 {
    font-size: 24px;
    color: #4CAF50;
    margin-bottom: 20px;
  }

  .form-group {
    margin-bottom: 20px;
    text-align: left;
  }

  .form-group label {
    display: inline-block;
    font-weight: bold;
    margin-right: 10px; /* 给标签和选项之间添加一些间距 */
  }

  .form-group input {
    padding: 8px;
    border: 1px solid #ccc;
    border-radius: 4px;
  }

  .options {
    display: flex;
    gap: 10px;
    align-items: center; /* 确保选项垂直居中 */
  }

  .options label {
    display: inline-flex;
    align-items: center;
    cursor: pointer;
  }

  .options input {
    margin-right: 5px;
  }

  button {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 12px 24px;
    cursor: pointer;
    border-radius: 5px;
    font-size: 16px;
    transition: background-color 0.3s ease;
  }

  button:hover {
    background-color: #45a049;
  }

  .required {
    color: red;
    font-weight: bold;
    margin-left: 5px;
  }

  /* 诊断结果部分 */
  .disease-container {
    margin-top: 40px;
    padding: 20px;
    background-color: #fff;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  }

  .disease-container h2 {
    font-size: 28px;
    color: #333;
    margin-bottom: 20px;
  }

  .disease-container p {
    font-size: 16px;
    color: #555;
    line-height: 1.6;
  }

    /* 按钮样式 */
  .toggle-details-btn {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 8px 16px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
    margin-top: 10px;
    transition: background-color 0.3s ease, transform 0.3s ease;
  }

  .toggle-details-btn:hover {
    background-color: #45a049;
    transform: scale(1.05);
  }

  /* 展开内容样式 */
  .expanded-content {
    padding-left: 20px;
    margin-top: 10px;
    font-size: 14px;
    color: #555;
    border-left: 2px solid #4CAF50;
    margin-bottom: 20px;
  }

  /* 各个详情列表 */
  .detail-list {
    list-style-type: disc;
    margin-left: 20px;
    padding: 0;
  }

  .detail-list li {
    margin-bottom: 8px;
  }

  h4 {
    font-size: 18px;
    color: #333;
    font-weight: bold;
    margin-top: 15px;
  }

  /* 动画效果 */
  .expanded-content {
    transition: max-height 0.5s ease-in-out, padding 0.5s ease-in-out;
  }

  .expanded-content ul {
    opacity: 0;
    max-height: 0;
    transition: opacity 0.3s ease, max-height 0.3s ease;
  }

  .expanded-content .detail-list {
    opacity: 1;
    max-height: 1000px;
  }

</style>
