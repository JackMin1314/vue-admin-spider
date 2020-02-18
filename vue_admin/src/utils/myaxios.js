import axios from 'axios'
import qs from 'qs'
import message from 'element-ui'

// function getcsrf() {
//   axios.get('http://127.0.0.1:9999/').then((res) => {
//     if (res.data) {
//       console.log('pre res_data:', res.data)
//       console.log('pre res.header.csrf:', res.headers['csrf_token'])
//       return res.headers['csrf_token']
//     } else {
//       console.log('请求结果为空...')
//     }
//   }).catch(error => { console.log(error) })
// }
// 创建axios实例
var instance = axios.create({
  timeout: 8000,
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest'
  }
})

// 全局axios配置
instance.defaults.timeout = 7000 // 设置默认的超时时间(ms)
// 解决axios自带的option预请求
// post默认请求头添加
instance.defaults.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
instance.defaults.xsrfCookieName = ''
instance.defaults.xsrfHeaderName = ''
// 添加超时访问次数和间隔(ms)
instance.defaults.retry = 2
instance.defaults.retryDelay = 1000
// instance.defaults.withCredentials = true // 设置axios每次请求带上cookies

// 设置请求拦截器,添加请求头和格式化参数等值
instance.interceptors.request.use(
  config => {
    if (config.method === 'post') {
      config.data = qs.stringify(config.data) // POST传参序列化
    }
    config.headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
    return config
  }, error => {
    return Promise.reject(error)
  }
)
// 设置响应拦截器，解决csrf_token过期问题
instance.interceptors.response.use(
  response => {
    // 当请求是400的时候说明csrf_token过期了重新请求添加 
    if (response.status === 400) {
      this.axios.get('/').then(resp => {
        instance.defaults.headers['csrf_token'] = resp.headers['csrf_token']
      }).catch(err => {console.log('响应拦截器get异常:', err)})
      console.log('new csrf_token is:', instance.defaults.headers['csrf_token'])
    }
    else {
      return Promise.resolve(response)
    }
  }, error => {
    console.log('响应拦截异常:',error)
    return Promise.reject(error)
  }
)

export default instance

export function responsetips(resp) {
  var codetype = ''
  switch (resp.data.code) {
    case '0':
      codetype = 'success'
      break
    case '-1':
      codetype = 'error'
      break
    case '1':
      codetype = 'warning'
      break
    default:
      break
  }
  // 引用element-ui的Message方法
  message.Message({
    showClose: true,
    message: resp.data.msg,
    type: codetype,
    duration: 2500
  })
}
