/**
 * 设置cookies
 * @param {*} c_name cookie名字
 * @param {*} value  cookie名字对应值
 */
export function setCookie(c_name, value) {
  document.cookie = c_name + '=' + escape(value) + ';'
  // console.log(document.cookie)
}
/**
 * 获取cookies
 * @param {*} c_name 获取的cookie名字
 * @returns 返回的是str值或者空字符
 */
export function getCookie(c_name) {
  if (document.cookie.length > 0) {
    let c_start = document.cookie.indexOf(c_name + '=')
    if (c_start !== -1) {
      c_start = c_start + c_name.length + 1
      let c_end = document.cookie.indexOf(';', c_start)
      if (c_end === -1) c_end = document.cookie.length
      return unescape(document.cookie.substring(c_start, c_end))
    }
  }
  return ''
}
 // 前端加密算法
export function name(params) {
  
}