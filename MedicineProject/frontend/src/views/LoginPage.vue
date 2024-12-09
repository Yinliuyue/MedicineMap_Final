<template>
  <div class="login-page">
    <h1>登录</h1>
    <form @submit.prevent="handleLogin">
      <div class="input-group">
        <label for="username">用户名</label>
        <input type="text" v-model="username" id="username" required />
      </div>
      <div class="input-group">
        <label for="password">密码</label>
        <input type="password" v-model="password" id="password" required />
      </div>
      <button type="submit">登录</button>
    </form>
    <p>
      没有账户？<router-link to="/register">注册</router-link>
    </p>
  </div>
</template>

<script>
export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: ''
    };
  },
  // methods: {
  //   handleLogin() {
  //     // 登录逻辑，这里只是一个模拟
  //     console.log('登录中...', this.username, this.password);
      
  //     // 假设登录成功，跳转到主页
  //     this.$router.push('/');
  //   }
  // },
  created() {
    // 页面加载时自动触发登录操作或其他初始化逻辑
    console.log("登录页面已加载");
  }
};
</script>

<style scoped>
.login-page {
  width: 300px;
  margin: 0 auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.input-group {
  margin-bottom: 15px;
}

input {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
