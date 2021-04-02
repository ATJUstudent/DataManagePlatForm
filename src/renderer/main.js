import Vue from 'vue'
import axios from 'axios'

import App from './App'
import router from './router'
import store from './store'

import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
Vue.use(ElementUI)

//导入样式表
import './styles/global.css'

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
axios.defaults.baseURL = 'http://127.0.0.1:8080'
Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false

import echarts from 'echarts'
Vue.prototype.$echarts = echarts

import JsonExcel from 'vue-json-excel'

Vue.component('downloadExcel', JsonExcel)


/* eslint-disable no-new */
new Vue({
  components: { App },
  router,
  store,
  template: '<App/>'
}).$mount('#app')
