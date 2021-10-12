import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store/index'
//ajax框架
// import axios from "axios"
// import VueAxios from "vue-axios"
//组件库
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
//Echart制图
import * as echarts from 'echarts';

//全局变量
import constPath from "./assets/js/constPath.js";

//全局样式
import './assets/styles/common.css';
import './assets/styles/protogenetic.css';

//Vue.use(VueAxios,axios);
Vue.use(ElementUI);

Vue.prototype.$echarts = echarts;
Vue.config.productionTip = false;
Vue.prototype.constPath = constPath;

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')
