<template>
  <div>
    <!-- 标题 -->
    <div class="title">
      <h1>AI智慧问诊系统</h1>
    </div>

    <!-- 导航栏 -->
    <div class="navbar">
      <router-link to="/home" class="nav-item" active-class="active">问答系统</router-link>
      <router-link to="/record" class="nav-item" active-class="active">分析结果</router-link>
      <router-link to="/show" class="nav-item" active-class="active">知识图谱展示</router-link>
      <!-- <router-link to="/my" class="nav-item" active-class="active">My</router-link> -->
    </div>
  
    <!-- 页面内容展示区 -->
    <div class="content">
      <router-view></router-view> <!-- 显示当前页面的内容 -->
    </div>
  </div>
</template>
  
<script>
  export default {
    name: 'LayoutPage'
  }
</script>
  
<style scoped>
  .navbar {
    background-color: #333;
    padding: 10px;
    text-align: center;
  }
  
  .nav-item {
    color: white;
    text-decoration: none;
    margin: 0 15px;
    font-size: 18px;
    padding: 10px 20px;
    border-radius: 5px;
  }
  
  .nav-item:hover {
    background-color: #575757;
  }
  
  .nav-item.active {
    background-color: #4CAF50;
  }
  
  .content {
    margin-top: 30px;
    text-align: center;
  }
</style>
  