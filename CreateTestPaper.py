import os
import sys
#print(os.path.dirname(__file__))
#os.chdir(os.path.dirname(__file__))
def app_path():
    """Returns the base application path."""
    if hasattr(sys, 'frozen'):
        # Handles PyInstaller
        return os.path.dirname(sys.executable)  #使用pyinstaller打包后的exe目录
    return os.path.dirname(__file__) # 正常运行路径
#sys.exit()
os.chdir(app_path())
import html2text
import re
import random
import mistune
from bs4 import BeautifulSoup
import shutil
import platform
#import lxml
#转中文数字
numdict = {1:"一",2:"二",3:"三",4:"四",5:"五",6:"六",7:"七",8:"八",9:"九",0:"零"} #个位数的字典
digitdict = {1:"十",2:"百",3:"千",4:"万"} #位称的字典
def maxdigit(number,count):
    num = number//10 #整除是//
    if num != 0:
        return maxdigit(num,count+1) #加上return才能进行递归
    else:
        digit_num = number%10 #digit_num是最高位上的数字
        return count,digit_num #count记录最高位
def No2Cn(number):
    max_digit,digit_num = maxdigit(number,0)
 
    temp = number
    num_list = [] #储存各位数字
    while temp > 0:
        position = temp%10
        temp //= 10 #整除是//
        num_list.append(position)
 
    chinese = ""
    if max_digit == 0: #个位数
        chinese = numdict[number]
    elif max_digit == 1: #十位数
        if digit_num == 1: #若十位上是1，则称为“十几”，而一般不称为“一十几”（与超过2位的数分开讨论的原因）
            chinese = "十"+numdict[num_list[0]]
        else:
            chinese = numdict[num_list[-1]]+"十"+numdict[num_list[0]]
    elif max_digit > 1: #超过2位的数
        while max_digit > 0:
            if num_list[-1] != 0: #若当前位上数字不为0，则加上位称
                chinese += numdict[num_list[-1]]+digitdict[max_digit]
                max_digit -= 1
                num_list.pop(-1)
            else: #若当前位上数字为0，则不加上位称
                chinese += numdict[num_list[-1]]
                max_digit -= 1
                num_list.pop(-1)
        chinese += numdict[num_list[-1]]
        
    if chinese.endswith("零"): #个位数如果为0，不读出
        chinese = chinese[:-1]
    if chinese.count("零") > 1: #中文数字中最多只有1个零
        count_0 = chinese.count("零")
        chinese = chinese.replace("零","",count_0-1)
    return chinese
## 转中文数字 
## 取得桌面地址
def GetDesktopPath():
    return os.path.join(os.path.expanduser("~"), 'Desktop')
## 判断是否数字
def is_number(string):
    pattern = re.compile(r'^[-+]?[0-9]*\.?[0-9]+([eE][-+]?[0-9]+)?$')
    return bool(pattern.match(string))
    
print('------------使用说明------------\n')
print('1. 题库为markdown文件,默认题库与程序放在同一文件夹下，并命名为`.source.md`\n')
print('2. ##### 五级标题为题型，有序列表为题号\n')
print('3. 题号后用`解析: `区分答案部分。!!这个很重要，否则无法导出答案!!\n')
print('4. LateX公式中不要有空格\n')
#print('5. LateX公式中包含的`\%`,`\#`,`\;`,`\,`,`\\`转义符号,进行html转换前要替换。')
"""sourceName = input('导入的题库')
sourceName += '.md'
while os.path.exists(sourceName)==False:
    sourceName = input('题库不存在，请重新输入题库名称')
    sourceName +='.md'"""
#sourceName = os.getcwd()+'/.source.md'
sourceName = input('输入题库绝对路径[使用默认题库回车]: ')
sourceName = sourceName.strip()
if sourceName.strip() == '':
    sourceName = os.getcwd()+'/.source.md'
while os.path.isfile(sourceName)==False:
    sourceName = input('题库不存在，请重新输入[使用默认题库回车]: ')
    sourceName = sourceName.strip()
    if sourceName.strip() == '':
        sourceName = os.getcwd()+'/.source.md'
        break
