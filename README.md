# Word Tribe App 单词部落小程序介绍
2024.1.26


## 作品介绍：
Word Tribe App 单词部落小程序是一款强大的单词学习软件，有“每日一言”“积累新单词”“复习单词”“单词挑战”“查看历史成绩”“工具库”等优秀功能，也有着开发者精心打磨优化的反馈效果及美观的界面UI设计，旨在让每个用户都能在智能化环境下更有效、有趣地学习单词，提升英语水平。

## 制作材料：
1. Python3.9.4 因为开发时限较短、项目较简单，考虑使用开发速度快、灵活性强的Python来制作。
2. wxPython Python的GUI拓展库，使用简单，适合小项目使用。
3. Windows NotePad使用外部.txt文件存储用户的历史信息，使得程序可持续化，同时优化用户体验。

## 作品创新：
1.	设计“积累-复习-挑战-分析“的四步走学习模式，让用户在趣味中学会单词，真正扎实地掌握这个单词，提升自己的英语能力。
2.	在“单词挑战“后绘制用户历史成绩折线统计图，帮助用户分析自己的成绩变化趋势，夯实基础、查漏补缺。
3.	开创性地设置外部工具库，将优秀的Web网站集成到软件中，让用户学习更方便，对软件的信赖度更高。

## 制作过程：
制作时间为1.24下午、1.25晚上、1.26上午，总计约13小时，代码共1008行，总大小49K。设计应用程序其实就是源代码开发的过程。我先确定了四大具体功能，然后先实现前端功能（即界面设计），再针对前端的特点精心编写后端程序，打磨信息存储和使用反馈，优化用户体验。
 
### 在设计过程中，我遇到了如下主要困难：
1.	如何存储用户的单词，使得用户的历史信息被保存。
2.	每日一言如何随机出示，同时有足够多的数量，不单调重复。 
3.	读入用户单词时，如果用户是首次使用应用，那么没有存储历史信息的txt文档，强行读入会报FileNotFoundError异常。
4.	“单词积累”模块如何正确分割例句及译文。
5.	在“单词挑战”模块的随机出现选项模块设计中出现技术问题，无法改变选项，正确选项不定。
6.	显示历史成绩的折线统计图中的中文是乱码
7.	想用爬虫爬取牛津、剑桥等字典的信息，实现查单词的功能，但是上述网站没有公开其数据API，所以直接爬取可能违反了其使用条款。
8.	在测试过程中发现页面僵硬，退出只能靠右上角的叉号，很多时候用户输入信息得不到反馈。
9.	代码太乱，修改起来十分费事，自带IDLE不方便，代码可读性差。
10.	软件有时会毫无征兆的崩溃。
    
### 针对以上困难，我经过大量思考、尝试和研究，给出如下解决方法并解决问题：
1.	参考许多App都在AppData文件夹中存储历史信息，我们可以简单效仿，在同目录下用Windows NotePad存储.txt文档，在每次用户使用应用开始时从文档中读取信息并做好相应预设。
2.	上网搜索名言，并自己编写格式化程序把网上杂乱无章的名言变得有序且可供程序识别（可惜的是格式化程序被误删且无法恢复）。使用Python的random库随机出示，还可以切换名言。
3.	使用Python自带的异常处理机制try-except，如果文件不存在就手动创建文件，并对其做好预设，减少用户使用软件的麻烦。
4.	查阅Python官方文档，发现str对象有split()函数，可以根据指定字符分割字符串。为了避免引起歧义，我们采用在正常英语句子中没有的“::”作为分隔符。
5.	通过查阅wxPython官方文档和Python的类实现原理，发现StaticText对象只能进行一次构造+实例化+赋值，但是官方提供了许多改变其属性的接口函数，例如这个功能可以使用SetLabel()函数设置显示的文字。
6.	上网搜索，发现是没有设置使用的语言导致。网站给出的解决方法是使用pylab类库中的mpl对象来设置字体，解决乱码问题。
7.	翻阅wxPython官方文档，发现其中有html2类库，可以把Web网页投射到本地App应用上，果断考虑设置工具库模块，把常用网站链接到应用中。这也是最大的创新之一。
8.	设置用户按下按钮后的反馈，例如“积累新单词”中的“添加词性、释义”模块按下添加按键后会弹出“添加成功！”字样、“单词挑战”模块中选择选项后会输出“Accepted！”或“Wrong Answer！”字样等等。还有很多。
9.	改用性能更强、编辑起来更方便的Sublime text4编辑器。同时重构代码，用编译器自带格式化功能美化代码、添加详细的注释。
10.	发现是有一个while循环中的循环控制变量出错，导致如果用户前面一题答错的话，while循环无法通过循环条件退出，造成死循环。修改后此问题消失。
    
## 软件的实用性考量：
该软件开发时就秉持“以实用为主”的设计理念，一切界面的美观都是建立在完整、清晰的使用逻辑和便于使用、有创新性的功能的基础之上设计的。同时有“查看历史折线统计图”“工具库”等创新性的设计，让其实用性更上一层楼。

## 软件后续可能更新：
1.	找到一个公开数据API的小型英语单词网，把用爬虫查单词、用爬虫爬取单词自动添加到用户数据库中的设想变成现实。
2.	用MySQL数据库进行后端管理，实现用户注册功能，实施多账号间的相互比拼、聊天、发个人博客等功能。
3.	考虑使用PyQt进行后续开发，wxPython无法开发复杂软件。
4.	添加背景图片、艺术字体等效果，让应用更美观。

## 软件效果预览
在项目文件里。

![image1](https://pic.imgdb.cn/item/65c2f5ba9f345e8d030ef4fb.png)
![image2](https://pic.imgdb.cn/item/65c2f5ba9f345e8d030ef581.png)
![image3](https://pic.imgdb.cn/item/65c2f5bb9f345e8d030ef5c9.png)
![image4](https://pic.imgdb.cn/item/65c2f5bb9f345e8d030ef61c.png)
![image5](https://pic.imgdb.cn/item/65c2f5bb9f345e8d030ef6ae.png)

![image6](https://pic.imgdb.cn/item/65c2f5c79f345e8d030f12a1.png)
![image7](https://pic.imgdb.cn/item/65c2f5c79f345e8d030f1330.png)
![image8](https://pic.imgdb.cn/item/65c2f5c79f345e8d030f13d0.png)
![image9](https://pic.imgdb.cn/item/65c2f5c79f345e8d030f141c.png)
![image10](https://pic.imgdb.cn/item/65c2f5c89f345e8d030f1528.png)