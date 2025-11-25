# Sanic框架Demo
Sanic 版本为最新版本 23.3.0, Python版本为3.9。
此Demo包含mysql、redis、arq等配置。
Sanic最新版本变化有点大,此Demo只适用与23.3.0,若安装的是其他的版本，会有很多稀奇古怪的问题。
## 安装
pip install -r requirements.txt
## 使用
### 使用前要安装redis和mysql并设置密码
redis配置和数据库配置在settings.py,可根据需求自行配置
### Windows、Linux、MacOS
python server.py
### Linux、MacOS
python start_loop.py
注：windows不支持uvloop启动