with open(sourceName, "r") as file:
    contents = file.read()
while contents.find("\n##### ") == -1:
    sourceName = input("题库为空或格式不符，请重新载入题库")
    sourceName = sourceName.strip()
    if sourceName.strip() == '':
        sourceName = os.getcwd()+'/.source.md'
        break
    while os.path.isfile(sourceName)==False:
        sourceName = input('题库不存在，请重新输入[使用默认题库回车]: ')
        sourceName = sourceName.strip()
        if sourceName.strip() == '':
            sourceName = os.getcwd()+'/.source.md'
            break
    with open(sourceName, "r") as file:
        contents = file.read()
    if contents.find("\n##### ") != -1:
        break

yon = input('Y/y 随机出卷；F/f 全部导出；C/c 取消')
while yon != "Y" and yon != 'y' and yon != 'C' and yon != 'c' and yon != 'F' and yon != 'f':
    print('输入错误，请重新输入\n')
    yon = input('Y/y 随机出卷；F/f 全部导出；C/c 取消')
if yon == 'C' or yon == 'c':
    sys.exit()
deskTop = GetDesktopPath()
title = input('请输入试卷名称: ')
while title.strip() == '':
    title = input('试卷名称不能为空，请重新输入: ')
"""while title.replace(' ','').find('source') != -1 :
    title = input('试卷名称与题库冲突，请重新输入: ')"""
while os.path.isdir(r''+deskTop+'/'+title):
    print("同名试题已经存在")
    judge = input("Y 覆盖，S 重新输入，N 取消")
    if judge == 'N' or judge == 'n':
        sys.exit()
    elif judge == "S" or judge == 's':
        title = input("输入新的名称")
        while title.strip() == '':
            title = input('试卷名称不能为空，请重新输入: ')
    elif judge == "Y" or judge == 'y':
        break
    else:
        print("输入错误，请重新输入")
        continue
nameQuestion = title+'.md'
nameAnswer = title+'Answer.md'
outDir = deskTop+'/'+title+'/'
if os.path.isdir(r''+outDir)==False:
    #print("不存在")
    os.mkdir(r''+outDir)
    os.mkdir(r''+outDir+'/img')
    #os.makedirs(r''+outDir+'img')
with open(outDir+nameQuestion,'w') as fileQ:
    fileQ.truncate(0)
with open(outDir+nameAnswer,'w') as fileA:
    fileA.truncate(0)
        
if yon == 'Y' or yon == 'y':
    fullScore = input('设置试卷总分: ')
    while is_number(fullScore)==False:
        fullScore = input("类型不对，请重新设置试卷总分: ")
    fullScore = int(fullScore)
    finishTime = input('设置考试时长(分钟): ')
    while is_number(finishTime)==False:
        finishTime = input("类型不对，请重新设置考试时长: ")
    t1 = '<div align="center" style="font-size:30px;font-weight:bolder">'+title+'</div>\n'
    t1 += '姓名: \t\t\t\t\t\t班级: \t\t\t\t\t\t考试日期: \t\t\t\t\t\t总分: '+str(fullScore)+'\t\t'+'时长: '+finishTime+'\t\t分数: \n\n'
    t1 += '***\n' 
    
if yon == 'F' or yon == 'f':
    t1 = '<div align="center" style="font-size:30px;font-weight:bolder">'+title+'</div>\n\n'
    t1 += '***\n\n'
        
t2 = '<div align="center" style="font-size:30px;font-weight:bolder">'+title+'</div>\n\n答案\n\n'
t2 += '***\n\n'   
with open(outDir+nameQuestion,'w') as fileQ:
    fileQ.write(t1)
with open(outDir+nameAnswer,'w') as fileA:
    fileA.write(t2)
       
