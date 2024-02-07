# -*- coding: UTF-8 -*-

'''
Word Tribe 单词部落
强大的背单词软件，让大家轻松学习单词。

 @Author    7.8 阎乐成
 @DateTime  2024-01-26
 @copyright None
 @license   None
 @version   1.0.0
'''

import wx  # GUI支持
import wx.html2  # 用来加载外部网页
import random  # 随机数模块
import matplotlib.pyplot as plt  # 绘制折线图
from time import sleep  # 时间模块（等待0.5秒）
from pylab import mpl  # 折线图内避免中文乱码


class Dict:  # 该定义方式为仿结构体(C++ struct)
    '''Dict
    字典类，存储当前词汇的相关信息
    '''

    def __init__(self, _eng, _dic, _sents):
        self.eng = _eng
        self.dic = _dic
        self.sents = _sents
    '''__init__()
    
    初始化设置
    
    Arguments:
        _eng (str) -- 词汇名
        _dic (list[dict]) -- 词性和释义对应的字典，每对词性和释义为单独的字典，用列表存储每个字典
        _sents (list[dict]) -- 例句英文和译文的对应字典，存储方式同_dic
    '''

    def __str__(self):
        return str(self.eng) + str(self.dic) + str(self.sents)
    '''__str__()

    获取用户字典的相关信息，返回字符串

    Returns:
        [str] -- 字典相关信息
    '''


mydict = []  # 用户的单词字典，存储的是对象Dict
sentence = {}  # 存储一言中的内容，全局只更新一次
history = []  # 用户的历史挑战成绩，全局只更新一次


def set_default_txt():  # 为字典文档dict.txt设置默认值
    f = open(r"dict.txt", 'a+')
    f.write(
        "Dict(\"English\", [{\"n. 名词\":\"英语；英语课程\"},{\"adj. 形容词\":\"英国的\"}],[{\"I love English. : 我爱英语。\"}])" + '\n')
    f.write("Dict(\"Chinese\",[{\"n. 名词\":\"中国人\"},{\"adj. 形容词\":\"中国人的\"}],[{\"I am Chinese. \":\" 我是中国人。\"}])" + '\n')
    f.write("Dict(\"learn\",[{\"v. 动词\":\"学习\"}],[{\"He learns English. \":\" 他学习英语。\"}])" + '\n')
    f.write("Dict(\"easy\",[{\"adj. 形容词\":\"简单的\"}],[{\"Learning English is easy. \":\" 学英语很简单。\"}])" + '\n')
    f.close()


def get_dict():  # 获取用户的单词字典
    try:  # 检测异常，没有的话自动创建文件
        f = open(r"dict.txt", 'r')
    except FileNotFoundError:
        # 避免readlines()错误（文件为空），设置默认值
        set_default_txt()
        f = open(r"dict.txt", 'r')
    global mydict
    mydict = []  # 清空一波
    lis = f.readlines()
    for it in lis:
        temp = eval(str(it))
        mydict.append(temp)
    f.seek(0)  # 还原文件指针到初始位置，便于下次打开
    f.close()


def get_sent_txt():  # 从txt文件中读取所有的一言，存储到字典中
    global sentence  # 引入全局变量
    f = open("good_sentences.txt", 'r', encoding='UTF-8')  # 用utf-8编码读入中文
    lis = f.readlines()
    i = 0
    while i < len(lis) and i + 1 < len(lis):  # 防止列表下标越界
        if i < 10:  # 根据句子序号确定要删除前多少个字符
            t = 2
        elif 10 <= i < 99:
            t = 3
        elif 99 <= i < 100:
            t = 4
        sentence[lis[i][t:]] = lis[i + 1]  # 用切片，避免加上txt中前面句子的序号
        i += 2
    f.close()


def get_history():  # 读取用户历史的挑战成绩
    global history
    try:  # 检测异常，没有的话自动创建文件
        f = open(r"history.txt", 'r')
    except FileNotFoundError:
        # 避免readlines()错误（文件为空），设置默认值
        f = open(r"history.txt", 'a+')  # 创建文件
        f.close()
        f = open(r"history.txt", 'r')
    history = []  # 清空
    for it in f.readlines():
        history.append(float(it))


def add_enter(sent, pos):  # 给字符串添加换行符，为了一言显示美观
    # pos==0表示修改英文句子，pos==1表示修改中文句子
    sentL = []
    if pos == 0:  # 修改英文句子，单词间有空格
        sentL = sent.split()  # 用空格分割，为了显示完整的单词把字符串分割成列表
    elif pos == 1:  # 修改中文句子，字符间没有空格
        sentL = []
        for it in sent:  # 需手动把字符串转换成列表
            sentL.append(it)
    if pos == 0:
        temp = 20  # 英文字符20个一换行
    elif pos == 1:
        temp = 10  # 中文字符10个一换行
    s = 0  # 记录当前已经确定显示的字符长度
    flag = True  # 开关初始化
    for it in range(len(sentL)):
        if s + len(sentL[it]) >= temp:
            sentL[it] = '\n' + sentL[it]  # 给这一个前加上换行
            s = 0
        else:
            if pos == 0:  # 否则英文加上空格，中文不加空格
                sentL[it] = ' ' + sentL[it]
            s += len(sentL[it])
        if '——' in sentL[it]:  # （英文串的作者区域）为了美观，如果有名言作者也加上换行
            sentL[it] = '\n' + sentL[it]
            s = 0  # 加了换行符后长度清空
        elif '—' in sentL[it] and flag == True:  # （中文串作者的区域）
            # 中文串的‘————’会被拆分成四个‘—’
            sentL[it] = '\n' + sentL[it]
            s = 0  # 加了换行符后长度清空
            flag = False  # 因为只有一个作者，所以加一次换行即可，开关变为false
    sent = ''.join(sentL)
    return sent


def get_random_sent():  # 获取随机的一言
    pos = random.randint(0, 99)  # 随机选择一个句子
    sent1 = str(list(sentence.keys())[pos])
    sent1 = add_enter(sent1, 0)  # 添加换行符，避免显示超出应用框
    sent2 = str(list(sentence.values())[pos])
    sent2 = add_enter(sent2, 1)
    sent = sent1 + '\n\n' + sent2  # 合并名言和翻译，中间加上两个换行
    return sent


def get_random_word():  # 获取随机用户字典中的单词
    inx = int(random.randint(0, len(mydict) - 1))  # randint区间是闭区间，而数组下标是从0~(len-1)，所以随机数后项要-1
    temp = mydict[inx].eng
    return temp


