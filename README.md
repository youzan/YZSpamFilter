<p>
<a href="https://github.com/youzan/"><img alt="有赞logo" width="36px" src="https://img.yzcdn.cn/public_files/2017/02/09/e84aa8cbbf7852688c86218c1f3bbf17.png" alt="youzan">
</p></a>
<p align="center">
    <img alt="项目logo" src="https://img.yzcdn.cn/public_files/2017/02/06/ee0ebced79a80457d77ce71c7d414c74.png">
</p>
<p align="center">易用且有效的中文垃圾信息过滤工具</p>

## 用途
可为帖子、邮件、博客等提供中文垃圾信息过滤服务，开发人员提供训练数据即可生成自己所需的过滤模型，已被业界多个公司使用

## 特点
 
- **准确性高** ：离线测试真实垃圾帖，垃圾信息过滤准确率在90%以上；在线测试真实垃圾帖，指标在80%以上；
- **实时性好** ：可提供实时的垃圾信息过滤服务；
- **模型可自动更新**：支持自动更新模型，增加模型的有效性。

## 依赖

使用前需安装必要的python库，包括 jieba，flask
```
pip install -r requirements.txt
```
## 使用方法

1. 准备两份垃圾信息的文档，一份为正常的信息，一份为垃圾信息，每一行为一条数据，如本项目内的 `ham.txt` 与 `spam.txt`

    > 注: 正负样本数量最好各大于1000

2. 运行数据准备程序 `createTrainAndTestData.py`，生成训练与测试数据
   示例: `python createTrainAndTestData.py`
   运行完毕后，会生成 `trainPos.txt`、`trainNeg.txt`、`testPos.txt`、`testNeg.txt`,分别对应训练正样本、训练负样本、测试正样本、测试负样本

3. 运行训练测试程序 `filter.py`
   示例: `python filter.py`
   该程序首先会利用上步得到的训练样本训练出垃圾信息过滤的模型，然后对上步得到的测试样本进行测试并打印测试结果
   其中tar为正确接受率，及正样本测试正确率，trr为错误拒绝率，即负样本测试正确率，accuracy为整体正确率
   运行一次后，程序将模型保存为pickle文件，下次会直接从该文件中读取模型

    > 特别提示: filter.py程序最后的single judge为调用示例

4. 运行 restful api 主程序 `mainApi.py`
   示例: `python mainApi.py`
   该程序首先会调用 `filterApi.py` 程序，为垃圾信息过滤提供网络接口服务，采用默认的网络接口时，会开启 resuful api 服务，此时调用示例为：
   ```
   curl 'http://0.0.0.0:5060/api/spamfilter?query=赚钱test宝妈tes日赚学生兼职*.@打字员'
   ```
   当 `query` 的信息为垃圾信息时，返回 `{"spam": "True"}`；反之，返回 `{"spam": "False"}`
5. 考虑到实际使用过程中，需要模型进行自动更新，因此 `autorefresh.py` 为垃圾信息的自动更新示例
   示例: `python autorefresh.py`
    1. 当模型错误的将某个正常信息当做垃圾信息时，对于大多数垃圾信息过滤服务而言，问题较为严重，因此，示例中分两步
    ```
    f.Algorithm.discover(FalseRejectstr, True) --- 将该信息从垃圾信息的统计分布取出
    f.Algorithm.cover(FalseRejectstr, False) --- 将该信息加入正常信息的统计分布
    ```
    2. 当模型错误的将某个垃圾信息当做正常信时，问题严重性较低，因此，只做一步
    ```
    f.Algorithm.cover(FalseAcceptstr, True) --- 将该信息加入垃圾信息的统计分布
    ```

    > 注: True表示信息为垃圾信息，False则相反
    > 实际使用过程中，上述两个步骤可根据实际需求自由修改，开发人员可设计程序与数据库对接，实现模型的自动更新

6. `config.py` 中存放了若干程序参数，使用过程中可自由配置，各参数说明如下：
    ```
    'bind_addr': '0.0.0.0',   #服务绑定地址
    'bind_port': 5080,        #服务绑定端口
    'threshold': 83,                          #过滤阈值
    'stopwords_file':'stopwords_common.txt',  #停止词文件
    'classify_model':'filter.pickle',         #过滤模型
    'ham_file':'ham.txt',                     #正常信息
    'spam_file':'spam.txt',                   #垃圾信息
    'train_rate':0.5                          #正常、垃圾信息中用于训练的信息比例（范围0到1）
    ```

## 效果统计

1. 测试效果:  tar = 99.49%, trr = 93.48%, accuracy = 97.61%
2. 线上效果:  经有赞线上效果统计，10.10 - 10.16日一个星期内，对于有赞bbs后台拦截统计，共拦截到垃圾帖子289，其中误拦截为9，漏拦截为43

## 声明
本工具内所有数据与指标统计皆基于有赞BBS后台真实数据

