<template>
  <div class="register-page">
    <h1>注册</h1>
    <form @submit.prevent="handleRegister">
      <div class="input-group">
        <label for="username">用户名</label>
        <input type="text" v-model="username" id="username" required />
      </div>
      <div class="input-group">
        <label for="password">密码</label>
        <input type="password" v-model="password" id="password" required />
      </div>
      <div class="input-group">
        <label for="confirmPassword">确认密码</label>
        <input type="password" v-model="confirmPassword" id="confirmPassword" required />
      </div>
      <button type="submit">注册</button>
    </form>
    <p>
      已有账户？<router-link to="/login">登录</router-link>
    </p>
  </div>
</template>
  
<script>
  export default {
    name: 'register-page',
    data() {
      return {
        username: '',
        password: '',
        confirmPassword: ''
      };
    },
    methods: {
      handleRegister() {
        if (this.password !== this.confirmPassword) {
          alert('两次密码不一致');
          return;
        }
        // 这里可以添加注册逻辑，比如调用 API 创建账户
        console.log('注册中...', this.username, this.password);
        // 注册成功后，跳转到登录页面
        this.$router.push('/login');
      }
    }
  };
</script>
  
<style scoped>
  /* 你可以根据需要为这个组件写样式 */
  .register {
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
</style>
  