def get_word_inx(finder):  # 寻找单词在用户字典中的索引
    for i in range(len(mydict)):
        if mydict[i].eng == finder:  # 找到就返回索引值
            return i
    return -1  # 没查找到返回-1


def get_random_di(inx):  # 随机获取对应用户字典元素中的释义
    # 传入字典中元素的下标
    l = list(mydict[inx].dic)
    inx2 = int(random.randint(0, len(l) - 1))  # 随机下标
    return str(''.join(l[inx2].values()))  # 获取唯一的键(用列表+字典的存储形式)，转换成字符串返回


class AddNewWords(wx.Frame):  # 积累新单词窗口类
    def __init__(self, superior):
        # 设置窗口基础信息
        _title = "Word Tribe 单词部落 > Add New Words - 积累新单词"
        wx.Frame.__init__(self, parent=superior, id=wx.ID_ANY, title=_title, pos=(300, 100), size=(800, 650))

        # 设置窗口容器
        panel = wx.Panel(self, -1)

        lbl = wx.StaticText(panel, -1, "Add New Words 积累新单词", pos=(120, 20))  # 居中放置，略微偏左，保持美观
        font = wx.Font(30, wx.DECORATIVE, wx.ITALIC, wx.BOLD, underline=True)  # 古老英文字体 粗体 斜体 加下划线
        lbl.SetFont(font)
        lbl.SetForegroundColour('#156DC4')  # 用靛蓝色

        # 设置新单词的输入框，包含单词、词性、词性对应意思、例句
        # 英语词汇
        lbl1 = wx.StaticText(panel, -1, "Vocabulary 词汇", pos=(50, 100))  # 居中放置，略微偏左，保持美观
        font1 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False)  # 古老英文字体 粗体
        lbl1.SetFont(font1)

        self.temp_eng = wx.TextCtrl(panel, -1, "", pos=(240, 100), size=(250, -1), style=wx.TE_CENTER)
        font2 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL, False)
        self.temp_eng.SetFont(font2)

        # 词性 + 汉语意思
        lbl2 = wx.StaticText(panel, -1, "Characteristic 词性", pos=(50, 150))  # 居中放置，略微偏左，保持美观
        font3 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False)  # 古老英文字体 粗体
        lbl2.SetFont(font3)

        # 用下拉选择框处理词性
        self.list1 = ["n. 名词", "v. 动词", "adj. 形容词", "adv. 副词",
                      "conj. 连词", "prep. 介词", "pron. 代词", "num. 数词", "int. 感叹词"]
        self.temp_char = wx.ComboBox(panel, value="", size=(100, -1), pos=(300, 150),
                                     choices=self.list1, style=wx.CB_DROPDOWN)  # style里是下拉列表

        self.wordL = []  # 当前词汇字典，用列表存储，{词性:释义}
        lbl3 = wx.StaticText(panel, -1, "Definition 释义", pos=(50, 200))
        font4 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False)  # 古老英文字体 粗体
        lbl3.SetFont(font4)

        # 词性对应的释义由用户自己输入
        self.temp_zh = wx.TextCtrl(panel, -1, "", pos=(240, 200), size=(250, -1))

        # 加上添加词性的按钮
        button1 = wx.Button(panel, wx.ID_ANY, pos=(240, 250), size=(80, 35), label="Add 添加")
        button1.Bind(wx.EVT_BUTTON, self.add_char)

        # 例句输入
        lbl4 = wx.StaticText(panel, -1, "Example 例句", pos=(50, 300))
        font5 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False)  # 古老英文字体 粗体
        lbl4.SetFont(font5)

        # 输入格式提示
        lbl5 = wx.StaticText(panel, -1, "Input Format 输入格式：English sentences. :: 中文译文。", pos=(200, 300))

        # 输入词性成功的提示反馈
        self.lbl6 = wx.StaticText(panel, -1, "", pos=(400, 260))
        font6 = wx.Font(12, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline=False)  # 古老英文字体 粗体
        self.lbl6.SetFont(font6)

        # 输入框
        self.temp_exam = wx.TextCtrl(panel, -1, "", pos=(240, 320), size=(250, -1), style=wx.TE_MULTILINE)

        # 最终确定按钮
        button2 = wx.Button(panel, wx.ID_ANY, pos=(240, 550), size=(80, 35), label="Accept 确认")
        button2.Bind(wx.EVT_BUTTON, self.accepted)

        # 清除选项按钮
        button3 = wx.Button(panel, wx.ID_ANY, pos=(350, 550), size=(80, 35), label="Delete 清除")
        button3.Bind(wx.EVT_BUTTON, self.clear)

        # 退出按钮
        button4 = wx.Button(panel, wx.ID_ANY, pos=(460, 550), size=(80, 35), label="Quit 退出")
        button4.Bind(wx.EVT_BUTTON, self.quit)

        # 添加开发者标识
        dev_lbl = wx.StaticText(panel, label="Developed by Yan Lecheng, Class 8, Grade 7,\n     Laoshan Experimental Junior Middle School\nV1.0.0", pos=(
            450, 500))
        dev_font = wx.Font(10, wx.FONTFAMILY_SCRIPT, wx.NORMAL, wx.LIGHT, underline=False)  # 楷体 粗体
        dev_lbl.SetFont(dev_font)
        dev_lbl.SetForegroundColour('#060408')  # 黑色

    def quit(self, event):  # 退出按钮
        self.Close()  # 退出窗口

    def add_char(self, event):  # 增加新词性和释义的添加按钮
        self.lbl6.SetLabel('')  # 在这里清空，便于后续反馈
        char = self.temp_char.GetStringSelection()  # 获取选择的字符后才能
        txt = self.temp_zh.GetValue()  # 释义
        self.wordL.append({str(char), str(txt)})
        # 优化反馈，添加后给出提示语
        sleep(0.5)  # 等待0.5秒，给用户看到的时间
        self.lbl6.SetLabel('添加成功！')
        self.lbl6.SetForegroundColour('#26EB10')  # 设置为绿色

    def clear(self, event):  # 清空按钮
        self.wordL = []  # 清空释义列表
        self.temp_eng.Clear()  # 清除输入内容
        self.temp_zh.Clear()
        self.temp_exam.Clear()
        self.temp_char.Clear()
        self.temp_char.Append(self.list1)  # 下拉列表Clear函数会连带清除choices中的内容，清除完后重新赋值

    def accepted(self, event):  # 保存按钮
        txt1 = self.temp_eng.GetValue()  # 获取英文
        # 释义及对应的词性存储在wordL列表中
        txt2 = self.temp_exam.GetValue()  # 获取例句
        txt2 = txt2.split('\n')
        f = open("dict.txt", 'a+')
        st = "Dict(\"" + txt1 + "\",["  # 存储一个中间变量记录输出内容，便于直接加入到mydict中，不用重新读取
        i = 0
        for it1, it2 in self.wordL:
            st += "{\"" + it1 + "\":\"" + it2 + "\"}"
            if i < len(self.wordL) - 1:
                st += ','  # 这样做最后一次不输出多余逗号
            i += 1
        st += "],["
        i = 0
        for it in txt2:
            if it == "":  # 如果没有例句的话会报错，人为加上::防止存储单词失败
                it = " :: "
            it = list(str(it).split("::"))  # 把两个句子以冒号分开
            st += "{\"" + it[0] + "\":\"" + it[1] + "\"}"  # 现在可以正常输出
            if i < len(txt2) - 1:  # 最后一个不要多输出逗号
                st += ','
            i += 1
        st += "])"
        mydict.append(eval(st))  # 魔法函数eval，对字符串中的表达式或类型初始化求值
        f.write('\n' + st)  # 向文件写入
        f.close()
        self.clear(None)  # 优化，确认后自动清空


