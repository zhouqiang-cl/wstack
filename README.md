
#此系统包括两个部分:

##1. 物理装机系统, 基于 racadm + pxe + ks, 目前只针对 DELL 机器.

<br/>

pm 目录下是物理装机系统的代码, 只提供 API, 目前有三个功能:
   
```
1). 装机检查, 检查机器是否可以正常安装机器;
   
2). 自动安装, 全自动安装, 调用 API 即可, 不需要人为干预;
   
3). 手动安装, 调用 API 后需要人为控制机器进入 PXE 模式方可安装.
   
```

几点:
   
```
1). 机器 hostname 和 ip 会从资产系统自动获取, 由装机之后的 %post 脚本实现, 先从 /api/v1/pm/message 获取 sn 的 usage, 作为申请主机名的 key, 根据装机时刻 DHCP 拿到的内网网段作为申请 ip 的 key, hostname 和 ip 都申请到之后再通过 /api/v1/pm/message 传回本系统.


2). 调用 API 后, 返回一个安装结果的 API 供查看安装状况;

   
3). 提供装机之后的 user-data 功能, 用于装机之后执行自定义脚本.
```



<br/><br/>

##2. 虚拟机系统.

<br/>

vmmaster 是虚拟机系统的 master 代码;

vmagent 是跑在每台宿主机上的代码, 这部分代码完全独立, 可独立部署.

另外, libs 目录存放一些公共的库和工具.



<br/><br/>

##3. 部署.

<br/>
使用 circus 部署，实现发布过程不影响当前请求。

