/**
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

/** 支持大小写字母，下划线，数字，- _ ? ! * @.的命名
 * @param {string} str
 * @returns {Boolean}
 */
export function validUsername(str) {
  // 支持字母下划线和数字问号感叹号等匹配(mysql "--"加空格会注释，没有空格不会注释。"-- "会注释)
  const reg = /^[a-zA-Z0-9-_?\.@!\*]*$/
  return reg.test(str)
}
