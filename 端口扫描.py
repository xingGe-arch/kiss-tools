import socket
import threading
import re
import requests
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
ip = input('请输入ip地址或域名：')
thread_num = int(input('请输入线程数：'))
print('\033[31m[*]\033[0m当前默认进程为top1000')
lock = threading.Lock()
port_list_used = set()
def port_scan():
    server_list = '''
0 端口：无效端口,通常用于分析操作系统
1 端口：传输控制协议端口服务多路开关选择器
2 端口：管理实用程序
3 端口：压缩进程
5 端口：远程作业登录
7 端口：回显
9 端口：丢弃
11 端口：在线用户
13 端口：时间
17 端口：每日引用
18 端口：消息发送协议
19 端口：字符发生器
20 端口：FTP 文件传输协议(默认数据口)
21 端口：FTP 文件传输协议(控制)
22 端口：SSH 远程登录协议
23 端口：telnet (终端仿真协议),木马 Tiny Telnet Server 开放此端口
24 端口：预留给个人用邮件系统
25 端口：SMTP 服务器所开放的端口，用于发送邮件
27 端口：NSW 用户系统 FE
29 端口：MSG ICP
31 端口：MSG 验证,木马 Master Paradise、HackersParadise 开放此端口
33 端口：显示支持协议
35 端口：预留给个人打印机服务
37 端口：时间
38 端口：路由访问协议
39 端口：资源定位协议
41 端口：图形
42 端口：主机名服务
43 端口：who is 服务
44 端口：MPM(消息处理模块)标志协议
45 端口：消息处理模块
46 端口：消息处理模块(默认发送口)
47 端口：NI FTP
48 端口：数码音频后台服务
49 端口：TACACS 登录主机协议
50 端口：远程邮件检查协议
51 端口：IMP(接口信息处理机)逻辑地址维护
52 端口：施乐网络服务系统时间协议
53 端口：dns 域名服务器
54 端口：施乐网络服务系统票据交换
55 端口：ISI 图形语言
56 端口：施乐网络服务系统验证
57 端口：预留个人用终端访问
58 端口：施乐网络服务系统邮件
59 端口：预留个人文件服务
60 端口：未定义
61 端口：NI 邮件
62 端口：异步通讯适配器服务
63 端口：whois++
64 端口：通讯接口
65 端口：TACACS 数据库服务
66 端口：Oracle SQL *NET
67 端口：引导程序协议服务端
68 端口：引导程序协议客户端
69 端口：小型文件传输协议
70 端口：信息检索协议
71 端口：远程作业服务
72 端口：远程作业服务
73 端口：远程作业服务
74 端口：远程作业服务
75 端口：预留给个人拨出服务
76 端口：分布式外部对象存储
77 端口：预留给个人远程作业输入服务
78 端口：修正 TCP
79 端口：查询远程主机在线用户等信息
80 端口：http,用于网页浏览,木马 Executor 开放此端口
81 端口：HOST2 名称服务
82 端口：传输实用程序
83 端口：模块化智能终端 ML 设备
84 端口：公用追踪设备
85 端口：模块化智能终端 ML 设备
86 端口：Micro Focus Cobol 编程语言
87 端口：预留给个人终端连接
88 端口：Kerberros 安全认证系统
89 端口：SU/MIT  telnet(终端仿真网关)
90 端口：DNSIX 安全属性标记图
91 端口：MIT Dover 假脱机
92 端口：网络打印协议
93 端口：设备控制协议
94 端口：Tivoli 对象调度
96 端口：DIXIE 协议规范
97 端口：快速远程虚拟文件协议
98 端口：TAC 新闻协议
99 端口：后门程序 ncx99 开放此端口
100 端口：未知用途
101 端口：NIC 主机名称服务
102 端口：消息传输代理
103 端口：Genesis 点对点传输网络
105 端口：信箱名称服务
106 端口：3COM-TSMUX 开放端口
107 端口：远程 Telnet 服务
108 端口：SNA 网关访问服务
109 端口：POP2 服务器开放此端口,用于接收邮件
110 端口：POP3 服务器开放此端口,用于接收邮件
111 端口：SUN 公司的 RPC 服务所有端口
112 端口：McIDAS 数据传输协议
113 端口：认证服务，用于鉴别 TCP 连接的用户
114 端口：音频新闻多点服务
115 端口：简单文件传输服务
116 端口：ANSA REX 通知
117 端口：UUCP 路径服务
118 端口：SQL 服务
119 端口：NEWS 新闻组传输协议，承载 USENET 通信
121 端口：木马 BO jammerkillahV 开放端口
122 端口：SMAKY 网络
123 端口：网络时间协议，蠕虫病毒会利用，一般关闭
128 端口：GSS X 许可认证
129 端口：密码生成器协议
130 端口：Cisco 软件开放端口
131 端口：Cisco 软件开放端口
132 端口：Cisco 软件开放端口
133 端口：统计服务
134 端口：INGRES-网络服务
135 端口：DCOM 服务，冲击波病毒利用，不能关闭
136 端口：命名系统
137 端口：NETBIOS 协议应用，为共享开放
138 端口：NETBIOS 协议应用，为共享开放
139 端口：NETBIOS 协议应用，为共享开放
140 端口：EMFIS 数据服务
141 端口：EMFIS 控制服务
143 端口：Interim 邮件访问协议
144 端口：UMA 软件开放端口
145 端口：UAAC 协议
149 端口：AED 512 仿真服务
150 端口：SQL(结构化查询语言)-网络
152 端口：后台文件传输协议
156 端口：SQL(结构化查询语言)服务
158 端口：PC 邮件服务器
159 端口：NSS-路由
160 端口：SGMP-陷阱
161 端口：简单网络管理协议
162 端口：SNMP 陷阱
163 端口：CMIP/TCP 管理
164 端口：CMIP/TCP 代理
166 端口：Sirius 系统
169 端口：发送
170 端口：网络附言
177 端口：x 显示管理控制协议，入侵者通过它访问 X-windows 操作台
178 端口：NextStep Window 服务
179 端口：边界网关协议
180 端口：图表
181 端口：统一
184 端口：OC 服务器
185 端口：远程-KIS
186 端口：KIS 协议
187 端口：应用通信接口
189 端口：队列文件传输
190 端口：网关进入控制协议
191 端口：Prospero 目录服务
192 端口：OSU 网络监视系统
193 端口：Spider 远程控制协议
194 端口：多线交谈协议
197 端口：目录地址服务
198 端口：目录地址服务监视器
200 端口：IBM 系统资源控制器
201 端口：AppleTalk(Mac  机所用的网络协议)路由保证
202 端口：AppleTalk(Mac 机所用的网络协议 )Name Binding
203 端口：AppleTalk(Mac 机所用的网络协议)未用端口
204 端口：AppleTalk(Mac 机所用的网络协议)回显
205 端口：AppleTalk(Mac 机所用的网络协议)未用端口
206 端口：AppleTalk(Mac 机所用的网络协议)区信息
207 端口：AppleTalk(Mac 机所用的网络协议)未用端口
208 端口：AppleTalk(Mac 机所用的网络协议)未用端口
209 端口：快速邮件传输协议
210 端口：ANSI(美国国家标准协会)Z39.50
211 端口：Texas Instruments 914C/G 终端
213 端口：IPX(以太网所用的协议)
218 端口：Netix 消息记录协议
219 端口：Unisys ARPs
220 端口：交互邮件访问协议 v3
223 端口：证书分发中心
224 端口：masq 拨号器
241 端口：预留端口 (224-241)
245 端口：链接
246 端口：显示系统协议
257 端口：安全电子交易系统
258 端口：Yak Winsock 个人聊天
259 端口：有效短程遥控
260 端口：开放端口
261 端口：IIOP 基于 TLS/SSL 的命名服务
266 端口：SCSI(小型计算机系统接口)on ST
267 端口：Tobit David 服务层
268 端口：Tobit David 复制
281 端口：个人连结
282 端口：Cable 端口 A/X
286 端口：FXP 通信
308 端口：Novastor 备份
313 端口：Magenta 逻辑
318 端口：PKIX 时间标记
333 端口：Texar 安全端口
344 端口：Prospero 数据存取协议
345 端口：Perf 分析工作台
346 端口：Zebra 服务器
347 端口：Fatmen 服务器
348 端口：Cabletron 管理协议
358 端口：Shrink 可上网家电协议
359 端口：网络安全风险管理协议
362 端口：SRS 发送
363 端口：RSVP 隧道
372 端口：列表处理
373 端口：Legend 公司
374 端口：Legend 公司
376 端口：AmigaEnvoy 网络查询协议
377 端口：NEC 公司
378 端口：NEC 公司
379 端口：TIA/EIA/IS-99 调制解调器客户端
380 端口：TIA/EIA/IS-99 调制解调器服务器
381 端口：hp(惠普)性能数据收集器
382 端口：hp(惠普)性能数据控制节点
383 端口：hp(惠普)性能数据警报管理
384 端口：远程网络服务器系统
385 端口：IBM 应用程序
386 端口：ASA 信息路由器定义文件.
387 端口：Appletalk 更新路由.
389 端口：轻型目录访问协议
395 端口：网络监视控制协议
396 端口：Novell(美国 Novell 公司)Netware(Novell 公司出的网络操作系统)over IP 
400-499
400 端口：工作站解决方案
401 端口：持续电源
402 端口：Genie 协议
406 端口：交互式邮件支持协议
408 端口：Prospero 资源管理程序
409 端口：Prospero 资源节点管理.
410 端口：DEC(数据设备公司)远程调试协议
411 端口：远程 MT 协议
412 端口：陷阱协定端口
413 端口：存储管理服务协议
414 端口：信息查询
415 端口：B 网络
423 端口：IBM 操作计划和控制开端
424 端口：IBM 操作计划和控制追踪
425 端口：智能计算机辅助设计
427 端口：服务起位置
434 端口：移动 ip 代理
435 端口：移动 ip 管理
443 端口：基于 TLS/SSL 的网页浏览端口，能提供加密和通过安全端口传输的另一种 HTTP
444 端口：简单网络内存分页协议
445 端口：Microsoft-DS，为共享开放，震荡波病毒利用，一般应关闭
446 端口：DDM-远程关系数据库访问
447 端口：DDM-分布式文件管理
448 端口：DDM-使用安全访问远程数据库
456 端口：木马 HACKERS PARADISE 开放此端口
458 端口：apple quick time 软件开放端口
459 端口：ampr-rcmd 命令
464 端口：k 密码服务
469 端口：广播控制协议
470 端口：scx-代理
472 端口：ljk-登陆
481 端口：Ph 服务
487 端口：简单异步文件传输
489 端口：nest-协议
491 端口：go-登陆
499 端口：ISO ILL 协议
500-599
500 端口：Internet 密钥交换，Lsass 开放端口，不能关闭
509 端口：陷阱
510 端口：FirstClass 协议
512 端口：远程进程执行
513 端口：远程登陆
514 端口：cmd 命令
515 端口：spooler
516 端口：可视化数据
518 端口：交谈
519 端口：unix 时间
520 端口：扩展文件名称服务器
525 端口：时间服务
526 端口：新日期
529 端口：在线聊天系统服务
530 端口：远程过程调用
531 端口：聊天
532 端口：读新闻
533 端口：紧急广播端口
534 端口：MegaMedia 管理端
537 端口：网络流媒体协议
542 端口：商业
543 端口：Kerberos(软件)v4/v5
544 端口：krcmd 命令
546 端口：DHCPv6 客户端
547 端口：DHCPv6 服务器
552 端口：设备共享
554 端口：Real Time Stream 控制协议
555 端口：木马 PhAse1.0、Stealth Spy、IniKiller 开放此端口
556 端口：远距离文件服务器
563 端口：基于 TLS/SSL 的网络新闻传输协议
564 端口：plan 9 文件服务
565 端口：whoami 查询
566 端口：streettalk
567 端口：banyan-rpc(远程过程调用)
568 端口：DPA 成员资格
569 端口：MSN 成员资格
570 端口：demon(调试监督程序)
571 端口：udemon(调试监督程序)
572 端口：声纳
573 端口：banyan-贵宾
574 端口：FTP 软件代理系统
581 端口：Bundle Discovery 协议
582 端口：SCC 安全
583 端口：Philips 视频会议
584 端口：密钥服务器
585 端口：IMAP4+SSL (Use 993 instead)
586 端口：密码更改
587 端口：申请
589 端口：Eye 连结
595 端口：CAB 协议
597 端口：PTC 名称服务
598 端口：SCO 网络服务器管理 3
599 端口：Aeolon Core 协议
600-808
600 端口：Sun IPC(进程间通讯)服务器
601 端口：可靠系统登陆服务
604 端口：通道
606 端口：Cray 统一资源管理
608 端口：发送人-传递/提供 文件传输器
609 端口：npmp-陷阱
610 端口：npmp-本地
611 端口：npmp-gui( 图形用户界面)
612 端口：HMMP 指引
613 端口：HMMP 操作
614 端口：SSL(加密套接字协议层)shell(壳)
615 端口：Internet 配置管理
616 端口：SCO(Unix 系统)系统管理服务器
617 端口：SCO 桌面管理服务器
619 端口：Compaq(康柏公司)EVM
620 端口：SCO 服务器管理
623 端口：ASF 远程管理控制协议
624 端口：Crypto 管理
631 端口：IPP (Internet 打印协议)
633 端口：服务更新(Sterling 软件)
637 端口：局域网服务器
641 端口：repcmd 命令
647 端口：DHCP(动态主机配置协议)Failover
648 端口：注册登记协议(RRP)
649 端口：Cadview-3d 软件协议
666 端口：木马 Attack FTP、Satanz Backdoor 开放此端口
808 端口：ccproxy http/gopher/ftp (over http)协议
1001-1290
1001 端口：木马 Silencer，WebEx 开放端口
1011 端口：木马 Doly 开放端口
1024 端口：动态端口的开始,木马 yai 开放端口
1025 端口：inetinfo.exe(互联网信息服务)木马 netspy 开放端口
1026 端口：inetinfo.exe(互联网信息服务)
1027 端口：应用层网关服务
1030 端口：应用层网关服务
1031 端口：BBN IAD
1033 端口：本地网络信息端口
1034 端口：同步通知
1036 端口：安全部分传输协议
1070 端口：木马 Psyber Stream，Streaming Audio 开放端口
1071 端口：网络服务开放端口
1074 端口：网络服务开放端口
1080 端口：Socks 这一协议以通道方式穿过防火墙，允许防火墙后面的人通过一个 IP 地址访问 INTERNET
1110 端口：卡巴斯基反病毒软件开放此端口
1125 端口：卡巴斯基反病毒软件开放此端口
1203 端口：许可证生效端口
1204 端口：登陆请求监听端口
1206 端口：Anthony 数据端口
1222 端口：SNI R&D 网络端口
1233 端口：普遍的附录服务器端口
1234 端口：木马 SubSeven2.0、Ultors Trojan 开放此端口
1243 端口：木马 SubSeven1.0/1.9 开放此端口
1245 端口：木马 Vodoo，GabanBus，NetBus，Vodoo 开放此端口
1273 端口：EMC-网关端口
1289 端口：JWalk 服务器端口
1290 端口：WinJa 服务器端口
1333-1999
1333 端口：密码策略(网络服务)(svchost.exe)
1334 端口：网络服务(svchost.exe)
1335 端口：数字公正协议
1336 端口：即时聊天协议(svchost.exe)
1349 端口：注册网络协议端口
1350 端口：注册网络协议端口
1352 端口：tcp lotusnote lotus note
1371 端口：富士通配置协议端口
1372 端口：富士通配置协议端口
1374 端口：EPI 软件系统端口
1376 端口：IBM 个人-个人软件端口
1377 端口：Cichlid 许可证管理端口
1378 端口：Elan 许可证管理端口
1380 端口：Telesis 网络许可证管理端口
1381 端口：苹果网络许可证管理端口
1386 端口：CheckSum 许可证管理端口
1387 端口：系统开放端口(rundll32.exe)
1388 端口：数据库高速缓存端口
1389 端口：文档管理端口
1390 端口：存储控制器端口
1391 端口：存储器存取服务器端口
1392 端口：打印管理端口
1393 端口：网络登陆服务器端口
1394 端口：网络登陆客户端端口
1395 端口：PC 工作站管理软件端口
1396 端口：DVL 活跃邮件端口
1397 端口：音频活跃邮件端口
1398 端口：视频活跃邮件端口
1399 端口：Cadkey 许可证管理端口
1433 端口：Microsoft 的 SQL 服务开放端口
1434 端口：Microsoft 的 SQL 服务监视端口
1492 端口：木马 FTP99CMP 开放此端口
1509 端口：木马 Psyber Streaming Server 开放此端口
1512 端口：Microsoft Windows 网络名称服务
1524 端口：许多攻击脚本安装一个后门 SHELL 于这个端口
1600 端口：木马 Shivka-Burka 开放此端口
1645 端口：远程认证拨号用户服务
1701 端口：第 2 层隧道协议
1731 端口：NetMeeting 音频调用控制
1801 端口：Microsoft 消息队列服务器
1807 端口：木马 SpySender 开放此端口
1900 端口：可被利用 ddos 攻击，一般关闭
1912 端口：金山词霸开放此端口
1981 端口：木马 ShockRave 开放此端口
1999 端口：木马 BackDoor,yai 开放此端口
2000 端口：木马 GirlFriend 1.3、Millenium 1.0 开放此端口
2001 端口：木马 Millenium 1.0、Trojan Cow,黑洞 2001 开放此端口
2003 端口：GNU 查询
2023 端口：木马 Pass Ripper 开放此端口
2049 端口：NFS 程序常运行于此端口
2115 端口：木马 Bugs 开放此端口
2140 端口：木马 Deep Throat 1.0/3.0，The Invasor 开放此端口
2500 端口：应用固定端口会话复制的 RPC 客户
2504 端口：网络平衡负荷
2565 端口：木马 Striker 开放此端口
2583 端口：木马 Wincrash 2.0 开放此端口
2801 端口：木马 Phineas Phucker 开放此端口
2847 端口：诺顿反病毒服务开放此端口
3024-3996
3024 端口：木马 WinCrash 开放此端口
3128 端口：squid http 代理服务器开放此端口
3129 端口：木马 Master Paradise 开放此端口
3150 端口：木马 The Invasor,deep throat 开放此端口
3210 端口：木马 SchoolBus 开放此端口
3306 端口：MySQL 开放此端口
3333 端口：木马 Prosiak 开放此端口
3389 端口：WINDOWS 2000 终端开放此端口
3456 端口：inetinfo.exe(互联网信息服务)开放端口，VAT 默认数据
3457 端口：VAT 默认控制
3527 端口：Microsoft 消息队列服务器
3700 端口：木马 Portal of Doom 开放此端口
3996 端口：木马 RemoteAnything 开放此端口

4000 端口：腾讯 QQ 客户端开放此端口
4060 端口：木马 RemoteAnything 开放此端口
4092 端口：木马 WinCrash 开放此端口
4133 端口：NUTS Bootp 服务器
4134 端口：NIFTY-Serve HMI 协议
4141 端口：Workflow 服务器
4142 端口：文档服务器
4143 端口：文档复制
4145 端口：VVR 控制
4321 端口：远程 Who Is 查询
4333 端口：微型 sql 服务器
4349 端口：文件系统端口记录
4350 端口：网络设备
4351 端口：PLCY 网络服务
4453 端口：NSS 警报管理
4454 端口：NSS 代理管理
4455 端口：PR 聊天用户
4456 端口：PR 聊天服务器
4457 端口：PR 注册
4480 端口：Proxy+ HTTP 代理端口
4500 端口：Lsass 开放端口，不能关闭
4547 端口：Lanner 许可管理
4555 端口：RSIP 端口
4590 端口：木马 ICQTrojan 开放此端口
4672 端口：远程文件访问服务器
4752 端口：简单网络音频服务器
4800 端口：Icona 快速消息系统
4801 端口：Icona 网络聊天
4802 端口：Icona 许可系统服务器
4848 端口：App 服务器-Admin HTTP
4849 端口：App 服务器-Admin HTTPS
4950 端口：木马 IcqTrojan 开放 5000 端口
5000 端口：木马 blazer5，Sockets de Troie 开放 5000 端口，一般应关闭
5001 端口：木马 Sockets de Troie 开放 5001 端口
5006 端口：wsm 服务器
5007 端口：wsm 服务器 ssl
5022 端口：mice 服务器
5050 端口：多媒体会议控制协议
5051 端口：ITA 代理
5052 端口：ITA 管理
5137 端口：MyCTS 服务器端口
5150 端口：Ascend 通道管理协议
5154 端口：BZFlag 游戏服务器
5190 端口：America-Online(美国在线)
5191 端口：AmericaOnline1(美国在线)
5192 端口：AmericaOnline2(美国在线)
5193 端口：AmericaOnline3(美国在线)
5222 端口：Jabber 客户端连接
5225 端口：HP(惠普公司)服务器
5226 端口：HP(惠普公司)
5232 端口：SGI 绘图软件端口
5250 端口：i 网关
5264 端口：3Com 网络端口 1
5265 端口：3Com 网络端口 2
5269 端口：Jabber 服务器连接
5306 端口：Sun MC 组
5321 端口：木马 Sockets de Troie 开放 5321 端口
5400 端口：木马 Blade Runner 开放此端口
5401 端口：木马 Blade Runner 开放此端口
5402 端口：木马 Blade Runner 开放此端口
5405 端口：网络支持
5409 端口：Salient 数据服务器
5410 端口：Salient 用户管理
5415 端口：NS 服务器
5416 端口：SNS 网关
5417 端口：SNS 代理
5421 端口：网络支持 2
5423 端口：虚拟用户
5427 端口：SCO-PEER-TTA(Unix 系统)
5432 端口：PostgreSQL 数据库
5550 端口：木马 xtcp 开放此端口
5569 端口：木马 Robo-Hack 开放此端口
5599 端口：公司远程安全安装
5600 端口：公司安全管理
5601 端口：公司安全代理
5631 端口：pcANYWHERE(软件)数据
5632 端口：pcANYWHERE(软件)数据
5673 端口：JACL 消息服务器
5675 端口：V5UA 应用端口
5676 端口：RA 管理
5678 端口：远程复制代理连接
5679 端口：直接电缆连接
5720 端口：MS-执照
5729 端口：Openmail 用户代理层
5730 端口：Steltor’s 日历访问
5731 端口：netscape(网景)suiteware
5732 端口：netscape(网景)suiteware
5742 端口：木马 WinCrash1.03 开放此端口
5745 端口：fcopy-服务器
5746 端口：fcopys-服务器
5755 端口：OpenMail(邮件服务器)桌面网关服务器
5757 端口：OpenMail(邮件服务器)X.500 目录服务器
5766 端口：OpenMail (邮件服务器)NewMail 服务器
5767 端口：OpenMail (邮件服务器)请求代理曾(安全)
5768 端口：OpenMail(邮件服务器) CMTS 服务器
5777 端口：DALI 端口
5800 端口：虚拟网络计算
5801 端口：虚拟网络计算
5802 端口：虚拟网络计算 HTTP 访问, d
5803 端口：虚拟网络计算 HTTP 访问, d
5900 端口：虚拟网络计算机显示 0
5901 端口：虚拟网络计算机显示 1
5902 端口：虚拟网络计算机显示 2
5903 端口：虚拟网络计算机显示 3
6000 端口：X Window 系统
6001 端口：X Window 服务器
6002 端口：X Window 服务器
6003 端口：X Window 服务器
6004 端口：X Window 服务器
6005 端口：X Window 服务器
6006 端口：X Window 服务器
6007 端口：X Window 服务器
6008 端口：X Window 服务器
6009 端口：X Window 服务器

6379端口：redis集群
6456 端口：SKIP 证书发送
6471 端口：LVision 许可管理器
6505 端口：BoKS 管理私人端口
6506 端口：BoKS 管理公共端口
6507 端口：BoKS Dir 服务器,私人端口
6508 端口：BoKS Dir 服务器,公共端口
6509 端口：MGCS-MFP 端口
6510 端口：MCER 端口
6566 端口：SANE 控制端口
6580 端口：Parsec 主服务器
6581 端口：Parsec 对等网络
6582 端口：Parsec 游戏服务器
6588 端口：AnalogX HTTP 代理端口
6631 端口：Mitchell 电信主机
6667 端口：Internet 多线交谈
6668 端口：Internet 多线交谈
6670 端口：木马 Deep Throat 开放此端口
6671 端口：木马 Deep Throat 3.0 开放此端口
6699 端口：Napster 文件(MP3)共享服务
6701 端口：KTI/ICAD 名称服务器
6788 端口：SMC 软件-HTTP
6789 端口：SMC 软件-HTTPS
6841 端口：Netmo 软件默认开放端口
6842 端口：Netmo HTTP 服务
6883 端口：木马 DeltaSource 开放此端口
6939 端口：木马 Indoctrination 开放此端口
6969 端口：木马 Gatecrasher、Priority 开放此端口
6970 端口：real 音频开放此端口
7000 端口：木马 Remote Grab 开放此端口
7002 端口：使用者& 组 数据库
7003 端口：音量定位数据库
7004 端口：AFS/Kerberos 认证服务
7005 端口：音量管理服务
7006 端口：错误解释服务
7007 端口：Basic 监督进程
7008 端口：服务器-服务器更新程序
7009 端口：远程缓存管理服务
7011 端口：Talon 软件发现端口
7012 端口：Talon 软件引擎
7013 端口：Microtalon 发现
7014 端口：Microtalon 通信
7015 端口：Talon 网络服务器
7020 端口：DP 服务
7021 端口：DP 服务管理
7100 端口：X 字型服务
7121 端口：虚拟原型许可证管理
7300 端口：木马 NetMonitor 开放此端口
7301 端口：木马 NetMonitor 开放此端口
7306 端口：木马 NetMonitor，NetSpy1.0 开放此端口
7307 端口：木马 NetMonitor 开放此端口
7308 端口：木马 NetMonitor 开放此端口
7323 端口：Sygate 服务器端
7511 端口：木马聪明基因开放此端口
7588 端口：Sun 许可证管理
7597 端口：木马 Quaz 开放此端口
7626 端口：木马冰河开放此端口
7633 端口：PMDF 管理
7674 端口：iMQ SSL 通道
7675 端口：iMQ 通道
7676 端口：木马 Giscier 开放此端口
7720 端口：Med 图象入口
7743 端口：Sakura 脚本传递协议
7789 端口：木马 ICKiller 开放此端口
7797 端口：Propel 连接器端口
7798 端口：Propel 编码器端口
8000 端口：腾讯 QQ 服务器端开放此端口
8001 端口：VCOM 通道
8007 端口：Apache(类似 iis)jServ 协议 1.x
8008 端口：HTTP Alternate
8009 端口：Apache(类似 iis)JServ 协议 1.3
8010 端口：Wingate 代理开放此端口
8011 端口：木马 way2.4 开放此端口
8022 端口：OA-系统
8080 端口：WWW 代理开放此端口
8081 端口：ICECap 控制台
8082 端口：BlackIce(防止黑客软件)警报发送到此端口
8118 端口：Privoxy HTTP 代理
8121 端口：Apollo 数据端口
8122 端口：Apollo 软件管理端口
8181 端口：Imail
8225 端口：木马灰鸽子开放此端口
8311 端口：木马初恋情人开放此端口
8351 端口：服务器寻找
8416 端口：eSpeech Session 协议
8417 端口：eSpeech RTP 协议
8473 端口：虚拟点对点
8668 端口：网络地址转换
8786 端口：Message 客户端
8787 端口：Message 服务器
8954 端口：Cumulus 管理端口
9000 端口：CS 监听
9001 端口：ETL 服务管理
9002 端口：动态 id 验证
9021 端口：Pangolin 验证
9022 端口：PrivateArk 远程代理
9023 端口：安全网络登陆-1
9024 端口：安全网络登陆-2
9025 端口：安全网络登陆-3
9026 端口：安全网络登陆-4
9101 端口：Bacula 控制器
9102 端口：Bacula 文件后台
9103 端口：Bacula 存储邮件后台
9111 端口：DragonIDS 控制台
9217 端口：FSC 通讯端口
9281 端口：软件传送端口 1
9282 端口：软件传送端口 2
9346 端口：C 技术监听
9400 端口：木马 Incommand 1.0 开放此端口
9401 端口：木马 Incommand 1.0 开放此端口
9402 端口：木马 Incommand 1.0 开放此端口
9594 端口：信息系统
9595 端口：Ping Discovery 服务
9800 端口：WebDav 源端口
9801 端口：Sakura 脚本转移协议-2
9802 端口：WebDAV Source TLS/SSL
9872 端口：木马 Portal of Doom 开放此端口
9873 端口：木马 Portal of Doom 开放此端口
9874 端口：木马 Portal of Doom 开放此端口
9875 端口：木马 Portal of Doom 开放此端口
9899 端口：木马 InIkiller 开放此端口
9909 端口：域名时间
9911 端口：SYPECom 传送协议
9989 端口：木马 iNi-Killer 开放此端口
9990 端口：OSM Applet 程序服务器
9991 端口：OSM 事件服务器
10000 端口：网络数据管理协议
10001 端口：SCP 构造端口
10005 端口：安全远程登陆
10008 端口：Octopus 多路器
10067 端口：木马 iNi-Killer 开放此端口
10113 端口：NetIQ 端点
10115 端口：NetIQ 端点
10116 端口：NetIQVoIP 鉴定器
10167 端口：木马 iNi-Killer 开放此端口
11000 端口：木马 SennaSpy 开放此端口
11113 端口：金山词霸开放此端口
11233 端口：木马 Progenic trojan 开放此端口
12076 端口：木马 Telecommando 开放此端口
12223 端口：木马 Hack’99 KeyLogger 开放此端口
12345 端口：木马 NetBus1.60/1.70、GabanBus 开放此端口
12346 端口：木马 NetBus1.60/1.70、GabanBus 开放此端口
12361 端口：木马 Whack-a-mole 开放此端口
13223 端口：PowWow 客户端，是 Tribal Voice 的聊天程序
13224 端口：PowWow 服务器，是 Tribal Voice 的聊天程序
16959 端口：木马 Subseven 开放此端口
16969 端口：木马 Priority 开放此端口
17027 端口：外向连接
19191 端口：木马蓝色火焰开放此端口
20000 端口：木马 Millennium 开放此端口
20001 端口：木马 Millennium 开放此端口
20034 端口：木马 NetBus Pro 开放此端口
21554 端口：木马 GirlFriend 开放此端口
22222 端口：木马 Prosiak 开放此端口
23444 端口：木马网络公牛开放此端口
23456 端口：木马 Evil FTP、Ugly FTP 开放此端口
25793 端口：Vocaltec 地址服务器
26262 端口：K3 软件-服务器
26263 端口：K3 软件客户端
26274 端口：木马 Delta 开放此端口
27374 端口：木马 Subseven 2.1 开放此端口
30100 端口：木马 NetSphere 开放此端口
30129 端口：木马 Masters Paradise 开放此端口
30303 端口：木马 Socket23 开放此端口
30999 端口：木马 Kuang 开放此端口
31337 端口：木马 BO(Back Orifice)开放此端口
31338 端口：木马 BO(Back Orifice)，DeepBO 开放此端口
31339 端口：木马 NetSpy DK 开放此端口
31666 端口：木马 BOWhack 开放此端口
31789 端口：Hack-a-tack
32770 端口：sun solaris RPC 服务开放此端口
33333 端口：木马 Prosiak 开放此端口
33434 端口：路由跟踪
34324 端口：木马 Tiny Telnet Server、BigGluck、TN 开放此端口
36865 端口：KastenX 软件端口
38201 端口：Galaxy7 软件数据通道
39681 端口：TurboNote 默认端口
40412 端口：木马 The Spy 开放此端口
40421 端口：木马 Masters Paradise 开放此端口
40422 端口：木马 Masters Paradise 开放此端口
40423 端口：木马 Masters Paradise 开放此端口
40426 端口：木马 Masters Paradise 开放此端口
40843 端口：CSCC 防火墙
43210 端口：木马 SchoolBus 1.0/2.0 开放此端口
43190 端口：IP-PROVISION
44321 端口：PCP 服务器(pmcd)
44322 端口：PCP 服务器(pmcd)代理
44334 端口：微型个人防火墙端口
44442 端口：ColdFusion 软件端口
44443 端口：ColdFusion 软件端口
44445 端口：木马 Happypig 开放此端口
45576 端口：E 代时光专业代理开放此端口
47262 端口：木马 Delta 开放此端口
47624 端口：Direct Play 服务器
47806 端口：ALC 协议
48003 端口：Nimbus 网关
50505 端口：木马 Sockets de Troie 开放此端口
50766 端口：木马 Fore 开放此端口
53001 端口：木马 Remote Windows Shutdown 开放此端口
54320 端口：木马 bo2000 开放此端口
54321 端口：木马 SchoolBus 1.0/2.0 开放此端口
61466 端口：木马 Telecommando 开放此端口
65000 端口：木马 Devil 1.03 开放此端口
40422 端口：木马 Masters Paradise 开放此端口
40423 端口：木马 Masters Paradise 开放此端口
40426 端口：木马 Masters Paradise 开放此端口
40843 端口：CSCC 防火墙
43210 端口：木马 SchoolBus 1.0/2.0 开放此端口
43190 端口：IP-PROVISION
44321 端口：PCP 服务器(pmcd)
44322 端口：PCP 服务器(pmcd)代理
44334 端口：微型个人防火墙端口
44442 端口：ColdFusion 软件端口
44443 端口：ColdFusion 软件端口
44445 端口：木马 Happypig 开放此端口
45576 端口：E 代时光专业代理开放此端口
47262 端口：木马 Delta 开放此端口
47624 端口：Direct Play 服务器
47806 端口：ALC 协议
48003 端口：Nimbus 网关
50505 端口：木马 Sockets de Troie 开放此端口
50766 端口：木马 Fore 开放此端口
53001 端口：木马 Remote Windows Shutdown 开放此端口
54320 端口：木马 bo2000 开放此端口
54321 端口：木马 SchoolBus 1.0/2.0 开放此端口
61466 端口：木马 Telecommando 开放此端口
65000 端口：木马 Devil 1.03 开放此端口
65301 端口：PC Anywhere 软件开放端口
'''
    port_list = '''80,23,443,21,22,25,3389,110,445,139,143,53,135,3306,8080,1723,111,995,993,5900,1025,587,8888,199,1720,465,548,113,81,6001,10000,514,5060,179,1026,2000,8443,8000,32768,554,26,1433,49152,2001,515,8008,49154,1027,5666,646,5000,5631,631,49153,8081,2049,88,79,5800,106,2121,1110,49155,6000,513,990,5357,427,49156,543,544,5101,144,7,389,8009,3128,444,9999,5009,7070,5190,3000,5432,1900,3986,13,1029,9,5051,6646,49157,1028,873,1755,2717,4899,9100,119,37'''
    port_list = port_list.split(',')
    #print(port_list)
    for port in port_list:
        port = int(port.replace('\n', ''))
        if port in port_list_used:
            continue
        port_list_used.add(port)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((ip, port))
            s.close()
            with lock:
                print(f'\t\033[32m{ip}:{port} ON\033[0m')

            # 只对可能的 HTTP 端口发请求
            HTTPS_PORTS = (443, 8443)
            HTTP_PORTS  = (80, 8080, 8000, 8081, 8888, 808, 3128)
            if port in HTTP_PORTS:
                url = f"http://{ip}:{port}"
            elif port in HTTPS_PORTS:
                url = f"https://{ip}:{port}"
            else:
                url = None
            if url:
                try:
                    header = {
                            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                        'AppleWebKit/537.36 (KHTML, like Gecko) '
                                        'Chrome/153.0.0.0 Safari/537.36 Edg/153.0.0.0'
                        }
                    response = requests.get(url, headers=header, timeout=2, verify=False)

                        # 修：正则匹配失败时给默认值
                    matches = re.findall(rf'{port}\s*端口：(.*?)\n', server_list)
                    service = matches[0].strip() if matches else "未知服务"

                    with lock:
                        print(f'\t\033[31m[*]目标IP[{port}]\033[0m\033[32m开放\033[0m -> \033[31m状态码:\033[0m\033[32m[{response.status_code}]\033[0m-> \033[34m长度:[{len(response.text)}]\033[0m -> \033[35m服务:[{service}]\033[0m-> \033[36mURL:\033[0m{response.url}')
                except Exception as e:
                        with lock:
                            print(f'\t[{port}] \033[31mHTTP 请求失败: {e}\033[0m')
        except Exception:
            # 端口关闭/超时，静默跳过
            pass

threads = []
for th in range(thread_num):
    t = threading.Thread(target=port_scan)
    t.start()
    threads.append(t)
for t in threads:
     t.join()
print("\n\033[31m[*] 扫描完成\033[0m")
input("输入任意键结束...")