class WordCompetition(wx.Frame):  # 背单词窗口类

    def __init__(self, superior):
        # 设置窗口基础信息
        _title = "Word Tribe 单词部落 > Word Competition - 单词挑战"
        wx.Frame.__init__(self, parent=superior, id=wx.ID_ANY, title=_title, pos=(300, 100), size=(800, 650))

        # 设置窗口容器
        panel = wx.Panel(self, -1)

        # 设置基础页面控件
        lbl1 = wx.StaticText(panel, -1, "Word Competition 单词挑战", pos=(120, 20))  # 居中放置，略微偏左，保持美观
        font1 = wx.Font(30, wx.DECORATIVE, wx.ITALIC, wx.BOLD, underline=True)  # 古老英文字体 粗体 斜体 加下划线
        lbl1.SetFont(font1)
        lbl1.SetForegroundColour('#156DC4')  # 用靛蓝色

        lbl2 = wx.StaticText(panel, -1, "Given Words:\n（给出单词）", pos=(100, 100))  # 居中放置，略微偏左，保持美观
        font2 = wx.Font(17, wx.DECORATIVE, wx.NORMAL, wx.BOLD, underline=False)  # 古老英文字体 粗体
        lbl2.SetFont(font2)

        # lbl3设置成类成员变量，在类内函数里还要用到
        self.lbl3 = wx.StaticText(panel, -1, "Default 默认", pos=(270, 100))  # 居中放置，略微偏左，保持美观
        font3 = wx.Font(17, wx.DECORATIVE, wx.NORMAL, wx.BOLD, underline=True)  # 古老英文字体 粗体 加下划线
        self.lbl3.SetFont(font3)
        self.lbl3.SetForegroundColour('#010D09')  # 用黑色
        temp = get_random_word()  # 设置随机单词
        self.lbl3.SetLabel(temp)

        # 设置随机选项
        if len(mydict) >= 4:  # 用户字典里有四个以上的单词才能设置选项
            inx1 = get_word_inx(temp)  # 获取当前单词在字典中的序号
            opt1 = get_random_di(inx1)  # 获取随机释义作为选项
            self.true = int(random.randint(0, 3))  # 随机正确答案在哪个选项里
            self.trueL = [(220, 150), (470, 150), (220, 210), (470, 210)]  # 设置四个选项对应位置
            # lbl4设置成类成员变量，在类内函数里还要用到
            self.lbl4 = wx.StaticText(panel, -1, str(chr(65 + self.true) + '. ' + opt1),
                                      pos=self.trueL[self.true])  # 居中放置，略微偏左，保持美观
            font4 = wx.Font(17, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False)  # 默认字体 粗体
            self.lbl4.SetFont(font4)
            self.lbl4.SetForegroundColour('#010D09')  # 用黑色

            inx2 = inx1
            while inx2 == inx1:  # 避免重复序号
                inx2 = int(random.randint(0, len(mydict) - 1))
            opt2 = get_random_di(inx2)  # 获取选项对应释义
            true2 = self.true
            while true2 == self.true:  # 避免重复选项编号
                true2 = int(random.randint(0, 3))
            # lbl5设置成类成员变量，在类内函数里还要用到
            self.lbl5 = wx.StaticText(panel, -1, str(chr(65 + true2) + '. ' + opt2),
                                      pos=self.trueL[true2])  # 居中放置，略微偏左，保持美观
            font5 = wx.Font(17, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False)  # 默认字体 粗体
            self.lbl5.SetFont(font5)
            self.lbl5.SetForegroundColour('#010D09')  # 用黑色

            inx3 = inx1
            while inx3 == inx1 or inx3 == inx2:  # 避免重复序号
                inx3 = int(random.randint(0, len(mydict) - 1))
            opt3 = get_random_di(inx3)  # 获取选项对应释义
            true3 = self.true
            while true3 == self.true or true3 == true2:  # 避免重复选项编号
                true3 = int(random.randint(0, 3))
            # lbl6设置成类成员变量，在类内函数里还要用到
            self.lbl6 = wx.StaticText(panel, -1, str(chr(65 + true3) + '. ' + opt3),
                                      pos=self.trueL[true3])  # 居中放置，略微偏左，保持美观
            font6 = wx.Font(17, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False)  # 默认字体 粗体
            self.lbl6.SetFont(font6)
            self.lbl6.SetForegroundColour('#010D09')  # 用黑色

            inx4 = inx1
            while inx4 == inx3 or inx4 == inx1 or inx4 == inx2:  # 避免重复序号
                inx4 = int(random.randint(0, len(mydict) - 1))
            opt4 = get_random_di(inx4)  # 获取选项对应释义
            true4 = self.true
            while true4 == true3 or true4 == self.true or true4 == true2:  # 避免重复选项编号
                true4 = int(random.randint(0, 3))
            # lbl7设置成类成员变量，在类内函数里还要用到
            self.lbl7 = wx.StaticText(panel, -1, str(chr(65 + true4) + '. ' + opt4),
                                      pos=self.trueL[true4])  # 居中放置，略微偏左，保持美观
            font7 = wx.Font(17, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False)  # 默认字体 粗体
            self.lbl7.SetFont(font7)
            self.lbl7.SetForegroundColour('#010D09')  # 用黑色

        self.lbl8 = wx.StaticText(panel, -1, "Select 选择（A、B、C、D）:",
                                  pos=(50, 250))  # 居中放置，略微偏左，保持美观
        font8 = wx.Font(17, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline=False)  # 默认字体 粗体
        self.lbl8.SetFont(font8)
        self.lbl8.SetForegroundColour('#010D09')  # 用黑色
        self.temp_ans = wx.TextCtrl(panel, -1, "", pos=(365, 250), size=(100, -1))

        # 设置确认选择按钮
        self.button1 = wx.Button(panel, wx.ID_ANY, pos=(200, 300), size=(80, 35), label="Accept 确定")
        self.button1.Bind(wx.EVT_BUTTON, self.accept)

        # 设置切换下一个按钮
        self.button2 = wx.Button(panel, wx.ID_ANY, pos=(200, 350), size=(80, 35), label="Next 下一个")
        self.button2.Bind(wx.EVT_BUTTON, self.go_next)

        # 设置退出按钮
        self.button3 = wx.Button(panel, wx.ID_ANY, pos=(200, 400), size=(80, 35), label="Quit 退出")
        self.button3.Bind(wx.EVT_BUTTON, self.quit)

        # 预设置结果文本框
        self.lbl9 = wx.StaticText(panel, -1, "", pos=(330, 300))
        font9 = wx.Font(17, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline=False)  # 默认字体 粗体
        self.lbl9.SetFont(font9)

        # 预设置显示答案文本框，这个pos针对Accepted
        self.lbl10 = wx.StaticText(panel, -1, "", pos=(520, 300))
        font10 = wx.Font(10, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline=False)  # 默认字体 粗体
        self.lbl10.SetFont(font10)

        self.true_tot = 0  # 回答正确数
        self.wrong_tot = 0  # 回答错误数

        # 添加开发者标识
        dev_lbl = wx.StaticText(panel, label="Developed by Yan Lecheng, Class 8, Grade 7,\n     Laoshan Experimental Junior Middle School\nV1.0.0", pos=(
            450, 500))
        dev_font = wx.Font(10, wx.FONTFAMILY_SCRIPT, wx.NORMAL, wx.LIGHT, underline=False)  # 楷体 粗体
        dev_lbl.SetFont(dev_font)
        dev_lbl.SetForegroundColour('#060408')  # 黑色

    def ShowMessage(self):
        # 显示正确数、错误数、正确率
        st = "正确：{0}  错误：{1}  正确率：{:.2f}".format(self.true_tot, self.wrong_tot,
                                                 self.true_tot / (self.true_tot + self.wrong_tot))
        wx.MessageBox("答题结果", st, wx.OK | wx.ICON_INFORMATION)

    def quit(self, event):  # 设置退出按钮，弹出消息框，可以查看报表
        # 显示正确数、错误数、正确率
        st = "正确：{0}  错误：{1}  正确率：{2:.2f}".format(self.true_tot, self.wrong_tot,
                                                  self.true_tot / max(1, self.true_tot + self.wrong_tot))
        # 加一个max()函数是为了避免除以0而报异常

        # 记录到历史成绩中，答题数为0不记录，视为无效数据
        if self.true_tot + self.wrong_tot > 0:
            temp = float(self.true_tot / (self.true_tot + self.wrong_tot))
            history.append(temp)
            f = open(r"history.txt", 'a+')  # 打开文件，追加写模式
            print("{:.2f}".format(temp), file=f)
            f.close()

        # 信息框
        dial = wx.MessageDialog(None, caption="答题结果",
                                message=st,
                                style=wx.YES_NO)
        result = dial.ShowWindowModal()
        if result == wx.ID_YES or result == wx.ID_NO:  # 获取用户的选择，不管选择什么都退出窗口
            pass  # 这里纯粹是为了等待用户按下选项，无实际作用
        self.Close()  # 关闭当前窗口

    def go_next(self, event):  # 切换下一个按钮，用来初始设置+切屏
        # 出示随机单词
        temp = get_random_word()
        self.lbl3.SetLabel(temp)

        # 设置随机选项
        panel = wx.Panel(self, -1)
        if len(mydict) >= 4:  # 用户字典里有四个以上的单词才能设置选项
            inx1 = get_word_inx(temp)  # 获取当前单词在字典中的序号
            opt1 = get_random_di(inx1)  # 获取随机释义作为选项
            self.true = int(random.randint(0, 3))  # 随机正确答案在哪个选项里
            self.trueL = [(220, 150), (420, 150), (220, 210), (420, 210)]  # 设置四个选项对应位置

            # 修改旧选项
            self.lbl4.SetLabel(str(chr(65 + self.true) + '. ' + opt1))  # 修改内容
            self.lbl4.SetPosition(self.trueL[self.true])  # 修改坐标

            inx2 = inx1
            while inx2 == inx1:  # 避免重复序号
                inx2 = int(random.randint(0, len(mydict) - 1))
            opt2 = get_random_di(inx2)  # 获取选项对应释义
            true2 = self.true
            while true2 == self.true:  # 避免重复选项编号
                true2 = int(random.randint(0, 3))

            # 修改旧选项
            self.lbl5.SetLabel(str(chr(65 + true2) + '. ' + opt2))  # 修改内容
            self.lbl5.SetPosition(self.trueL[true2])  # 修改坐标

            inx3 = inx1
            while inx3 == inx1 or inx3 == inx2:  # 避免重复序号
                inx3 = int(random.randint(0, len(mydict) - 1))
            opt3 = get_random_di(inx3)  # 获取选项对应释义
            true3 = self.true
            while true3 == self.true or true3 == true2:  # 避免重复选项编号
                true3 = int(random.randint(0, 3))

            # 修改旧选项
            self.lbl6.SetLabel(str(chr(65 + true3) + '. ' + opt3))  # 修改内容
            self.lbl6.SetPosition(self.trueL[true3])  # 修改坐标

            inx4 = inx1
            while inx4 == inx3 or inx4 == inx1 or inx4 == inx2:  # 避免重复序号
                inx4 = int(random.randint(0, len(mydict) - 1))
            opt4 = get_random_di(inx4)  # 获取选项对应释义
            true4 = self.true
            while true4 == true3 or true4 == self.true or true4 == true2:  # 避免重复选项编号
                true4 = int(random.randint(0, 3))

            # 修改旧选项
            self.lbl7.SetLabel(str(chr(65 + true4) + '. ' + opt4))  # 修改内容
            self.lbl7.SetPosition(self.trueL[true4])  # 修改坐标

        self.temp_ans.SetLabel('')  # 设置填写区为空
        self.lbl9.SetLabel('')  # 清空答案结果显示
        self.lbl10.SetLabel('')  # 清空正确答案显示

    def accept(self, event):  # 确认按钮，对答案进行判断，显示正确答案
        txt1 = self.temp_ans.GetValue()  # 获取用户答案
        trueans = chr(65 + self.true)  # 获取正确答案的选项
        panel = wx.Panel(self, -1)

        # 显示正确/错误
        if txt1 == trueans:  # 用户选项正确
            self.lbl9.SetLabel('Accepted! 正确！')
            self.lbl9.SetForegroundColour('#26EB10')  # 用绿色
            self.true_tot += 1  # 统计变量加一
            # 设置合适于Accepted的位置
            self.lbl10.SetPosition((520, 300))
        else:
            self.lbl9.SetLabel('Wrong Answer! 错误！')
            self.lbl9.SetForegroundColour('#FF0000')  # 用红色
            self.wrong_tot += 1  # 统计变量加一
            # Wrong Answer 长度较长，需要调整一下正确答案的显示位置，避免遮挡
            self.lbl10.SetPosition((570, 300))

        # 显示正确答案
        self.lbl10.SetLabel('正确答案：' + trueans)


