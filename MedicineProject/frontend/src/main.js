import { createApp } from 'vue'
import App from './App.vue'
import router from './router'; // 引入 router 配置

createApp(App)
  .use(router)
  .mount('#app')
