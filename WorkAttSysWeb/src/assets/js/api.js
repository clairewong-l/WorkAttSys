//业务数据请求,指定接口地址
import {get,post} from "./axiosDelegate"

//详细请求参数、返回数据格式请查看接口文档
//验证注册
export const applyRegister = (params)=>post('applyRegister.json',params);
//验证登录
export const modifyLogin = (params)=>post('modifyLogin',params);

//获取员工最新出勤动态
export const getStaffNews = (params) =>get('getStaffNews',params);

//获取所有部门类别
export const getDepartmentName = (params) =>get('getDepartmentName',params);

//获取公告 最新公告、所有公告
export const getNewNotice = (params) =>get('getNewNotice',params);
//发布公告
export const addNotice = (params) =>post('addNotice',params);
//export const addNotice = (params) =>get('addNotice.json',params);
//修改公告
export const updateNotice = (params) =>post('updateNotice',params);
//export const updateNotice = (params) =>get('common.json',params);
//删除公告
export const deleteNotice = (params) =>get('deleteNotice',params);
//export const deleteNotice = (params) =>get('common.json',params);

//获取指定日期公司所有员工的异常出勤记录
export const getExRecordMsg = (params)=>get('getExRecordMsg',params);

//获取公司所有待处理的申请信息
export const getApplicationMsg = (params)=>get('getApplicationMsg',params);
//审批申请信息
export const disposeApplicationMsg = (params)=>post('disposeApplicationMsg',params);
//export const disposeApplicationMsg = (params)=>get('common.json',params);

//获取指定月份的员工打卡记录统计
export const getAllAttRecord = (params)=>get('getAllAttRecord',params);

//获取公司所有员工信息
export const getStaff = (params) =>post('getStaff',params);

//修改员工信息
export const updateStaff = (params)=>post('updateStaff',params);

//删除员工信息
export const deleteStaff = (params)=>post('deleteStaff',params);

//新增员工信息
export const addStaff = (params)=>post('addStaff',params);

//获取部门最新信息
export const getDepartment = (params)=>post('getDepartment',params);

//修改部门信息
export const updateDepartment = (params)=>post('updateDepartment',params);

//删除部门信息
export const deleteDepartment = (params)=>post('deleteDepartment',params);

//新增部门信息
export const addDepartment = (params)=>post('addDepartment',params);

//修改公司时间设置信息
export const updateTime = (params)=>post('updateTime',params);

//获取公司时间设置信息
export const getTime = (params)=>post('getTime',params);