class ReviewWords(wx.Frame):  # 复习单词窗口类
    def __init__(self, superior):
        # 设置窗口基础信息
        _title = "Word Tribe 单词部落 > Review Words - 复习单词"
        wx.Frame.__init__(self, parent=superior, id=wx.ID_ANY, title=_title, pos=(300, 100), size=(800, 650))

        # 设置窗口容器
        panel = wx.Panel(self, -1)

        # 设置基础页面控件
        lbl1 = wx.StaticText(panel, -1, "Review Words 复习单词", pos=(120, 20))  # 居中放置，略微偏左，保持美观
        font1 = wx.Font(30, wx.DECORATIVE, wx.ITALIC, wx.BOLD, underline=True)  # 古老英文字体 粗体 斜体 加下划线
        lbl1.SetFont(font1)
        lbl1.SetForegroundColour('#156DC4')  # 用靛蓝色

        # 显示当前字典中第一个单词
        self.pos = 0
        self.temp = mydict[self.pos].eng

        self.lbl2 = wx.StaticText(panel, -1, "Vocabulary 词汇: ", pos=(30, 100))  # 居中放置，略微偏左，保持美观
        font2 = wx.Font(20, wx.DECORATIVE, wx.NORMAL, wx.BOLD, underline=False)  # 古老英文字体 粗体
        self.lbl2.SetFont(font2)
        self.lbl2.SetForegroundColour('#000000')  # 用黑色

        self.lbl3 = wx.StaticText(panel, -1, self.temp, pos=(280, 100))  # 居中放置，略微偏左，保持美观
        font3 = wx.Font(20, wx.DECORATIVE, wx.ITALIC, wx.BOLD, underline=True)  # 古老英文字体 粗体 斜体 加下划线
        self.lbl3.SetFont(font3)
        self.SetForegroundColour('#000000')  # 用黑色

        # 预设置显示单词词汇及释义的区域
        self.lbl4 = wx.StaticText(panel, -1, "Characteristic And Definition:\n（词性和释义）", pos=(10, 200))
        font4 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False)  # 默认字体 粗体
        self.lbl4.SetFont(font4)
        self.SetForegroundColour('#000000')  # 用黑色

        self.lbl5 = wx.StaticText(panel, -1, "", pos=(350, 200))
        font5 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline=False)  # 默认字体
        self.lbl5.SetFont(font5)
        self.SetForegroundColour('#000000')  # 用黑色

        # 预设置显示单词例句的区域
        self.lbl6 = wx.StaticText(panel, -1, "Example 例句: ", pos=(10, 300))
        font6 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False)  # 默认字体 粗体
        self.lbl6.SetFont(font6)
        self.SetForegroundColour('#000000')  # 用黑色

        self.lbl7 = wx.StaticText(panel, -1, "", pos=(350, 200))
        font7 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.NORMAL, underline=False)  # 默认字体
        self.lbl7.SetFont(font7)
        self.SetForegroundColour('#000000')  # 用黑色

        # 设置显示详细信息按钮
        button1 = wx.Button(panel, wx.ID_ANY, pos=(600, 100), size=(100, 55), label="Display Definition\n显示信息")
        button1.Bind(wx.EVT_BUTTON, self.show_info)

        # 设置预览下一个按钮
        button2 = wx.Button(panel, wx.ID_ANY, pos=(600, 155), size=(100, 55), label="Next 下一个")
        button2.Bind(wx.EVT_BUTTON, self.go_next)

        # 设置退出按钮
        button3 = wx.Button(panel, wx.ID_ANY, pos=(600, 210), size=(100, 55), label="Quit 退出")
        button3.Bind(wx.EVT_BUTTON, self.quit)

        # 添加开发者标识
        dev_lbl = wx.StaticText(panel, label="Developed by Yan Lecheng, Class 8, Grade 7,\n     Laoshan Experimental Junior Middle School\nV1.0.0", pos=(
            450, 500))
        dev_font = wx.Font(10, wx.FONTFAMILY_SCRIPT, wx.NORMAL, wx.LIGHT, underline=False)  # 楷体 粗体
        dev_lbl.SetFont(dev_font)
        dev_lbl.SetForegroundColour('#060408')  # 黑色

    # 退出窗口
    def quit(self, event):
        self.Close()  # 关闭当前窗口对象

    # 切换到下一个单词
    def go_next(self, event):
        # 指针变量加一，取模是为了防止越界
        self.pos = (self.pos + 1) % len(mydict)
        # 设置新词汇
        self.lbl3.SetLabel(mydict[self.pos].eng)
        # 词性及释义隐藏
        self.lbl5.SetLabel('')
        # 例句显示区归位
        self.lbl6.SetPosition((10, 300))
        # 清空显示的例句
        self.lbl7.SetLabel('')

    def show_info(self, event):  # 显示单词详细信息
        inx = self.pos  # 获取当前单词在字典列表中的编号
        st = ""  # 这将是存储当前词汇的词性及释义导出格式的字符串
        for it in mydict[inx].dic:
            s1 = ''.join(it.keys())  # 这个字典只有唯一的键和值，直接转为字符串即可
            s2 = ''.join(it.values())
            st += s1 + (' ' * 3) + s2 + '\n\n'  # 中间加三个空格
        self.lbl5.SetLabel(st)

        # 根据词性个数设置例句的位置
        self.lbl6.SetPosition((10, 250 + len(mydict[inx].dic) * 20))  # 每一个词性大约高20像素
        self.lbl7.SetPosition((180, 250 + len(mydict[inx].dic) * 20))

        st = ""  # 这将是存储例句导出格式的字符串
        for it in mydict[inx].sents:
            s1 = ''.join(it.keys())  # 这个字典只有唯一的键和值，直接转为字符串即可
            s2 = ''.join(it.values())
            st += s1 + '\n    ' + s2 + '\n\n'  # 中间加一个换行和缩进
        self.lbl7.SetLabel(st)


