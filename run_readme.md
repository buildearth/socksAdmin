# 资料

代码：

https://github.com/buildearth/socksAdmin/tree/master

资料

https://docs.dvcloud.xin/

# 开始

## 后端项目本地运行

1. 进入项目目录 cd backend
2. 在项目根目录中，复制 ./conf/env.example.py 文件为一份新的到 ./conf 文件夹下，并重命名为 env.py
3. 在 env.py 中配置数据库信息
	mysql数据库版本建议：8.0
	mysql数据库字符集：utf8mb4
4. 安装依赖环境
	pip3 install -r requirements.txt
5. 执行迁移命令：
	python3 manage.py makemigrations
	python3 manage.py migrate
6. 初始化数据
	python3 manage.py init
7. 初始化省市县数据:
	python3 manage.py init_area
8. 启动项目
	python3 manage.py runserver 0.0.0.0:8000
  或使用 uvicorn :
    uvicorn application.asgi:application --port 8000 --host 0.0.0.0 --workers 8

建议一开始就使用mysql，因为后端写好后，前端要动态配置路由，存储在表中。



## 前端项目运行

npm install 

启动服务

npm run dev



本地端口修改位置`web/.env.development`

```
# 本地环境
ENV = 'development'

# 本地环境接口地址
VITE_API_URL = 'http://127.0.0.1:9000'

# 是否启用按钮权限
VITE_PM_ENABLED = true
```



# 新增app

## 后端

在`dvadmin`目录下新加`ucloud`目录，新增app。

```
python manage.py makemigrations ucloud
python manage.py migrate ucloud
```

# 前端

在src/views下新加文件夹`ucloud`作为新模块。

子文件夹细分模块。

编写完成后，需要在菜单中增加对于内容。