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
#import CrawlerConfig
import sys
#acii 编码
reload(sys)
sys.setdefaultencoding('utf-8')



g_mutex = threading.Lock()   #互斥锁
g_pages = []        #下载的页面
g_pages_dict = {}
g_dledUrl = []      #下载过的页面
g_toDlUrl = []        #当前要下载的页面
g_failedUrl = []       #下载失败的页面
g_crawledUrl = []      #爬过的Url
g_dledPic = []
g_totalcount = 0    #下载过的页面数量
g_maxDepth = 15  #最大搜索层数
th_lifeTime = 40
g_newUrlList = []

PREFIX = dirname(abspath(__file__))          #当前绝对路径
DOWN_PREFIX = PREFIX + '/down/'
LOG_PREFIX = PREFIX + '/log/'
LOG_IMG = LOG_PREFIX + 'img_log'


RE_CN = re.compile(ur'[\u4e00-\u9fa5]+')     #匹配中文
RE_MOVIE = None                              #匹配视频 电影


class WebCrawler:

    def __init__(self, thNumber):
        self.thNumber = thNumber
        self.threadPool = []
        #TODO
        self.logfile = file(LOG_PREFIX+'#log.txt', 'w')
        self.logfile_img = file(str(LOG_IMG), 'w')
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

        iDownloaded = 0
        while iDownloaded < len(g_toDlUrl):
            iThread = 0
            #启动多个下载线程
            while iThread < self.thNumber and iDownloaded + iThread < len(g_toDlUrl):
                iCurrentUrl = iThread + iDownloaded
                g_totalcount += 1    #进入循环则下载页面数加1
                self.download(g_toDlUrl[iCurrentUrl], os.getcwd()+'/' + 'down_html'+ '/' + str(g_totalcount)+'.htm')
                #print 'Thread started:', i+j, '--File number = ', g_totalcount, '\n'
                iThread += 1
            iDownloaded += iThread
            for th in self.threadPool:
                th.join(th_lifeTime)     #等待线程结束，30秒超时
            self.threadPool = []    #清空线程池
        g_toDlUrl = []    #清空列表

    def updateToDl(self):
        global g_toDlUrl
        global g_dledUrl
        global g_newUrlList
        ##广度
        g_toDlUrl = list(set(g_newUrlList)-set(g_dledUrl))
        #Clear Job
        g_newUrlList = []
        g_pages = []
        g_pages_dict = {}
        #print 'to dl url updated .....'
        #print 'after updated ,size',len(g_toDlUrl)

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

            self.parseAll()

            self.updateToDl()
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
        for key in g_pages_dict.keys():

            print 'parse Url :',key
            self.parse_img(key, g_pages_dict[key])
            self.parse_link(key, g_pages_dict[key])
            #TODO 删除
            g_crawledUrl.append(key)

#查找链接
    def parse_link(self, key, html_doc):
        global g_toDlUrl
        global g_newUrlList

        print 'parse link'
        soup = BeautifulSoup(html_doc, from_encoding="gb18030")  #解决中文乱码问题
        for link in soup.find_all('a', href=True):
        #for link in soup.find_all('a'):
            hurl = link['href']
            #if (link):
                #print 'if link', link
              #  re_href = re.compile('href="(.*)" ')
              #  findhrefSrc = re.findall(re_href, str(link))
              # if(findhrefSrc):
              #      for i_href in findhrefSrc:
                 #       print 'fsfsfsf...fsfs',i_href
                        #print 'haha'
            if (hurl):
                hurl = self.getUrl(key, hurl)
                print '--++--',hurl
            #print(hurl)  #TODO 加入到 to Download 列表
            #TODO 如果爬过，则跳过
                if hurl in g_crawledUrl:
            #    print 'crawled ...pass...'
                    continue
            #TODO 限定url 数量
            #if(len(g_toDlUrl) >=5):
            #    break
            g_newUrlList.append(hurl)
            #print 'after parse link, size of to dl url',len(g_toDlUrl)


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
                            # log imgage
                            log_content = "\n " + img_path
                            self.logfile_img.write(log_content)



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
        global g_currentDledUrl

        try:
            #print 'Thread run== \n'

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
                       #g_pages.append(s)     #加入到列表 中
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
        #g_currentDledUrl.append(self.url)
        g_mutex.release()


#用于解析
class ParseThread(threading.Thread):
    def __init__(self, fileName):
        threading.Thread.__init__(self)
        self.fileName = fileName

    def run(self):
        print 'Parse run ====== \n'
        #解析url