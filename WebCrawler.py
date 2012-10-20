#encoding=utf-8

import threading
import requests
import GetUrl
import urllib2
import os
from os.path import dirname, abspath
from bs4 import BeautifulSoup
import ParsUrl
import re

g_mutex = threading.Lock()   #互斥锁
g_pages = []        #下载的页面
g_pages_dict = {}
g_dledUrl = []      #下载过的页面
g_toDlUrl = []        #当前要下载的页面
g_failedUrl = []       #下载失败的页面
g_crawledUrl = []      #爬过的Url
g_dledPic = []
g_totalcount = 0    #下载过的页面数量

PREFIX = dirname(abspath(__file__))          #当前绝对路径
DOWN_PREFIX = PREFIX+'/down/'

RE_CN = re.compile(ur'[\u4e00-\u9fa5]+')     #匹配中文
RE_MOVIE = None                              #匹配视频 电影



class WebCrawler:

    def __init__(self, thNumber):
        self.thNumber = thNumber
        self.threadPool = []
        #TODO
        self.logfile = file(os.getcwd()+'/'+'log'+'/'+'#log.txt', 'w')
        print self.logfile

    def download(self, url, fileName):
        #print 'url',url
        #print 'fileName',fileName
        global g_crawledUrl

        Cth = CrawlerThread(url, fileName)
        self.threadPool.append(Cth)                   #加入到线程池
        Cth.start()

    def downloadAll(self):
        print 'download All'
        global g_toDlUrl
        global g_totalcount
        i = 0
        while i < len(g_toDlUrl):
            j = 0
            #启动多个下载线程
            while j < self.thNumber and i + j < len(g_toDlUrl):
                g_totalcount += 1    #进入循环则下载页面数加1
                self.download(g_toDlUrl[i+j], os.getcwd()+'/' + 'down_html'+ '/' + str(g_totalcount)+'.htm')
                #print 'Thread started:', i+j, '--File number = ', g_totalcount, '\n'
                j += 1
            i += j
            for th in self.threadPool:
                th.join(30)     #等待线程结束，30秒超时
            self.threadPool = []    #清空线程池
        g_toDlUrl = []    #清空列表

    def updateToDl(self):
        global g_toDlUrl
        global g_dledUrl
        newUrlList = []
        #for s in g_pages:
        #    newUrlList += GetUrl.GetUrl(s)   #######TODO GetUrl要具体实现
        g_toDlUrl = list(set(newUrlList) - set(g_dledUrl))    #提示unhashable
        print 'to dl url updated .....'
        print 'after updated ,size',len(g_toDlUrl)

    def Craw(self, entryUrl):    #这是一个深度搜索，到g_toDlUrl为空时结束
        g_toDlUrl.append(entryUrl)
        depth = 0
        while len(g_toDlUrl) != 0:
            depth += 1
            print '\n'
            print 'Searching depth ', depth, '...'
            print 'to Dl Url size', len(g_toDlUrl)
            #download all
            self.downloadAll()
            #update to download
            self.updateToDl()
            self.parseAll()
            #------------------------------------------------------------------#
            #content = '\n>>>Depth ' + str(depth)+':\n'
            #write log                        ##（该标记表示此语句用于写文件记录）
            #self.logfile.write(content)                                        ##
            #i = 0                                                              ##
            #while i < len(g_toDlUrl):                                          ##
            #    content = str(g_totalcount + i) + '->' + g_toDlUrl[i] + '\n'   ##
            #    self.logfile.write(content)                                    ##
            #    i += 1

            print 'craw Once -----------------------------------------'
            #------------------------------------------------------------------#
    def parseAll(self):
        global g_pages
        global g_pages_dict
        global g_crawledUrl
        #TODO 启动线程

        #for html_doc in g_pages:
        #    #self.parse_link(html_doc)
        #    self.parse_img(html_doc)
        #   self.parse_link(html_doc)
        print 'parse All'
        for key in g_pages_dict.keys():

            print 'parse Url :',key
            self.parse_img(key, g_pages_dict[key])
            self.parse_link(key, g_pages_dict[key])
            #TODO 删除
            g_crawledUrl.append(key)
            del(g_pages_dict[key])
        #print 'parse all'

