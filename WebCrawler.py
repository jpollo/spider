#encoding=utf-8

import threading
import GetUrl
import urllib

g_mutex = threading.Lock()
g_pages = []        #下载的页面
g_dledUrl = []      #下载过的页面
g_toDlUrl = []        #当前要下载的页面
g_failedUrl = []       #下载失败的页面
g_totoalCount = 0    #下载过的页面数量


class WebCrawler:

    def __init__(self, thNumber):
        self.thNum = thNumber

    def craw():
        while len(urlList) != 0:
            init_url_list()
            DownLoad_list()
            Update_list()
 
    def download(self, url, fileName):
        Cth = CrawlerThread(url, fileName)
        self.threadPool.append(Cth)
        Cth.start()
    
    def downloadAll(self):
        global g_toDlUrl
        global g_totalcount
        i = 0
        while i < len(g_toDlUrl):
            j = 0
            while j < self.threadNumber and i + j < len(g_toDlUrl):
                g_totalcount += 1    #进入循环则下载页面数加1
                self.download(g_toDlUrl[i+j],str(g_totalcount)+'.htm')
                print 'Thread started:',i+j,'--File number = ',g_totalcount
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
        for s in g_pages:
            newUrlList += GetUrl.GetUrl(s)   #######GetUrl要具体实现
        g_toDlUrl = list(set(newUrlList) - set(g_dledUrl))    #提示unhashable
                
    def Craw(self,entryUrl):    #这是一个深度搜索，到g_toDlUrl为空时结束
        g_toDlUrl.append(entryUrl)
        depth = 0
        while len(g_toDlUrl) != 0:
            depth += 1
            print 'Searching depth ',depth,'...\n\n'
            self.downloadAll()
            self.updateToDl()
            content = '\n>>>Depth ' + str(depth)+':\n'                         ##（该标记表示此语句用于写文件记录）
            self.logfile.write(content)                                        ##
            i = 0                                                              ##
            while i < len(g_toDlUrl):                                          ##
                content = str(g_totalcount + i) + '->' + g_toDlUrl[i] + '\n'   ##
                self.logfile.write(content)                                    ##
                i += 1                                                         ##





class CrawlerThread(threading.Thread):
    def __init__(self, url, fileName):
        threading.Thread.__init__(self)
        self.url = url
        self.fileName = fileName
        
    def run(self):
        global g_mutex
        global g_failedUrl
        global g_dledUrl
        try:
            f = urllib.urlopen(self.url)
            s = f.read()
            fout = file(self.fileName, 'w')
            fout.write(s)
            fout.close()
        except:
            g_mutex.acquire()
            g_dledUrl.append(self.url)
            g_failedUrl.append(self.url)
            g_mutex.release()
            print 'Failed downloading and saving', self.url
            return None
        
        g_mutex.acquire()
        g_pages.append(s)
        g_dledUrl.append(self.url)
        g_mutex.release()
       
        
