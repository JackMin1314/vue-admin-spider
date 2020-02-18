import Vue from 'vue'

import 'normalize.css/normalize.css' // A modern alternative to CSS resets

// 导入星空特效
import VueParticles from 'vue-particles'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// import locale from 'element-ui/lib/locale/lang/en' // lang i18n

import '@/styles/index.scss' // global css

import App from './App'
import store from './store'
import router from './router'
import '@/icons' // icon
import '@/permission' // permission control

/**
 * If you don't want to use mock-server
 * you want to use MockJs for mock api
 * you can execute: mockXHR()
 *
 * Currently MockJs will be used in the production environment,
 * please remove it before going online ! ! !
 */
// if (process.env.NODE_ENV === 'production') {
//   const { mockXHR } = require('../mock')
//   mockXHR()
// }

// 使用第三方login的星座连线
Vue.use(VueParticles)

// 导入自己封装的axios
import instance from './utils/myaxios'

// 使用axios
instance.defaults.baseURL = '/api' // 默认每次请求都会自动在前面加上/api
instance.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
Vue.use(instance)
// 这里申明一个全局，接下来配置/config/index.js设置下请求地址和跨域等
Vue.prototype.$axios = instance
// axios.defaults.withCredentials = true // 设置axios每次请求带上cookies

// set ElementUI lang to EN
// Vue.use(ElementUI, { locale })
// 如果想要中文版 element-ui，按如下方式声明
Vue.use(ElementUI)

Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App)
})
// 配置AES密钥必须8/16/32位
var c_key="10209999"
export default c_key
// var service = axios.create({
// })
// // 请求拦截
// axios.interceptors.request.use(config => {
//   if (config.method === 'get') {
//     config.params = { ...config.params, ...config.data }
//   } else if (config.method === 'jsonp') {
//     config.headers = {
//       'X-Requested-With': 'XMLHttpRequest',
//       'Content-Type': 'application/json; charset=UTF-8',
//       'Access-Control-Allow-Origin': '*'
//     }
//     config.method = 'get'
//     config.params = { ...config.params, ...config.data }
//   } else {
//     if (config.data) {
//       const data = config.data
//       console.log(data)
//       config.data = qs(data)
//     }
//   }
//   return config
// }, function(error) {
//   return Promise.reject(error)
// })
// export default service
