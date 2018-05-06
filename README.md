# web-log-analysis

1. 将原始的Web日志数据导入数据库中，建立原始Web访问日志数据表（id, ip, identd, user, time, url, status, size, refer, agent组成）

2. 数据预处理
    1. 数据清理：剔除无用数据
    2. 用户识别：针对不同IP建立个人库，通过基于IP启发式规则来识别
    3. 会话识别：时间阈值、最大向前引用
    4  路径填充：使用站点拓扑结构、用户访问页面的参引页面
    5  事务识别：引用长度法、最大向前引用法、时间窗口

3. 模式挖掘模块（采用 Apriori 算法）：

    基于逐级搜索的思想。它采用多轮搜索的方法，每一轮搜索扫描一遍整个数据集，并最终生成所有的频繁项目集。Apriori算法常常会产生数量巨大的项集，随着序列模式的长度增加，候选序列会成指数级增长，虽然通过Apriori的向下封闭属性缩小了候选项集的大小，但是算法的时间复杂度仍然达不到比较理想的程度。另外，该算法需要多次的扫描日志数据库，只要候选序列的长度增加，就必须扫描一遍数据库，这样对整个算法的执行效率有很大的影响。
    - 改进：缩小候选集大小；缩小事务数据库大小；有共同userID属性的候选集才可能是频繁项目集.
    
    1. 路径分析：判定最频繁访问路径
    2. 关联规则：寻找同一事件中出现不同项的相关性
    3. 序列模式：挖掘数据库中高频率出现有序列
    4. 分类分析：识别一个特殊群体的公共属性的描述，决策树方法或神经元网络
    5. 聚类分析：聚类分析是把具有相似特征的用户或数据项归类,在网站管理中通过聚类具有相似浏览行为的用户。基于模糊理论的Web页面聚类算法与客户群体聚类算法的模糊聚类定义相同。K—means、DBSCAN
    6. 统计：从Web 站点中抽取知识的最常用方法, 它通过分析会话文件, 对浏览时间、浏览路径等进行频度、平均值等统计分析
    7. 协同过滤：采用最近邻技术，利用客户的历史、喜好信息计算用户之间的距离，目标客户对特点商品的喜好程度由最近邻居对商品的评价的加权平均值来计算

4. 分析目标：
    1. 对被频繁访问的资源预警
    2. 网站上不存在资源的请求（恶意传参等）
    3. 观察搜索引擎蜘蛛的来访情况
    4. 观察访客行为
    5. 作用：对访问时间进行统计，可以得到服务器在某些时间段的访问情况； 对IP进行统计，可以得到用户的分布情况； 对请求URL的统计，可以得到网站页面关注情况； 对错误请求的统计，可以更正有问题的页面。

5. 输出结果：
    1. 输出统计报表，联系比较大的属性
    2. 异常行为提醒（离群点检测算法预警）
    3. 用户登录浏览习惯预测分析输出
    4. web日志分析审计输出


## **参考方法：**

1. 数据库设计：
- WALog 表，存储原始Web访问日志。WALog 表中的所有记录按时间顺序依次存储，主键id 字段自增， IP 字段表示用户访问的IP 地址，Date 字段是用户访问该页面的访问时间，Method 字段取值为“GET”或者“POST”，URL 字段存储用户访问的资源，Version 字段是HTTP 协议的版本号，Status 字段表示该次访问是否成功，Bytes 字段表示发送的字节数，Refer 字段为引用页面值，BrowserOS 是指存储浏览器类型和操作系统类型。
- CWALS 表，数据清理后的Web访问日志表，CWALog 表中包含ID， IP，Date，URL，Refer，Browse 字段，其含义与WALog 表中相同。 
- UILog表，用户识别后的日志数据表，包含UID，IP，Date，URL，Refer 字段，其中UID 为每个用户的唯一标识，其他字段意义不变。 
- USILog 表，用户会话识别后的日志数据表，包含USID，Date，URL，Refer 字段，其中USID为每个用户会话的唯一标识。 
- PSLog 表，路径填充后的Web 日志表，包含USID，Date，URL，Rlength 字段，其中Rlength 为页面引用长度，即用户在每个页面上的花费时间。
- CPS 表为内容页面表，包含ID 和URL 字段，该表为一个辅助表，用于路径填充阶段。 
- FILog 表，存储频繁项目集，其中Itemsets 存储频繁项目集合， ID 字段表示该项目是属于ID－频繁项集。
- SPLog 表，序列模式挖掘后存储序列模式Sequences 分别表示频繁序 列，ID 字段表示该序列属于ID－频繁序列。

