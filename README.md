# 小爱同学控制电脑开机

利用接入米家第三方平台(巴法平台开放的MQTT接口)，将 xiaoai-wol 部署到PVE/NAS/软路由等，通过小爱同学操作电脑开机。  
在 Docker 中部署运行 xiaoai-wol。 部署前请确认已经安装了 Docker Engine 或者 Docker Desktop。

## 食用方法
### 创建数据和配置文件夹
```mkdir -p ${HOME}/xiaoai-wol/data```  

### 使用 Docker 部署 AutoBangumi
- 复制以下命令运行即可。  
```shell
docker run -d \
  --name=xiaoai-wol \
  -v ${HOME}/xiaoai-wol/data:/app/data \
  -p 5835:5835 \
  -e TZ=Asia/Shanghai \
  -e PUID=$(id -u) \
  -e PGID=$(id -g) \
  -e UMASK=022 \
  --network=host \
  --restart unless-stopped \
  akihiro0723/xiaoai-wol:latest
```
### 注册巴法平台
- 待完善

### 配置小爱同学
- 待完善

### 配置 xiaoai-wol
安装好 xiaoai-wol 之后，xiaoai-wol 的 WebUI 会自动运行，但是主程序会处于暂停状态，可以进入 http://ip:5835 进行配置。



## TODO
- [ ] 支持点灯科技平台


## 参考

[Wake-On-Lan-Python](https://github.com/bentasker/Wake-On-Lan-Python),
[EthanHome-WOL](https://github.com/cgy233/EthanHome-WOL)