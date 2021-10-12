// 跨域代理前缀
const API_PROXY_PREFIX = '/api'
const BASE_URL = process.env.NODE_ENV === 'production' ? process.env.VUE_APP_API_BASE_URL : "http://127.0.0.1:5000"

// const BASE_URL = "http://127.0.0.1:5000"
module.exports = {
    REGISTER_ACCOUNT:BASE_URL+`/company/applyRegister`,
    LOGIN:BASE_URL+`/company/modifyLogin`,
    DEPARTMENT_LIST:`/department/list`,
    DEPARTMENT_UPDATE:`/department/update`,
    DEPARTMENT_DELETE:`/department/delete`,
    DEPARTMENT_ADD:`/department/delete`
  }


  