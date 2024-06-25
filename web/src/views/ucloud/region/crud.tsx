import * as api from './api';
import {
    dict,
    UserPageQuery,
    AddReq,
    DelReq,
    EditReq,
    compute,
    CreateCrudOptionsProps,
    CreateCrudOptionsRet
} from '@fast-crud/fast-crud';
import {dictionary} from '/@/utils/dictionary';
import {successMessage} from '/@/utils/message';
import {auth} from "/@/utils/authFunction";

export const createCrudOptions = function ({crudExpose}: CreateCrudOptionsProps): CreateCrudOptionsRet {
    const pageRequest = async (query: UserPageQuery) => {
        return await api.GetList(query);
    };
    const editRequest = async ({form, row}: EditReq) => {
        form.id = row.id;
        return await api.UpdateObj(form);
    };
    const delRequest = async ({row}: DelReq) => {
        return await api.DelObj(row.id);
    };
    const addRequest = async ({form}: AddReq) => {
        return await api.AddObj(form);
    };

    /**
     * 懒加载
     * @param row
     * @returns {Promise<unknown>}
     */
    const loadContentMethod = (tree: any, treeNode: any, resolve: Function) => {
        pageRequest({pcode: tree.code}).then((res: APIResponseData) => {
            resolve(res.data);
        });
    };

    return {
        crudOptions: {
            request: {
                pageRequest,
                addRequest,
                editRequest,
                delRequest,
            },
            actionbar: {
                buttons: {
                    add: {
                        show: auth('region:Create'),
                    }
                }
            },
            rowHandle: {
                //固定右侧
                fixed: 'right',
                width: 200,
                buttons: {
                    view: {
                        show: false,
                    },
                    edit: {
                        iconRight: 'Edit',
                        type: 'text',
						show: auth('region:Update')
                    },
                    remove: {
                        iconRight: 'Delete',
                        type: 'text',
						show: auth('region:Delete')
                    },
                },
            },
            pagination: {
                show: false,
            },
            table: {
                rowKey: 'id',
                lazy: true,
                load: loadContentMethod,
                treeProps: {children: 'children', hasChildren: 'hasChild'},
            },
            columns: {
                _index: {
                    title: '序号',
                    form: {show: false},
                    column: {
                        type: 'index',
                        align: 'center',
                        width: '70px',
                        columnSetDisabled: true, //禁止在列设置中选择
                    },
                },
                name: {
                    title: '名称',
                    search: {
                        show: true,
                    },
                    treeNode: true,
                    type: 'input',
                    column: {
                        minWidth: 120,
                    },
                    form: {
                        rules: [
                            // 表单校验规则
                            {required: true, message: '名称必填项'},
                        ],
                        component: {
                            placeholder: '请输入名称',
                        },
                    },
                },
                code: {
                    title: '地区编码',
                    search: {
                        show: true,
                    },
                    type: 'input',
                    column: {
                        minWidth: 90,
                    },
                    form: {
                        rules: [
                            // 表单校验规则
                            {required: true, message: '地区编码必填项'},
                        ],
                        component: {
                            placeholder: '请输入地区编码',
                        },
                    },
                },
            },
        },
    };
};
