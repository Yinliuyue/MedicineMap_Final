<template>
  <div class="user-center">
    <!-- 页面标题 -->
    <h1>个人中心</h1>

    <!-- 用户信息展示 -->
    <div class="user-info">
      <img :src="user.avatar" alt="User Avatar" class="avatar">
      <div class="user-details">
        <p><strong>用户名：</strong>{{ user.username }}</p>
        <p><strong>邮箱：</strong>{{ user.email }}</p>
        <p><strong>注册时间：</strong>{{ user.registrationDate }}</p>
      </div>
    </div>

    <!-- 修改个人信息按钮 -->
    <div class="actions">
      <button @click="editProfile">修改个人信息</button>
      <button @click="logout">退出登录</button>
    </div>
  </div>
</template>

<script>
  // import axios from 'axios';
  
  export default {
    name: 'MyPage',
    data() {
      return {
        user: {
          avatar: 'https://via.placeholder.com/100',  // 默认头像
          username: '张三',  // 示例用户名
          email: 'zhangsan@example.com',  // 示例邮箱
          registrationDate: '2022-01-01'  // 示例注册时间
        }
      };
    },
    methods: {
      // 修改个人信息
      editProfile() {
        this.$router.push('/edit-my');  // 跳转到修改个人信息页面
      },
      // 退出登录
      logout() {
        // 这里可以调用退出登录的逻辑，如清除用户信息、跳转到登录页等
        this.$router.push('/login');
      }
    }
  };
</script>

<style scoped>
  .user-center {
    text-align: center;
    font-family: Arial, sans-serif;
    margin-top: 50px;
  }

  h1 {
    font-size: 36px;
    color: #4CAF50;
  }

  .user-info {
    margin-top: 30px;
    display: flex;
    justify-content: center;
    align-items: center;
  }

  .avatar {
    border-radius: 50%;
    width: 100px;
    height: 100px;
    margin-right: 20px;
  }

  .user-details p {
    font-size: 18px;
    margin: 5px 0;
  }

  .actions {
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
