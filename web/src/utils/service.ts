import axios from 'axios';
import { get } from 'lodash-es';
import { ElMessage, ElMessageBox } from 'element-plus'
import type { Action } from 'element-plus'

// @ts-ignore
import { errorLog, errorCreate } from './tools.ts';
// import { env } from "/src/utils/util.env";
// import { useUserStore } from "../store/modules/user";
import { Local, Session } from '/@/utils/storage';
import qs from 'qs';
/**
 * @description 创建请求实例
 */
function createService() {
	// 创建一个 axios 实例
	const service = axios.create({
		timeout: 20000,
		headers: {
			'Content-Type': 'application/json;charset=utf-8'
		},
		paramsSerializer: {
			serialize(params) {
				return qs.stringify(params, {  indices: false,encoder: (val:string) => {
						if (typeof val === 'boolean') {
							return val ? 1 : 0;
						}
						return val;
					} });
			},
		},
	});
	// 请求拦截
	service.interceptors.request.use(
		(config) => config,
		(error) => {
			// 发送失败
			console.log(error);
			return Promise.reject(error);
		}
	);
	// 响应拦截
	service.interceptors.response.use(
		(response) => {
			if (response.config.responseType === 'blob') {
				return response;
			}
			// dataAxios 是 axios 返回数据中的 data
			const dataAxios = response.data;
			// 这个状态码是和后端约定的
			const { code } = dataAxios;
			// swagger判断
			if (dataAxios.swagger != undefined) {
				return dataAxios;
			}
			// 根据 code 进行判断
			if (code === undefined) {
				// 如果没有 code 代表这不是项目后端开发的接口
				errorCreate(`非标准返回：${dataAxios}， ${response.config.url}`, false);
				return dataAxios;
			} else {
				// 有 code 代表这是一个后端接口 可以进行进一步的判断
				switch (code) {
					case 400:
						Local.clear();
						Session.clear();
						errorCreate(`${dataAxios.msg}: ${response.config.url}`);
						window.location.reload();
						break;
					case 401:
						Local.clear();
						Session.clear();
						dataAxios.msg = '登录授权过期，请重新登录';
						ElMessageBox.alert(dataAxios.msg, '提示', {
							confirmButtonText: 'OK',
							callback: (action: Action) => {
								window.location.reload();
							},
						})
						errorCreate(`${dataAxios.msg}: ${response.config.url}`);
						break;
					case 2000:
						// @ts-ignore
						if (response.config.unpack === false) {
							//如果不需要解包
							return dataAxios;
						}
						return dataAxios;
					default:
						// 不是正确的 code
						errorCreate(`${dataAxios.msg}: ${response.config.url}`);
						return dataAxios;
				}
			}
		},
		(error) => {
			const status = get(error, 'response.status');
			switch (status) {
				case 400:
					error.message = '请求错误';
					break;
				case 401:
					error.message = '未授权，请登录';
					break;
				case 403:
					error.message = '拒绝访问';
					break;
				case 404:
					error.message = `请求地址出错: ${error.response.config.url}`;
					break;
				case 408:
					error.message = '请求超时';
					break;
				case 500:
					error.message = '服务器内部错误';
					break;
				case 501:
					error.message = '服务未实现';
					break;
				case 502:
					error.message = '网关错误';
					break;
				case 503:
					error.message = '服务不可用';
					break;
				case 504:
					error.message = '网关超时';
					break;
				case 505:
					error.message = 'HTTP版本不受支持';
					break;
				default:
					break;
			}
			errorLog(error);
			if (status === 401) {
				// const userStore = useUserStore();
				// userStore.logout();
			}
			return Promise.reject(error);
		}
	);
	return service;
}

/**
 * @description 创建请求方法
 * @param {Object} service axios 实例
 */
function createRequestFunction(service: any) {
	return function (config: any) {
		const configDefault = {
			headers: {
				'Content-Type': get(config, 'headers.Content-Type', 'application/json'),
			},
			timeout: 5000,
			baseURL: import.meta.env.VITE_API_URL as any,
			data: {},
		};

		// const token = userStore.getToken;
		const token = Session.get('token');
		if (token != null) {
			// @ts-ignore
			configDefault.headers.Authorization = 'JWT ' + token;
		}
		return service(Object.assign(configDefault, config));
	};
}

// 用于真实网络请求的实例和请求方法
export const service = createService();
export const request = createRequestFunction(service);

// 用于模拟网络请求的实例和请求方法
export const serviceForMock = createService();
export const requestForMock = createRequestFunction(serviceForMock);
