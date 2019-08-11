# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 20:33:58 2019

@author: Bohan
"""

import requests,json,hashlib,os,time
from pathlib import Path
from time import time, perf_counter
from fake_useragent import UserAgent
from xml.etree import ElementTree
#引入requests。
session = requests.session()

headers = {
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'
}
#add headers加请求头，前面有说过加请求头是为了模拟浏览器正常的访问，避免被反爬虫。
data={}
data['login']='liudab@163.com'     #Replace this with you ACCOUNTNAME in phytozome.jgi.doe.gov账户名
data['password']='19881227'       #Replace this with you PASSWORD in phytozome.jgi.doe.gov密码

def sign_in():
    global cookies_dict       #define cookies_dict to store dict form cookie
    global cookies_str
    cookies_dict={}
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


def createpath(file_path):
    try:
        if not os.path.exists(file_path):
            print ('文件夹',file_path,'不存在，重新建立')    #print ('folder',file_path,'is not exist, created it')
            #os.mkdir(file_path)
            os.makedirs(file_path)
    except IOError as e:
        print ('文件操作失败',e)      #print ('IOError',e)
    except Exception as e:
        print ('错误 ：',e)    #print ('Error',e)
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
    print('目前数据库中有以下版本:\n')         #print('The database have these Versions:\n')
    number=1
    for folderl1x in folderl1:     #遍历一级folder列表
        print(str(number)+'. '+folderl1x.attrib['name'])
        number=number+1
    pick=2           #pick=input('Pleas choose which version you want，input with number：\nFor example:2   After your input,pree Enter.\n')
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

def download_file_from_url(dl_url, file_name, md5, headers):
    file_path = Path(__file__).parent.joinpath(file_name)
    if file_path.exists():
        dl_size = file_path.stat().st_size        #if file exits, get downloaded file size
    else:
        dl_size = 0
    headers={
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36',
            'Cookie': cookies_dict}                          #include cookie into request headers
    headers['Range'] = f'bytes={dl_size}-'
    response = session.get(dl_url, stream=True)                          #use seesion get content via stream
    print('\n\n' + '*' * 30 + '下载信息' + '*' * 30)             #print('\n\n' + '*' * 30 + 'Downloading Information' + '*' * 30)
    try:
        total_size = int(response.headers['content-length'])                          #if server respond with content length, that could be continue download
        print(
            f'\n\n文件名称:{file_name}\t\t已下载文件大小:{dl_size / 1024 / 1024:.2f}M\t\t文件总大小:{total_size/1024/1024:.2f}M\n\n该文件支持断点续传\n')          #print(f'\n\nCurrent downloading:{file_name}\t\tDownloaded:{dl_size / 1024 / 1024:.2f}M\t\tThis file supports continue downloading, downloading......\n')
        start = perf_counter()
        data_count = 0
        count_tmp = 0
        start_time = time()
        with open(file_path, 'ab') as fp:                                     #if server respond with content length, that could be continue download, writ file with ab model, append
            for chunk in response.iter_content(chunk_size=512):
                data_count += len(chunk)
                now_pross = (data_count / total_size) * 100
                mid_time = time()
                if mid_time - start_time > 0.1:
                    speed = (data_count - count_tmp) / 1024 / (mid_time - start_time)
                    start_time = mid_time
                    count_tmp = data_count
                    print(
                        f"\rDownloading.........{now_pross:.2f}%\t{data_count//1024}Kb/{total_size//1024}Kb\t当前下载速度:{speed:.2f}Kb/s", end='')                    #f'\n\nDownloaded!Total used:{diff:.2f} seconds,  Average downloading speed:{speed:.2f}Kb/s!
                fp.write(chunk)
        
        end = perf_counter()
        diff = end - start
        speed = total_size/1024/diff
     
        print(
            f'\n\n下载完成!耗时:{diff:.2f}秒,  平均下载速度:{speed:.2f}Kb/s!\n文件路径:{file_path}\n')
    except KeyError:                                                           #if server respond with no content length, that means you should writ file with wb model, rewrite
        print(f'\n\n当前文件名称:{file_name}\t\t已下载文件大小:{dl_size / 1024 / 1024:.2f}M\t\t该文件服务器不支持断点续传,重新开始下载\n')         #print(f'\n\nCurrent downloading:{file_name}\t\tDownloaded:{dl_size / 1024 / 1024:.2f}M\t\tThis file doesn't supports continue downloading,restart to download this file.\n')
        start = perf_counter()
        data_count = 0
        count_tmp = 0
        start_time = time()
        with open(file_path, 'wb') as fp:
            for chunk in response.iter_content(chunk_size=512):
                data_count += len(chunk)
                mid_time = time()
                if mid_time - start_time > 0.1:
                    speed = (data_count - count_tmp) / 1024 / (mid_time - start_time)
                    start_time = mid_time
                    count_tmp = data_count
                    print(
                        f"\rDownloading.........\t{data_count//1024}Kb当前下载速度:{speed:.2f}Kb/s", end='')                    #f"\rDownloading.........\t{data_count//1024}KbCurrent downloading speed:{speed:.2f}Kb/s", end='')
                fp.write(chunk)
        
        end = perf_counter()
        diff = end - start
        speed = data_count/1024/diff
        print(
            f'\n\n下载完成!耗时:{diff:.2f}秒,  平均下载速度:{speed:.2f}Kb/s!\n文件路径:{file_path}\n')                    #f'\n\nDownloaded!Total used:{diff:.2f} seconds,  Average downloading speed:{speed:.2f}Kb/s!\nFile Path:{file_path}\n')
    fmd5=md5sum(file_name)
    if fmd5 == md5:                                              #check intergrity of file
        print('文件校验成功！')
    else:
        print('文件校验失败')

def paralleldownload():
    for j in range(int(len(tasklist))):
        try:
            if md5sum(tasklist[j][1]) != tasklist[j][2]:
                download_file_from_url(tasklist[j][0],tasklist[j][1],tasklist[j][2],headers)
            else:
                print('第'+str(j+1)+'个文件已存在且与本地文件一致')    #print('The No.'+str(j+1)+'file is already existing, and it don't need to be download again')
        except FileNotFoundError as e:
            print('共计'+str(int(len(tasklist)))+'个文件，'+'目前开始下载第'+str(j+1)+'个文件')  #print('There are total'+str(int(len(tasklist)))+'files，'+'We are downloading the number:'+str(j+1))
            download_file_from_url(tasklist[j][0],tasklist[j][1],tasklist[j][2],headers)

            




sign_in()
getxml()    #GETXML
gettasklist()   #GETtasklist

for i in range(int(len(fileurl)/4)):
    createpath(fileurl[i*4])     #解析官方xml文件，在根目录下创建所有子目录
paralleldownload()
