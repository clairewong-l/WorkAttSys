import axios from 'axios'
// import Cookie from 'js-cookie'

// 跨域认证信息 header 名
export const xsrfHeaderName = 'access-token'
export const refreshToken = 'RefreshToken'
// const xsrfHeaderNameTimeout = 30 * 60 * 1000
// const refreshTokenTimeout = 30 * 24 * 60 * 60 * 1000

axios.defaults.timeout = 5000
axios.defaults.withCredentials = false
axios.defaults.xsrfHeaderName = xsrfHeaderName
axios.defaults.xsrfCookieName = xsrfHeaderName

// http method
const METHOD = {
  GET: 'get',
  POST: 'post',
}


/**
 * axios请求
 * @param url 请求地址
 * @param method {METHOD} http method
 * @param params 请求参数
 * @returns {Promise<AxiosResponse<T>>}
 */
async function request(url, method, params, config = {}) {
  switch (method) {
    case METHOD.GET:
      return axios.get(url, { params, ...config })
    case METHOD.POST:
      return axios.post(url, params, config)
    default:
      return axios.get(url, { params, ...config })
  }
}

/**
 * 解析 url 中的参数
 * @param url
 * @returns {Object}
 */
function parseUrlParams(url) {
  const params = {}
  if (!url || url === '' || typeof url !== 'string') {
    return params
  }
  const paramsStr = url.split('?')[1]
  if (!paramsStr) {
    return params
  }
  const paramsArr = paramsStr.replace(/&|=/g, ' ').split(' ')
  for (let i = 0; i < paramsArr.length / 2; i++) {
    const value = paramsArr[i * 2 + 1]
    params[paramsArr[i * 2]] = value === 'true' ? true : value === 'false' ? false : value
  }
  return params
}

export { METHOD, request ,parseUrlParams }
