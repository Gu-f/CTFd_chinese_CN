# 汉化迁移  
中文已在官方仓库进行支持，感谢大家一路的关注和支持。  
后续的更新将在[这里](https://poeditor.com/join/project/p5jhdcrlm7)继续，并会合并到[CTFd](https://github.com/CTFd/CTFd)仓库，此仓库将会封存。  
# CTFd_chinese_CN
Time-Line:
+ 对CTFd平台的汉化，并可通过主题切换用户界面的中英文，同时集成CTFd-V2.1.4版本
+ 更新CTFd-V3.0.2版本汉化
+ 更新CTFd-V3.1.0版本汉化，同时主题上优化了大陆上访问CTFd资源无法加载导致的卡顿问题
+ ~~更新CTFd-V3.1.1版本汉化~~  
+ 更新CTFd-V3.1.1版本汉化独立包  
+ ~~更新CTFd-V3.4.0版本汉化包(admin/core), 同时优化大陆访问字体资源导致的卡顿问题~~ 此次的汉化文件以调整V3.4.0/CTFd-3.4.0/CTFd_old文件夹  
+ 更新CTFd V3.4.0版本汉化包本次更新基于代码层面进行了汉化，优化了卡顿，个人模式汉化覆盖率99%，团队模式汉化覆盖率95%
+ 更新CTFd V3.4.1版本汉化包本次更新基于代码层面进行了汉化，个人模式汉化覆盖率99%，团队模式汉化覆盖率95%

# 文件解读：
最新版请访问： https://github.com/CTFd/CTFd   
官方请访问：https://ctfd.io/    
Live Demo 预览演示请访问： https://demo.ctfd.io/  
### V2.1.4
CTFd-原版V2.1.4/CTFd ：文件为开源V2.1.4版本原有的文件，未作任何修改。  
core_chinese ：此文件为汉化的用户界面，不包括管理界面（一般仅用此文件即可）  
core_english ：此文件为原版英文用户界面  
themes ：此文件为汉化的用户及管理界面  

### V3.0.2
CTFd-master-V3.0.2：直接将themes下的admin和core进行替换即可，未增加core_chinese文件

### V3.1.0
CTFd-V3.1.0：直接将themes下的admin和core进行替换即可，未增加core_chinese文件  
预发行汉化版本，目前未发现兼容性问题，但无法保证部分位置汉化不兼容

### V3.1.1
~~CTFd-V3.1.1：与CTFd-V3.1.0通用~~  
CTFd-V3.1.1：直接进行覆盖即可（修改了CDN优化国内访问）  
~~与上一版本通用，目前未发现兼容性问题，但无法保证部分位置汉化~~  
感谢mlzxgzy提供此版本汉化文件  

### V3.4.0
~~CTFd-V3.4.0：直接进行覆盖即可（修改了CDN优化国内访问）~~  
~~截至到readme更新时间，汉化未进行至100%，主要位置已汉化完成，经测试不影响正常使用~~  
感谢mcyydscc提供此版本汉化文件  
通过review上个版本汉化，对汉化内容做了调整  
最新汉化文件所在GitHub中的目录为V3.4.0/CTFd-3.4.0/CTFd，上一版本已调整为CTFd_old
本次更新为基于代码层面汉化，个人模式汉化覆盖率99%，团队模式汉化覆盖率95%，并做了CDN优化  

### V3.4.1
最新汉化文件所在GitHub中的目录为V3.4.1/CTFd-3.4.1/CTFd
本次更新为基于代码层面汉化，个人模式汉化覆盖率99%，团队模式汉化覆盖率95%

# 使用方法：

## V3.4.1版本使用方法：  
方法同V3.4.0，请参考V3.4.0  

## V3.4.0版本使用方法：  
由于该版本汉化调整了python代码，来达到99%的汉化覆盖率，因此需要将整个CTFd文件进行覆盖  
将GitHub中的目录为V3.4.0/CTFd-3.4.0/CTFd内所有文件覆盖到<ctfd_project>/CTFd文件即可  
建议下载release的zip包，来减少冗余代码的下载，提高速度。release的zip包，只包含CTFd文件。  

### 下面两个方法为V3.4.0版本之前的方法，之后的请参考上方  
## 方法一：  
将core_chinese文件直接放入 CTFd\\CTFd\\themes目录即可在更换主题处找到该中文主题  
core_english文件同理  
## 方法二(推荐)：
themes文件直接替换CTFd\\CTFd目录下的themes内的所有文件即可完成汉化  

# 效果预览：  
![img](/image/index.jpg)  

![img](/image/admin.jpg)  

![img](/image/admin2.jpg)  

![img](/image/v3.4.0config.jpg)  

![img](/image/config.jpg)  

![img](/image/top.jpg)  

![img](/image/tz.jpg)  

![img](/image/user.jpg)  