#sourceName = os.getcwd()+'/.source.md'
filename = r''+sourceName
text = open(filename,encoding='utf8').read()
'''
text = text.replace("\%","-%")
text = text.replace("\#","-#")
text = text.replace("\_","downline")
text = text.replace("\;","-;")
text = text.replace("\,","-,")
text = text.replace("\\\\","@@")
'''
text = text.replace("*","myStar")
text = text.replace('\\','myEscape')
text = text.replace("         ","dubspace") #否则丢失格
#text = text.replace("    ","mytable") #否则丢失格
## 替换多个自定义字符
def strs_replace(mystr):
    '''
    mystr = mystr.replace("-%","\%")
    mystr = mystr.replace("-#","\#")
    mystr = mystr.replace("downline","\_")
    mystr = mystr.replace("-;","\;")
    mystr = mystr.replace("-,","\,")
    mystr = mystr.replace("@@","\\\\")
    '''
    mystr = mystr.replace("myEscape","\\")
    mystr = mystr.replace("myStar","*")
    mystr = mystr.replace("解析: ","")
    mystr = mystr.replace("dubspace","\t\t")
    mystr = mystr.replace("\\\\\n","\\\\")
    mystr = mystr.replace("待替换\n\n","\t")
    mystr = mystr.replace("\t$$\n","\t$$")
    mystr = mystr.replace("\n$$","$$")
    """
    #mystr = mystr.replace("mytable","\t")
    
    """
    return mystr
#%%
markdown = mistune.create_markdown(renderer='html')
html = markdown(text)
soup = BeautifulSoup(html,'html.parser')
firstHeader = soup.find("h5")
print("\n题库包含的题型如下:")
for tag in [firstHeader] + firstHeader.findNextSiblings():
    #print(soup.select('h5'))
    if tag.name == 'h5':
        print(tag.contents[0])