class Tools(wx.Frame):  # 工具库窗口类，wx.Dialog用来显示网页

    def __init__(self, superior):
        # 设置窗口基础信息
        wx.Frame.__init__(self, parent=superior, id=wx.ID_ANY,
                          title="Word Tribe 单词部落 > Tools - 工具库", pos=(300, 100), size=(800, 650))
        # 设置窗口容器
        panel = wx.Panel(self, -1)

        # 设置基础页面控件
        lbl1 = wx.StaticText(panel, -1, "Tools 工具库", pos=(260, 20))  # 居中放置，略微偏左，保持美观
        font1 = wx.Font(30, wx.DECORATIVE, wx.ITALIC, wx.BOLD, underline=True)  # 古老英文字体 粗体 斜体 加下划线
        lbl1.SetFont(font1)
        lbl1.SetForegroundColour('#156DC4')  # 用靛蓝色

        lbl2 = wx.StaticText(panel, -1, "English Tools:\n英语工具", pos=(20, 70))  # 居中放置，略微偏左，保持美观
        font2 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False)  # 粗体
        lbl2.SetFont(font2)
        lbl2.SetForegroundColour('black')  # 用黑色

        # 放置许多工具按钮
        # 设置查看牛津字典
        button1 = wx.Button(panel, wx.ID_ANY, pos=(200, 65), size=(100, 70), label="Oxford\n牛津字典")
        button1.Bind(wx.EVT_BUTTON, self.tool1)

        # 查看朗文字典
        button2 = wx.Button(panel, wx.ID_ANY, pos=(300, 65), size=(100, 70), label="Ldoce\n朗文词典")
        button2.Bind(wx.EVT_BUTTON, self.tool2)

        # 查看 Thesaurus 索引典
        button3 = wx.Button(panel, wx.ID_ANY, pos=(400, 65), size=(100, 70), label="Thesaurus\n索引典")
        button3.Bind(wx.EVT_BUTTON, self.tool3)

        # 查看 cambridge 剑桥词典
        button4 = wx.Button(panel, wx.ID_ANY, pos=(500, 65), size=(100, 70), label="Cambridge\n剑桥词典")
        button4.Bind(wx.EVT_BUTTON, self.tool4)

        # 查看 merriam 韦氏在线词典
        button5 = wx.Button(panel, wx.ID_ANY, pos=(600, 65), size=(100, 70), label="Merriam\n韦氏在线词典")
        button5.Bind(wx.EVT_BUTTON, self.tool5)

        # 查看有道翻译
        button6 = wx.Button(panel, wx.ID_ANY, pos=(200, 135), size=(100, 70), label="Youdao\n有道翻译")
        button6.Bind(wx.EVT_BUTTON, self.tool6)

        # 查看百度翻译
        button7 = wx.Button(panel, wx.ID_ANY, pos=(300, 135), size=(100, 70), label="Baidu\n百度翻译")
        button7.Bind(wx.EVT_BUTTON, self.tool7)

        # 查看DeepL谷歌翻译
        button8 = wx.Button(panel, wx.ID_ANY, pos=(400, 135), size=(100, 70), label="DeepL\n谷歌翻译")
        button8.Bind(wx.EVT_BUTTON, self.tool8)

        # --以下为写作工具--
        lbl3 = wx.StaticText(panel, -1, "Writing Tools:\n写作工具", pos=(20, 300))  # 居中放置，略微偏左，保持美观
        font3 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False)  # 粗体
        lbl3.SetFont(font3)
        lbl3.SetForegroundColour('black')  # 用黑色

        # 查看LaTeX在线公式编辑器
        button9 = wx.Button(panel, wx.ID_ANY, pos=(200, 300), size=(100, 70), label="LaTeX\n公式编辑器")
        button9.Bind(wx.EVT_BUTTON, self.tool9)

        # 查看StackEdit在线markdown编辑器
        button10 = wx.Button(panel, wx.ID_ANY, pos=(300, 300), size=(100, 70), label="StackEdit\nMarkdown编辑器")
        button10.Bind(wx.EVT_BUTTON, self.tool10)

        # 查看LaTeX在线公式编辑器2
        button11 = wx.Button(panel, wx.ID_ANY, pos=(400, 300), size=(100, 70), label="LaTeX2\n公式编辑器2")
        button11.Bind(wx.EVT_BUTTON, self.tool11)

        # 查看csdn
        button12 = wx.Button(panel, wx.ID_ANY, pos=(500, 300), size=(100, 70), label="CSDN\n内附Markdown写作器")
        button12.Bind(wx.EVT_BUTTON, self.tool12)

        lbl4 = wx.StaticText(panel, -1, "~~~持续更新中~~~", pos=(250, 500))  # 居中放置，略微偏左，保持美观
        font4 = wx.Font(15, wx.DEFAULT, wx.NORMAL, wx.BOLD, underline=False)  # 粗体
        lbl4.SetFont(font4)
        lbl4.SetForegroundColour('black')  # 用黑色
        lbl4.SetBackgroundColour('white')  # 用白色

        # 添加开发者标识
        dev_lbl = wx.StaticText(panel, label="Developed by Yan Lecheng, Class 8, Grade 7,\n     Laoshan Experimental Junior Middle School\nV1.0.0", pos=(
            450, 500))
        dev_font = wx.Font(10, wx.FONTFAMILY_SCRIPT, wx.NORMAL, wx.LIGHT, underline=False)  # 楷体 粗体
        dev_lbl.SetFont(dev_font)
        dev_lbl.SetForegroundColour('#060408')  # 黑色

        # 设置退出按钮
        button13 = wx.Button(panel, wx.ID_ANY, pos=(650, 400), size=(80, 50), label="Quit 退出")
        button13.Bind(wx.EVT_BUTTON, self.quit)

    def quit(self, event):  # 退出函数
        self.Close()  # 关闭窗口

    def tool1(self, event):  # 查看牛津字典
        # 用在应用内打开在线网页的办法来实现
        self.frame1 = wx.Frame(None, title="Oxford - 牛津字典", size=(1100, 550), pos=(50, 10))  # 创建临时窗口
        # 创建一个Web视图组件
        self.browser1 = wx.html2.WebView.New(self.frame1)
        # 加载本地HTML文件
        self.browser1.LoadURL('https://dictionary.cambridge.org/')
        # 设置窗口大小
        self.frame1.SetSize((1320, 900))  # 本机电脑是1920 x 1200
        # 显示主窗口
        self.frame1.Show()

    def tool2(self, event):  # 查看朗文词典
        # 用在应用内打开在线网页的办法来实现
        self.frame2 = wx.Frame(None, title="Ldoce - 朗文词典", size=(1100, 550), pos=(50, 10))  # 创建临时窗口
        # 创建一个Web视图组件
        self.browser2 = wx.html2.WebView.New(self.frame2)
        # 加载本地HTML文件
        self.browser2.LoadURL('https://www.ldoceonline.com/')
        # 设置窗口大小
        self.frame2.SetSize((1320, 900))  # 本机电脑是1920 x 1200
        # 显示主窗口
        self.frame2.Show()

    def tool3(self, event):  # 查看索引典Thesaurus
        # 用在应用内打开在线网页的办法来实现
        self.frame3 = wx.Frame(None, title="Thesaurus - 索引典", size=(1100, 550), pos=(50, 10))  # 创建临时窗口
        # 创建一个Web视图组件
        self.browser3 = wx.html2.WebView.New(self.frame3)
        # 加载本地HTML文件
        self.browser3.LoadURL('https://Thesaurus.com/')
        # 设置窗口大小
        self.frame3.SetSize((1320, 900))  # 本机电脑是1920 x 1200
        # 显示主窗口
        self.frame3.Show()

    def tool4(self, event):  # 查看cambridge剑桥词典
        # 用在应用内打开在线网页的办法来实现
        self.frame4 = wx.Frame(None, title="Cambridge - 剑桥词典", size=(1100, 550), pos=(50, 10))  # 创建临时窗口
        # 创建一个Web视图组件
        self.browser4 = wx.html2.WebView.New(self.frame4)
        # 加载本地HTML文件
        self.browser4.LoadURL('https://dictionary.cambridge.org/')
        # 设置窗口大小
        self.frame4.SetSize((1320, 900))  # 本机电脑是1920 x 1200
        # 显示主窗口
        self.frame4.Show()

    def tool5(self, event):  # 查看merriam韦氏在线词典
        # 用在应用内打开在线网页的办法来实现
        self.frame5 = wx.Frame(None, title="Merriam - 韦氏在线词典", size=(1100, 550), pos=(50, 10))  # 创建临时窗口
        # 创建一个Web视图组件
        self.browser5 = wx.html2.WebView.New(self.frame5)
        # 加载本地HTML文件
        self.browser5.LoadURL('https://www.merriam-webster.com/')
        # 设置窗口大小
        self.frame5.SetSize((1320, 900))  # 本机电脑是1920 x 1200
        # 显示主窗口
        self.frame5.Show()

    def tool6(self, event):  # 查看有道翻译
        # 用在应用内打开在线网页的办法来实现
        self.frame6 = wx.Frame(None, title="Youdao - 有道翻译", size=(1100, 550), pos=(50, 10))  # 创建临时窗口
        # 创建一个Web视图组件
        self.browser6 = wx.html2.WebView.New(self.frame6)
        # 加载本地HTML文件
        self.browser6.LoadURL('https://fanyi.youdao.com/')
        # 设置窗口大小
        self.frame6.SetSize((1320, 900))  # 本机电脑是1920 x 1200
        # 显示主窗口
        self.frame6.Show()

    def tool7(self, event):  # 查看百度翻译
        # 用在应用内打开在线网页的办法来实现
        self.frame7 = wx.Frame(None, title="Baidu - 百度翻译", size=(1100, 550), pos=(50, 10))  # 创建临时窗口
        # 创建一个Web视图组件
        self.browser7 = wx.html2.WebView.New(self.frame7)
        # 加载本地HTML文件
        self.browser7.LoadURL('https://fanyi.baidu.com/')
        # 设置窗口大小
        self.frame7.SetSize((1320, 900))  # 本机电脑是1920 x 1200
        # 显示主窗口
        self.frame7.Show()

    def tool8(self, event):  # 查看deepl谷歌翻译
        # 用在应用内打开在线网页的办法来实现
        self.frame8 = wx.Frame(None, title="DeepL - 谷歌翻译", size=(1100, 550), pos=(50, 10))  # 创建临时窗口
        # 创建一个Web视图组件
        self.browser8 = wx.html2.WebView.New(self.frame8)
        # 加载本地HTML文件
        self.browser8.LoadURL('https://www.deepl.com/zh/translator/')
        # 设置窗口大小
        self.frame8.SetSize((1320, 900))  # 本机电脑是1920 x 1200
        # 显示主窗口
        self.frame8.Show()

    def tool9(self, event):  # 查看deepl谷歌翻译
        # 用在应用内打开在线网页的办法来实现
        self.frame9 = wx.Frame(None, title="LaTeX - 公式编辑器", size=(1100, 550), pos=(50, 10))  # 创建临时窗口
        # 创建一个Web视图组件
        self.browser9 = wx.html2.WebView.New(self.frame9)
        # 加载本地HTML文件
        self.browser9.LoadURL('https://latex.91maths.com/')
        # 设置窗口大小
        self.frame9.SetSize((1320, 900))  # 本机电脑是1920 x 1200
        # 显示主窗口
        self.frame9.Show()

    def tool10(self, event):  # 查看StackEdit在线markdown
        # 用在应用内打开在线网页的办法来实现
        self.frame10 = wx.Frame(None, title="StackEdit - 在线Markdown编辑器", size=(1100, 550), pos=(50, 10))  # 创建临时窗口
        # 创建一个Web视图组件
        self.browser10 = wx.html2.WebView.New(self.frame10)
        # 加载本地HTML文件
        self.browser10.LoadURL('https://itsfoss.com/stackedit-markdown-editor/')
        # 设置窗口大小
        self.frame10.SetSize((1320, 900))  # 本机电脑是1920 x 1200
        # 显示主窗口
        self.frame10.Show()

    def tool11(self, event):  # 查看latex公式编辑器2
        # 用在应用内打开在线网页的办法来实现
        self.frame11 = wx.Frame(None, title="LaTeX2 - 公式编辑器2", size=(1100, 550), pos=(50, 10))  # 创建临时窗口
        # 创建一个Web视图组件
        self.browser11 = wx.html2.WebView.New(self.frame11)
        # 加载本地HTML文件
        self.browser11.LoadURL('https://www.latexlive.com/')
        # 设置窗口大小
        self.frame11.SetSize((1320, 900))  # 本机电脑是1920 x 1200
        # 显示主窗口
        self.frame11.Show()

    def tool12(self, event):  # 查看CSDN
        # 用在应用内打开在线网页的办法来实现
        self.frame12 = wx.Frame(None, title="CSDN - 博客+写作工具", size=(1100, 550), pos=(50, 10))  # 创建临时窗口
        # 创建一个Web视图组件
        self.browser12 = wx.html2.WebView.New(self.frame12)
        # 加载本地HTML文件
        self.browser12.LoadURL('https://csdn.net')
        # 设置窗口大小
        self.frame12.SetSize((1320, 900))  # 本机电脑是1920 x 1200
        # 显示主窗口
        self.frame12.Show()


