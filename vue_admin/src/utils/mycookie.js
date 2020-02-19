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
/**
 * AES加密
 * @param {*} c_password 前端传来的需要加密的明文
 */
import CryptoJS from 'crypto-js'
import c_key from '../main'
export function AESEncrypt(c_password){
  
  var encrypt=CryptoJS.AES.encrypt(c_password,CryptoJS.enc.Utf8.parse(c_key),{
     mode: CryptoJS.mode.ECB,
     padding: CryptoJS.pad.Pkcs7
  }).toString();
  console.log('encrypt:',encrypt)
return encrypt
}
/**
 * AES解密
 * @param {*} c_cipher 密文
 */
export function AESDecrypt(c_cipher) {
  var decrypt=CryptoJS.AES.decrypt(c_cipher, CryptoJS.enc.Utf8.parse(c_key), {
    mode: CryptoJS.mode.ECB,
    padding: CryptoJS.pad.Pkcs7
  }).toString(CryptoJS.enc.Utf8);// 必须要是utf8
  console.log('decrypt:',decrypt)
  return decrypt
}

/**
 * 设置本地的localstorage键值
 * @param {string} key 需要存本地localstorage的键名
 * @param {string} value 需要本地存的localstorage的key对应的值
 * @param {number} expire 以小时为单位的存活期
 */
export function setStorageExpire(key, value, expire) {
  const obj = {
    data: value,
    time: Date.now(),
    expire: 1000 * 60 * 60 * expire  // 1 hour*expire
  }
  localStorage.setItem(key, JSON.stringify(obj))
}
/**
 * 根据key提取本地localstorage的值，过期会返回null
 * @param {string} key 需要取本地localstorage的键名
 */
export function getStorageExpire(key) {
  const value = localStorage.getItem(key) // value是一个json对象，里面保存了data,time,expire属性
  if (value != null) {
    var obj = JSON.parse(value)
    const timespan = new Date().getTime() - obj.time
    // 保存时间过久
    if (timespan > obj.expire) {
      localStorage.removeItem(key)
      return null
    } else {
      return obj.data
    }
    // 本地没有这个值
  } else {
    return null
  }
}