#查找链接
    def parse_link(self, key, html_doc):
        global g_toDlUrl
        print 'parse link'
        soup = BeautifulSoup(html_doc, from_encoding="gb18030")  #解决中文乱码问题
        for link in soup.find_all('a', href=True):
        #for link in soup.find_all('a'):
            hurl = link['href']
            if (link):
                #print 'if link', link
                re_href = re.compile('href="(.*)" ')
                findhrefSrc = re.findall(re_href, str(link))
                if(findhrefSrc):
                    for i_href in findhrefSrc:
                 #       print 'fsfsfsf...fsfs',i_href
                        print 'haha'
            if (hurl):
                hurl = self.getUrl(key, hurl)
                print '--++--',hurl
            #print(hurl)  #TODO 加入到 to Download 列表
            #TODO 如果爬过，则跳过
                if hurl in g_crawledUrl:
            #    print 'crawled ...pass...'
                    continue
            #限定url 数量
            if(len(g_toDlUrl) >=5):
                break
            g_toDlUrl.append(hurl)
            print 'after parse link, size of to dl url',len(g_toDlUrl)


# 查找图片
    def parse_img(self, key, html_doc):
        global g_dledPic
        print 'parse_img'
        soup = BeautifulSoup(html_doc, from_encoding="gb18030")
        #print 'charset',soup.originalEncoding()
        result = soup.findAll(name='img')

        with open("%s/down.sh"%DOWN_PREFIX, "a") as down:

            patImgSrc1 = re.compile('src="(.*)" ')
            patImgSrc2 = re.compile('src2="(.*)" ')
            for imgsrc in result:
                findPatImgSrc1 = re.findall(patImgSrc1, str(imgsrc))
                findPatImgSrc2 = re.findall(patImgSrc2, str(imgsrc))
                findPatImgSrc = findPatImgSrc1 + findPatImgSrc2
                if(findPatImgSrc):
                    for i_src in findPatImgSrc:
                        if(i_src.endswith('jpg')):
                            #查找 图片是否下载过
                            if (i_src in g_dledPic):
                                continue
                            img_path = self.getUrl(key, i_src)
                            down.write('wget %s \n' % img_path)



    #转换 Url 绝对路径变相对路径
    def getUrl(self, key, hurl):
        hurl = hurl
        patten_1 = re.compile(r'http')
        match_1 = patten_1.match(hurl)
        if(not match_1):
            if key[-1] == '/':
                key_new = key[:-1]
                hurl = key_new + hurl
            else:
                hurl = key + hurl
        return hurl



class CrawlerThread(threading.Thread):
    def __init__(self, url, fileName):
        threading.Thread.__init__(self)
        self.url = url
        self.fileName = fileName

    def run(self):
        global g_mutex
        global g_failedUrl
        global g_dledUrl
        global g_pages
        global g_pages_dict

        try:
            print 'Thread run== \n'

            r = requests.get(self.url)
            if r.status_code == 200:
                f = urllib2.urlopen(self.url)
                #print 'url open sucess-----'
                s = f.read()
                #ParsUrl.getUrl(s)
                print 'url read sucess-----', self.url
                fout = file(self.fileName, 'w')
                fout.write(s)
                #print 'url content write sucess-----'
                if(s):
                       g_pages.append(s)     #加入到列表 中
                       g_pages_dict[self.url]=s
                fout.close()
        except:
            g_mutex.acquire()
            g_dledUrl.append(self.url)
            g_failedUrl.append(self.url)
            g_mutex.release()
            print 'Failed downloading and saving', self.url
            return None

        g_mutex.acquire()
        g_dledUrl.append(self.url)
        g_mutex.release()


#用于解析
class ParseThread(threading.Thread):
    def __init__(self, fileName):
        threading.Thread.__init__(self)
        self.fileName = fileName

    def run(self):
        print 'Parse run ====== \n'
        #解析url