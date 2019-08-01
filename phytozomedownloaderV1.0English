# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 20:33:58 2019

@author: Bohan
"""

import requests,json,hashlib,os
from xml.etree import ElementTree
#引入requests。
session = requests.session()

headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}
#add headers加请求头，前面有说过加请求头是为了模拟浏览器正常的访问，避免被反爬虫。
data={}
data['login']='XXXX@XXXXX.com'     #Replace this with you ACCOUNTNAME in phytozome.jgi.doe.gov账户名
data['password']='XXXXXXXX'       #Replace this with you PASSWORD in phytozome.jgi.doe.gov密码

def sign_in():
    url = 'https://signon-old.jgi.doe.gov/signon/create'     #把登录的网址赋值给URL sign_in URL
    session.post(url, headers=headers, data=data)
    cookies_dict = requests.utils.dict_from_cookiejar(session.cookies)
    cookies_str = json.dumps(cookies_dict)
    f = open('cookies.txt', 'w')
    f.write(cookies_str)
    f.close()
     # 以上7行代码，是登录网站并存储cookies,signin the phytozome and save cookies
def cookies_read():
    cookies_txt = open('cookies.txt', 'r')
    cookies_dict = json.loads(cookies_txt.read())
    cookies = requests.utils.cookiejar_from_dict(cookies_dict)
    return (cookies)
    # 以上4行代码，是cookies读取,read local cookies

def md5sum(filepath):
    fd = open(filepath,"rb")  
    fcont = fd.read()
    fd.close()           
    fmd5 = str(hashlib.md5(fcont).hexdigest())
    return fmd5
#定义一个md5sum函数，返回校验值,def a function md5sum, to check and return md5 value of a certain file

def sdownloadfile(link,filepath,md5):
    print('file:'+link+' is downloading') as englsih user      #you can use print('file:'+link+' is downloading') as englsih user
    downloadfile=session.get(link)
    with open(filepath,'wb') as f:
        f.write(downloadfile.content)
    fmd5=md5sum(filepath)
    if fmd5==md5:
        print('file:'+filepath+' is downloaded and it is intact！')    #you can use print('file:'+filepath+' is downloaded and it is intact！') as englsih user
    else:
        print('file:'+filepath+' is failed in md5sum！')         #you can use print('file:'+filepath+' is failed in md5sum！') as englsih user
#定义一个sdownloadfile函数，从link下载文件，存储到fiprint('file:'+filepath+' is failed in md5sum！')lepath，并利用md5值对下载完成的文件进行MD5校验, download file and check it integrity

def createpath(file_path):
    try:
        if not os.path.exists(file_path):
            print ('folder',file_path,'is not exist, created it')    #print ('folder',file_path,'is not exist, created it')
            #os.mkdir(file_path)
            os.makedirs(file_path)
    except IOError as e:
        print ('IOError',e)      #print ('IOError',e)
    except Exception as e:
        #print ('Error',e)    #print ('Error',e)
#定义一个createpath函数，检测所在目录是否存在，不存在则建立文件夹，check filedirectory exisit or not, if not create that folder
 

def getxml():
    global fileurl
    fileurl=[]
    PHYTOALL='Phytozome'
    xmldata=session.get('https://genome.jgi.doe.gov/portal/ext-api/downloads/get-directory?organism=Phytozome&organizedByFileType=false')
    #输入API指定的版本名称
    with open('./'+PHYTOALL+'.xml','wb') as xf:
        xf.write(xmldata.content)
    #下载对应版本的官方xml文件
    xmlDoc = ElementTree.parse('./'+PHYTOALL+'.xml')    #读取并使用ElementTree解析PhytozomeV12.xml文件，并命名为xmlDoc
    folderl1 = xmlDoc.findall('folder')    #使用findall功能找出子一级folder列表
    print('The database have these Versions:\n')        #print('The database have these Versions:\n')
    number=1
    for folderl1x in folderl1:     #遍历一级folder列表
        print(str(number)+'. '+folderl1x.attrib['name'])
        number=number+1
    pick=input('Pleas choose which version you want，input with number：\nFor example:2   After your input,pree Enter\n')           #pick=input('Pleas choose which version you want，input with number：\nFor example:2   After your input,pree Enter.\n')
    folderl1name =folderl1[int(pick)-1]
    folderl2 = folderl1name.findall('folder')     #使用findall功能找出子二级folder列表
    folderl2f = folderl1name.findall('file')
    for folderl2fname in folderl2f:
        folderpathl2 = "./"+ str(folderl1name.get('name'))+ "/" 
        fileurl.append(folderpathl2)
        fileurl.append(folderl2fname.get('filename'))
        fileurl.append('https://genome.jgi.doe.gov'+folderl2fname.get('url'))
        fileurl.append(folderl2fname.get('md5'))
    for folderl2name in folderl2:    #遍历二级folder列表
        folderl3 = folderl2name.findall('folder')    #使用findall功能找出子三级folder列表
        folderl3f = folderl2name.findall('file')
        for folderl3fname in folderl3f:
            folderpathl3 = "./"+ str(folderl1name.get('name'))+"/"+ str(folderl2name.get('name')) +  "/" 
            fileurl.append(folderpathl3)
            fileurl.append(folderl3fname.get('filename'))
            fileurl.append('https://genome.jgi.doe.gov'+folderl3fname.get('url'))
            fileurl.append(folderl3fname.get('md5'))
        for folderl3name in folderl3:     #遍历三级folder列表
            folderl4 = folderl3name.findall('folder')    #使用findall功能找出子4级folder列表
            folderl4f = folderl3name.findall('file')
            for folderl4fname in folderl4f:
                folderpathl4 = "./"+ str(folderl1name.get('name'))+"/"+ str(folderl2name.get('name')) +  "/" +str(folderl3name.get('name'))+  "/"
                fileurl.append(folderpathl4)
                fileurl.append(folderl4fname.get('filename'))
                fileurl.append('https://genome.jgi.doe.gov'+folderl4fname.get('url'))
                fileurl.append(folderl4fname.get('md5'))
            for folderl4name in folderl4:     #遍历4级folder列表
                folderl5 = folderl4name.findall('folder')    #使用findall功能找出子5级folder列表
                folderl5f = folderl4name.findall('file')
                for folderl5fname in folderl5f:
                    folderpathl5 = "./"+ str(folderl1name.get('name')) + "/" + str(folderl2name.get('name')) + "/" + str(folderl3name.get('name')) + "/"+ str(folderl4name.get('name')) + "/"
                    fileurl.append(folderpathl5)
                    fileurl.append(folderl5fname.get('filename'))
                    fileurl.append('https://genome.jgi.doe.gov'+folderl5fname.get('url'))
                    fileurl.append(folderl5fname.get('md5'))
    file = open("./genome.links","w")
    file.write(str(fileurl))
    file.close()
    return fileurl
#解析官方xml文件，将对应文件名称、路径以及MD5值存取至genom.links文件，格式为列表形式，4个数值循环存储，1路径，2文件名，3URL，4MD5值

def gettasklist():
    global tasklist
    tasklist={}
    for i in range(int(len(fileurl)/4)):
        onefilelist=[]
        onefilelist.append(fileurl[i*4+2])
        onefilelist.append(fileurl[i*4]+fileurl[i*4+1])
        onefilelist.append(fileurl[i*4+3])
        tasklist[i]=onefilelist
    return tasklist
#合并文件路径和文件名，合成tasklist,格式为1URL,2路径+文件名,3MD5值

sign_in()    #登录
getxml()    #GETXML
gettasklist()   #GETtasklist
for i in range(int(len(fileurl)/4)):
    createpath(fileurl[i*4])     #解析官方xml文件，在根目录下创建所有子目录

def paralleldownload():
    for j in range(int(len(tasklist))):
        try:
            if md5sum(tasklist[j][1]) != tasklist[j][2]:
                sdownloadfile(tasklist[j][0],tasklist[j][1],tasklist[j][2])
                print('There are total'+str(int(len(tasklist)))+'files，'+'We are downloading the number:'+str(j+1))  #print('There are total'+str(int(len(tasklist)))+'files，'+'We are downloading the number:'+str(j+1))
            else:
                print('The No.'+str(j+1)+'file is already existing, and it don't need to be download again')    #print('The No.'+str(j+1)+'file is already existing, and it don't need to be download again')
        except FileNotFoundError as e:
            sdownloadfile(tasklist[j][0],tasklist[j][1],tasklist[j][2])
            print('There are total'+str(int(len(tasklist)))+'files，'+'We are downloading the number:'+str(j+1))  #print('There are total'+str(int(len(tasklist)))+'files，'+'We are downloading the number:'+str(j+1))
paralleldownload()
        
        
