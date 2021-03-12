import axios from 'axios'
import { Message } from 'element-ui'

// 创建axios实例
const request = axios.create({
  baseURL: process.env.BASE_API, // api的base_url
  timeout: 60000 // 请求超时时间
})

// respone拦截器
request.interceptors.response.use(
  response => {
    const result = response.data
    if (result.code !== 200) {
      console.log('in errors')
      Message({
        message: result.message,
        type: 'error',
        duration: 5 * 1000
      })
      return Promise.reject('error')
    } else {
      return result
    }
  },
  error => {
    console.log('err' + error)// for debug
    Message({
      message: '请求出错！',
      type: 'error',
      duration: 5 * 1000
    })
    return Promise.reject(error)
  }
)

export function login(username, password) {
  return request({
    url: '/user/login',
    method: 'post',
    data: {
      username,
      password
    }
  })
}

export function remote(url, params) {
  return request({ url: url, method: 'post', data: params })
}

export function uploadFile(url, file) {
  var fileData = new FormData()
  fileData.append('file', file)
  return request({ url: url, method: 'post', data: fileData })
}

export const log_labels = {
  code: '序号',
  stype: '卫星型号',
  device: '所属单机',
  exception: '异常类型',
  system: '所属分系统',
  description: '异常现象描述',
  occurred: '发生时间',
  classify: '异常种类',
  env_related: '与环境是否有关',
  year: '年份',
  month: '月份',
  day: '日期',
  hour: '小时',
  fmonth: '年月',
  fday: '年月日',
  fhour: '年月日时'
}
