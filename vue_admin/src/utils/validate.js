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

/** 针对IT之家的文章url设计正则;通过,返回字符串，没通过返回“”
 * 
 * @param {string} str
 * @returns {string} 
 */
export function validIthomeURL(str) {
  // for PC
  const regx1 = new RegExp(
    "^(https://www\.)([a-z]*\.com)?/(([0-9]*/){2,})([0-9]*\.)?htm"
  );
  // for phone
  const regx2 = new RegExp("^(https://m\.)[a-z]*(\.com/)[a-z]*(/[0-9]*\.)?htm");
  if (regx1.test(str)) {
    return str.match(regx1)[0];
  } else if (regx2.test(str)) {
    return str.match(regx2)[0];
  }
  return "";
}
