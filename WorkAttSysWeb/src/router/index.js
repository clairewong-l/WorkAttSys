import Vue from 'vue'
import VueRouter from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import MainPage from '../views/MainPage.vue'
import ManagerPage from '../views/ManagerPage.vue'
import MessagePage from '../views/MessagePage.vue'
import RecordPage from '../views/RecordPage.vue'
import store from "../store/index"
Vue.use(VueRouter)

const routes = [
  {
    path:'/',
    name: 'Login',
    component: Login
  },
  {
    path: '/Register',
    name: 'Register',
    component: Register
  },
  {
    path: '/MainPage',
    name: 'MainPage',
    component: MainPage,
    meta: {
      loginRequire: true
    }
  },
  {
    path: '/ManagerPage',
    name: 'ManagerPage',
    component: ManagerPage,
    meta: {
      loginRequire: true
    }
  },
  {
    path: '/MessagePage',
    name: 'MessagePage',
    component: MessagePage,
    meta: {
      loginRequire: true
    }
  },
  {
    path: '/RecordPage',
    name: 'RecordPage',
    component: RecordPage,
    meta: {
      loginRequire: true
    }
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

// 路由登录拦截
router.beforeEach((to, from, next) => {
  // 要不要对meta.loginRequire属性做监控拦截
  if (to.matched.some(function (item) {
    console.log(item, "是否需要登录校验：", item.meta.loginRequire);
    return item.meta.loginRequire;
  })) {
    const user = store.getters.companyName;
    console.log(user)
    if (user == null) {
      console.log("用户未登录！");
      next('/');
    } else {
      next();
    }
  } else {
    next();
  }
});

export default router