class WordTribe(wx.Frame):  # 主窗口类

    def __init__(self, superior):
        # 设置窗口基础信息
        wx.Frame.__init__(self, parent=superior, id=wx.ID_ANY,
                          title="Word Tribe - 单词部落", pos=(300, 100), size=(800, 650))
        # 设置窗口容器
        panel = wx.Panel(self, -1)

        # 设置主窗口界面
        lbl1 = wx.StaticText(panel, -1, "Word Tribe 单词部落", pos=(170, 20))  # 居中放置，略微偏左，保持美观
        font1 = wx.Font(30, wx.DECORATIVE, wx.ITALIC, wx.BOLD, underline=True)  # 古老英文字体 粗体 斜体 加下划线
        lbl1.SetFont(font1)
        lbl1.SetForegroundColour('#156DC4')  # 用靛蓝色

        # 设置一言，放英语励志名句
        get_sent_txt()  # 从 txt 文件中导入内容
        # 放置
        lbl2 = wx.StaticText(panel, label="一言", pos=(600, 90))  # 这里设置成类的成员变量是因为在别的地方还要用到它
        font2 = wx.Font(20, wx.FONTFAMILY_SCRIPT, wx.NORMAL, wx.BOLD, underline=True)  # 楷体 粗体
        lbl2.SetFont(font2)
        lbl2.SetForegroundColour("#37BE4A")  # 深一点的绿色
        lbl2.SetBackgroundColour("#FFFFFF")  # 白色

        sent = get_random_sent()
        self.lbl3 = wx.StaticText(panel, label=sent, pos=(500, 120))  # 这里设置成类的成员变量是因为在修改一言的函数里还要用到它
        font3 = wx.Font(15, wx.FONTFAMILY_SCRIPT, wx.NORMAL, wx.LIGHT, underline=False)  # 楷体 粗体
        self.lbl3.SetFont(font3)
        self.lbl3.SetForegroundColour('#060408')  # 黑色
        self.lbl3.SetBackgroundColour("#FFFFFF")  # 白色

        # 设置切换按钮
        button1 = wx.Button(panel, wx.ID_ANY, pos=(700, 85), size=(80, 35), label="Change It\n换一个")
        button1.Bind(wx.EVT_BUTTON, self.set_random_sent)

        # 设置积累新单词的按钮
        button2 = wx.Button(panel, wx.ID_ANY, pos=(35, 100), size=(220, 70), label="Add New Words 积累新单词")
        button2.Bind(wx.EVT_BUTTON, self.add_new_words)

        # 设置复习新单词的按钮
        button3 = wx.Button(panel, wx.ID_ANY, pos=(35, 200), size=(220, 70), label="Review Words 复习单词")
        button3.Bind(wx.EVT_BUTTON, self.review_words)

        # 设置背单词的按钮
        button4 = wx.Button(panel, wx.ID_ANY, pos=(35, 300), size=(220, 70), label="Word Competition 单词挑战")
        button4.Bind(wx.EVT_BUTTON, self.word_competition)

        # 设置查看背单词历史成绩的按钮
        button5 = wx.Button(panel, wx.ID_ANY, pos=(280, 330), size=(100, 50), label="History 历史成绩")
        button5.Bind(wx.EVT_BUTTON, self.show_history)

        # 设置查看工具库的按钮
        button6 = wx.Button(panel, wx.ID_ANY, pos=(35, 400), size=(220, 70), label="Tools 工具库")
        button6.Bind(wx.EVT_BUTTON, self.tools)

        # 为了使界面不那么空虚，添加一点装饰（后来填坑）
        # 添加开发者标识
        dev_lbl = wx.StaticText(panel, label="Developed by Yan Lecheng, Class 8, Grade 7,\n     Laoshan Experimental Junior Middle School\nV1.0.0", pos=(
            450, 500))
        dev_font = wx.Font(10, wx.FONTFAMILY_SCRIPT, wx.NORMAL, wx.LIGHT, underline=False)  # 楷体 粗体
        dev_lbl.SetFont(dev_font)
        dev_lbl.SetForegroundColour('#060408')  # 黑色

    def add_new_words(self, event):  # 添加新单词函数
        frame = AddNewWords(None)
        frame.Show(True)

    # 复习单词函数
    def review_words(self, event):
        frame = ReviewWords(None)
        frame.Show(True)

    # 单词挑战函数
    def word_competition(self, event):
        frame = WordCompetition(None)
        frame.Show(True)

    # 打开工具库函数
    def tools(self, event):
        frame = Tools(None)
        frame.Show(True)

    # 将随机的一言放置
    def set_random_sent(self, event):
        sent = get_random_sent()
        self.lbl3.SetLabel(sent)  # 更新文本框lbl3里的一言

    # 查看单词挑战历史的折线图
    def show_history(self, event):
        if len(history) > 0:  # 如果列表不为空
            x_axis_data = range(len(history))  # x
            y_axis_data = history  # y

            plt.plot(x_axis_data, y_axis_data, 'b*--', alpha=0.5, linewidth=1, label='acc')  # 'bo-'表示蓝色实线，数据点实心原点标注
            # plot中参数的含义分别是横轴值，纵轴值，线的形状（'s'方块,'o'实心圆点，'*'五角星   ...，颜色，透明度,线的宽度和标签 ，

            plt.legend()  # 显示上面的label
            plt.xlabel('Serial Number 序号')  # x_label
            plt.ylabel('Result 成绩')  # y_label
            plt.title('History 历史成绩')  # 标题

            mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体：解决plot不能显示中文问题
            mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

            # plt.ylim(-1,1)#仅设置y轴坐标范围
            plt.show()


if __name__ == '__main__':
    get_dict()  # 从文件中加载英文单词信息
    get_history()  # 从文件中读取用户历史挑战成绩

    app = wx.App()
    frame = WordTribe(None)
    frame.Show(True)
    app.MainLoop()
