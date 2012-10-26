#encoding=utf-8
'''
Created on 2012-10-26

@author: arch
'''

import threading
from os.path import dirname, abspath

'''
爬虫配置文件
全局变量
路径
列表
LogFile
'''

DIR_PREFIX = dirname(abspath(__file__))          #当前绝对路径
DOWN_PREFIX = DIR_PREFIX + '/down/'
LOG_PREFIX = DIR_PREFIX + '/log/'
LOG_IMG = LOG_PREFIX + 'img_log'
LOG_LINK = LOG_PREFIX + 'link_log'

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