2. 频繁项目：
- 在日志数据预处理中，Web 日志预处理与传统数据预处理的不同点就是用户识别过程。在候选项集的生成过程中，考虑每个序列UserID 属性，每个候选项集都会有与之相应的一些UserID，在候选项集的合并过程中，如果两个待合并的候选项集有共同的userID属性，那么就可以将这两个集合合并成一个更大的集合，否则，这两个集合就不会生成候选项集了。事实上，如果两个候选项集没有共同的userID 属性，那么它的子集一定不会是频繁项目集，也一定会在算法的剪枝过程中被去掉。所以这样的两个集合是没有必要生成候选项集的。与此同时，候选集缩小之后，也间接地减少了扫描整个数据库的次数。
对于事务数据库的缩减，可以基于下面两个很明显的性质来缩减事务数据库: ①在对候选序列Fk+1计数时，可以提前删除长度小于k+2 的事务，因为长度小于k+2 的事务肯定不会出现在序列集Fk+2中; ②对于任意的事务t∈T( 事务数据库) ，如果i∈I 并且i∈t，f∈Fk且if，则i 可以删除，这就是说，在一次扫描事务数据库T 之后，可以把事务中的非频繁项删除。

3. 频繁序列：
AprioriAll 算法是一个经典的序列模式挖掘算法，但是该算法在生成候选序列的过程中，要求序列中的项目集必须有顺序，但是并不要求连续出现。而在很多实际应用中，要处理的序列不但要求有顺序，而且一定是连续出现的。假设Fk－1是k－1 阶频繁序列，Ck表示k 阶候选序列。那么，在生成候选序列的合并阶段中，将Fk－1和Fk－1合并生成候选序列，对于其中的两个序列s1和s2，如果将s1的第一个项目去掉后得到的余串与将s2的最后一项去掉后得到的余串相同，则将s1和s2合并。

4. 频繁项目集参考算法设计：

频繁项目集生成过程如下所示:
```
输入:
U= { U1，U2，…，Ui} / /用户集合
T = { t1， t2，…，tk} / /会话表
S / /支持度

输出:
·频繁项目集( Sequential Patterns)
( 1) 将会话表S 中的事务按照UserID 排序，然后对于每个session 按照时间顺序排序;
( 2) 生成1－频繁项集F1，F1中的每个项都应该包含一个对应的UseID，F1 = { large 1－itemsets} ;
( 3) 循环for k = 2; Fk－1! = null; k++; / /随后的各轮搜索
( 4) Ck = candidate－gen( Fk－1，S，U) ; / /生成k－候选项集
( 5) 扫描事务数据库中的每个事务ti;
( 6) Ci = subset( Ck，ti)
( 7) 扫描Ci中的所有候选项集集c
( 8) c． count ++; / /c 的计数加1
( 9) 如果ti的长度小于k+1，提前删除ti; / /删除长度小于k+1 的项
( 10) 如果ti不属于Ci，则将ti删除; / /删除非频繁项
( 11) 对任意的t∈ti
( 12) Fk = { c | c． count＞S} ; / /找出支持度大于最小支持度的候选集作为频繁集
( 13) 从F 中寻找最大引用项集
( 14) 结束·



候选项集的生成过程: candidate － gen ( Fk－1，S，U) ，如下所示:
( 1) 初始化，Ck = null;
( 2) 扫描Lk－1 中的每个项集Li
( 3) 对Lk－1 中的每个项集Lj
( 4) 如果Li 和Lj 有相同的U / /某个用户同时访问了Li 和Lj
( 5) c = Li 合并Lj / /合并两个项集生成更大的候选项集
( 6) 如果c 的k－1－子集中存在非频繁项集，则删除c
( 7) 否则，将c 加入到Ck;
( 8) 返回Ck，结束;


·候选序列的生成过程: candidate－gen( Fk－1，S) ，
如下所示:
( 1) 初始化，Ck = null;
( 2) 扫描Lk－1中的每个项集Li
( 3) 对Lk－1中的每个项集Lj
( 4) 如果Li和Lj有相同的U / /某个用户同时访问了Li和Lj
( 5) 如果Li的后k－2 余串和Lj的前k－2 个余串相同/ /连续的两个序列
( 6) c = Li合并Lj / /合并两个项集生成更大的候选项集
( 7) 如果c 的k－1－子集中存在非频繁项集，则删除c
( 8) 否则，将c 加入到Ck;
( 9) 返回Ck
，结束;
```