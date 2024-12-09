import { createRouter, createWebHistory } from 'vue-router'

import LayoutPage from '../components/LayoutPage.vue'; // 引入布局组件

import HomePage from '../views/HomePage.vue'
import RecordPage from '../views/RecordPage.vue'
import ShowAll from '../views/ShowAll.vue'
import MyPage from '../views/MyPage.vue'
import EditMy from '../views/EditMy.vue'

import LoginPage from '../views/LoginPage.vue'; // 引入登录页面
import RegisterPage from '../views/RegisterPage.vue'; // 引入注册页面

// 路由配置
const routes = [
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage,
    // meta: { requiresAuth: false }  // 登录页不需要认证
  },
  {
    path: '/register',
    name: 'RegisterPage',
    component: RegisterPage,
    // meta: { requiresAuth: false }  // 注册页不需要认证
  },
  {
    path: '/',
    redirect: '/home',  // 默认重定向到 /homege
  },
  {
    path: '/home',
    name: 'HomePage',
    component: LayoutPage,  // 使用 Layout 组件作为父组件
    children: [
      {
        path: '',
        name: 'HomePage',
        component: HomePage, // 显示 HomePage 组件
        // meta: { requiresAuth: true }  // 需要认证才能访问
      }
    ]
  },
  {
    path: '/record',
    name: 'RecordPage',
    component: LayoutPage,  // 使用 Layout 组件作为父组件
    children: [
      {
        path: '',
        name: 'RecordPage',
        component: RecordPage,  // 显示 RecordPage 组件
        // meta: { requiresAuth: true }  // 需要认证才能访问
      }
    ]
  },
  {
    path: '/show',
    name: 'ShowAll',
    component: LayoutPage,  // 使用 Layout 组件作为父组件
    children: [
      {
        path: '',
        name: 'ShowAll',
        component: ShowAll,  // 显示 ShowAll 组件
        // meta: { requiresAuth: true }  // 需要认证才能访问
      }
    ]
  },
  {
    path: '/my',
    name: 'MyPage',
    component: LayoutPage,  // 使用 Layout 组件作为父组件
    children: [
      {
        path: '',
        name: 'MyPage',
        component: MyPage,  // 显示 MyPage 组件
        // meta: { requiresAuth: true }  // 需要认证才能访问
      }
    ]
  },
  {
    path: '/editmy',
    name: 'EditMy',
    component: EditMy,
    // meta: { requiresAuth: true }  // 需要认证才能访问
  }
];

// 创建路由实例
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL), // 使用 HTML5 history 模式
  routes // 路由配置
});

// 路由守卫
router.beforeEach((to, from, next) => {
  // 假设通过 localStorage 判断用户是否已登录
  const isAuthenticated = localStorage.getItem('isAuthenticated');

  if (to.matched.some(record => record.meta.requiresAuth)) {
    // 如果目标页面需要认证且用户未登录
    if (!isAuthenticated) {
      // 未登录，重定向到登录页面
      next({ name: 'LoginPage' });
    } else {
      // 已登录，继续访问目标页面
      next();
    }
  } else {
    // 不需要认证的页面，直接访问
    next();
  }
});

// 创建登录方法：登录成功后存储认证状态
// function handleLogin() {
//   // 假设登录验证通过，存储认证状态
//   localStorage.setItem('isAuthenticated', 'true');  // 认证状态存储在 localStorage 中
//   this.$router.push('/home');  // 登录成功后跳转到主页
// }

export default router; // 导出路由实例