#print(firstHeader.contents[0])
#print(type(firstHeader))
i = 1
images = []
for tag in [firstHeader] + firstHeader.findNextSiblings():
    #print(soup.select('h5'))
    if tag.name == 'h5':
        #print(tag.contents[0])
        qType = tag.contents[0]
        questionType = '##### '+No2Cn(i)+qType[qType.rfind('、'):]
    if tag.name == 'ol':
        lis = list(tag.contents)
        #index1 = lis.index('\n',1)
        #if index1>0:
        #    del lis[index1]
        lis=[lis[i] for i in range(0,len(lis)) if lis[i]!="\n"]
        sums = len(lis)
        #print(len(lis))
        #yon = input('Y/y 抽取；N/n 跳过；C/c 全部跳过；F/f 全部导出')
        """if yon != 'N' and yon != 'n' and yon != "Y" and yon != 'y' and yon != 'C' and yon != 'c' and yon != 'F' and yon != 'f':
            print('输入错误，请重新输入\n')
            yon = input('Y/y 抽取；N/n 跳过；C/c 全部跳过；F/f 全部导出')"""
        if yon == 'F' or yon == 'f':
            number = sums
            questions = random.sample(lis,int(number))
            list1 = ''
            list2 = ''
            #print(len(questions))
            for value in questions:
                value = str(value)
                img = value.replace('&lt;','<')
                img = img.replace('&gt;','/>')
                soupimg = BeautifulSoup(img,'html.parser')
                #print(soupimg)
                for image in soupimg.findAll("img"):
                    images.append(image["src"])
                    #print(image["src"])
                qValue = value[0:value.rfind('<p>解析')]+'</li>'
                aValue = '<li>'+value[value.rfind('<p>解析'):]
                list1 += qValue+"\n"
                list2 += aValue+"\n"
                #之后的字符
                #print(value[value.rfind('<p>解析'):])
                #之前的字符
                #print(value[0:value.rfind('<p>解析')])
                #print(list1)
            list1 = questionType + '<ol>' + list1 + '</ol>'
            list2 = questionType + '<ol>' + list2 + '</ol>'
            list2 = list2.replace('参考方法\n$$','参考方法</p>\n<p>$$')
            list1 = list1.replace("</p>\n<p>","</p>待替换<p>")
            list2 = list2.replace('</p>\n<p>','</p>待替换<p>')
            
            qMarkdown = html2text.html2text(list1)
            qMarkdown = strs_replace(qMarkdown)
            
            aMarkdown = html2text.html2text(list2)
            aMarkdown = strs_replace(aMarkdown)
            #print(aMarkdown)
            #aMarkdown = aMarkdown.replace("#","\#")
            with open(outDir+nameQuestion,"a",encoding="utf8") as f1:
                f1.write(qMarkdown)
            with open(outDir+nameAnswer,"a",encoding="utf8") as f2:
                f2.write(aMarkdown)
            i +=1
        else:
            print('\n当前题型:'+qType[qType.rfind('、')+1:]+"共有"+str(sums)+"道; "+'剩余总分: '+str(fullScore)+'\n')
            yon = input('Y/y 确认；N/n 跳过；C/c 全部跳过')
            while yon != 'N' and yon != 'n' and yon != "Y" and yon != 'y' and yon != 'C' and yon != 'c':
                print('输入错误，请重新输入\n')
                yon = input('Y/y 确认；N/n 跳过；C/c 全部跳过')
            if yon == 'N' or yon == 'n':
                continue
            if yon == 'C' or yon == 'c':
                break
            else:
                number = input("请输入抽取的题目数量: ")
                while number.isdigit()==False:
                    number = input("类型不对，请重新输入抽取的题目数量: ")
                number = int(number)
                while int(number) > sums:
                    print("输入数量超过题库，无法生成！")
                    number = input("请重新输入抽取的题目数量: ")
                    while finishTime(number)==False:
                        number = input("类型不对，请重新输入抽取的题目数量: ")
                score = input("请输入每题分值: ")
                while is_number(score) == False:
                    score = input("类型不对，请重新设置每题分数: ")
                #print(random.sample(lis,int(number)))
                scores = int(number) * float(score)
                fullScore = fullScore - scores
                #print(type(scores))
                questionType += '$('+str(number)+'\\times'+str(score)+"="+str(scores)+')$\n'
                questions = random.sample(lis,int(number))
                list1 = ''
                list2 = ''
                #print(len(questions))
                for value in questions:
                    value = str(value)
                    img = value.replace('&lt;','<')
                    img = img.replace('&gt;','/>')
                    soupimg = BeautifulSoup(img,'html.parser')
                    #print(soupimg)
                    for image in soupimg.findAll("img"):
                        images.append(image["src"])
                        #print(image["src"])
                    qValue = value[0:value.rfind('<p>解析')]+'</li>'
                    aValue = '<li>'+value[value.rfind('<p>解析'):]
                    list1 += qValue+"\n"
                    list2 += aValue+"\n"
                    #之后的字符
                    #print(value[value.rfind('<p>解析'):])
                    #之前的字符
                    #print(value[0:value.rfind('<p>解析')])
                    #print(list1)
                list1 = questionType + '<ol>' + list1 + '</ol>'
                list2 = questionType + '<ol>' + list2 + '</ol>'
                list2 = list2.replace('参考方法\n$$','参考方法</p>\n<p>$$')
                list1 = list1.replace("</p>\n<p>","</p>待替换<p>")
                list2 = list2.replace('</p>\n<p>','</p>待替换<p>')
            
                qMarkdown = html2text.html2text(list1)
                qMarkdown = strs_replace(qMarkdown)
            
                aMarkdown = html2text.html2text(list2)
                aMarkdown = strs_replace(aMarkdown)
                #print(list2)
                with open(outDir+nameQuestion,"a",encoding="utf8") as f1:
                    f1.write(qMarkdown)
                with open(outDir+nameAnswer,"a",encoding="utf8") as f2:
                    f2.write(aMarkdown)
                i +=1
            
            #break

images = list(set(images))
#print(images)
for imgs in images:
    #print(outDir+imgs)
    dstimg = outDir+imgs
    if os.path.isfile(dstimg):
        os.remove(dstimg)
    shutil.copy2(os.getcwd()+'/'+imgs,dstimg)
    #print(img)
osType = 'open' if platform.system()=='Darwin' else 'start'
print('试题路径: '+outDir+nameQuestion)
os.system(osType+' '+outDir)
os.system(osType+' '+outDir+nameQuestion)
print('答案路径: '+outDir+nameAnswer)
#%%

