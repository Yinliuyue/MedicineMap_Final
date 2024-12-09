<template>
    <div class="edit-my">
      <h1>修改个人信息</h1>
  
      <!-- 用户信息编辑表单 -->
      <form @submit.prevent="savemy">
        <div class="form-group">
          <label for="username">用户名：</label>
          <input
            type="text"
            id="username"
            v-model="user.username"
            placeholder="请输入用户名"
            required
          />
        </div>
  
        <div class="form-group">
          <label for="email">邮箱：</label>
          <input
            type="email"
            id="email"
            v-model="user.email"
            placeholder="请输入邮箱"
            required
          />
        </div>
  
        <div class="form-group">
          <label for="password">新密码：</label>
          <input
            type="password"
            id="password"
            v-model="user.password"
            placeholder="请输入新密码"
          />
        </div>
  
        <div class="form-group">
          <label for="avatar">头像：</label>
          <input
            type="file"
            id="avatar"
            @change="handleAvatarChange"
          />
          <p v-if="avatarPreview">预览：<img :src="avatarPreview" alt="Avatar Preview" class="avatar-preview" /></p>
        </div>
  
        <div class="form-actions">
          <button type="submit">保存更改</button>
          <button @click="cancelEdit">取消</button>
        </div>
      </form>
    </div>
  </template>
  
  <script>
  export default {
    name: 'EditmyPage',
    data() {
      return {
        user: {
          username: '张三', // 默认用户名
          email: 'zhangsan@example.com', // 默认邮箱
          password: '', // 默认密码为空
          avatar: '', // 默认头像为空
        },
        avatarPreview: '' // 头像预览
      };
    },
    methods: {
      // 处理头像选择
      handleAvatarChange(event) {
        const file = event.target.files[0];
        if (file) {
          const reader = new FileReader();
          reader.onload = () => {
            this.avatarPreview = reader.result; // 设置头像预览
            this.user.avatar = file; // 更新头像
          };
          reader.readAsDataURL(file); // 读取图片文件
        }
      },
      // 保存用户修改的个人信息
      savemy() {
        // 这里你可以调用 API 保存修改的个人信息
        console.log('保存的用户信息：', this.user);
  
        // 提示用户保存成功
        alert('个人信息已保存！');
        
        // 跳转到个人中心页面
        this.$router.push('/my');
      },
      // 取消编辑，跳转回个人中心页面
      cancelEdit() {
        this.$router.push('/my');
      }
    }
  };
  </script>
  
  <style scoped>
  .edit-my {
    text-align: center;
    margin-top: 50px;
  }
  
  h1 {
    font-size: 36px;
    color: #4CAF50;
  }
  
  .form-group {
    margin: 15px 0;
    text-align: left;
    font-size: 18px;
  }
  
  input {
    padding: 8px;
    font-size: 16px;
    width: 80%;
    margin-top: 5px;
    border: 1px solid #ccc;
    border-radius: 5px;
  }
  
  input[type="file"] {
    width: 80%;
  }
  
  .avatar-preview {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    margin-top: 10px;
  }
  
  .form-actions {
    margin-top: 30px;
  }
  
  button {
    background-color: #4CAF50;
    color: white;
    padding: 10px 20px;
    font-size: 16px;
    cursor: pointer;
    border: none;
    border-radius: 5px;
    margin: 10px;
  }
  
  button:hover {
    background-color: #45a049;
  }
  </style>
  