import { REGISTER_ACCOUNT, LOGIN, DEPARTMENT_LIST ,DEPARTMENT_UPDATE,DEPARTMENT_DELETE,DEPARTMENT_ADD} from './config'
import { request } from './request'
export async function register(params) {
    const { cardId,
        name,
        pass,
        phone,
        companyName,
        companyManager
    } = params
    return request(REGISTER_ACCOUNT, 'post', {
        id: cardId,
        name,
        pwd: pass,
        phone,
        legal_person: companyManager,
        company_name: companyName
    })
}




export async function login(params) {
    return request(LOGIN, 'post', params)
}
export async function getDepartment(params) {
    return request(DEPARTMENT_LIST, 'post',params)
}
export async function updateDepartment(params) {
    return request(DEPARTMENT_UPDATE, 'post',params)
}
export async function deleteDepartment(params) {
    return request(DEPARTMENT_DELETE, 'post',params)
}
export async function addDepartment(params) {
    return request(DEPARTMENT_ADD, 'post',params)
}

