#encoding=utf-8

#文件 批量读取 url

import WebCrawler

if __name__ == '__main__':

    print '==========Start============'
#    url = raw_input('set url(Example:www.jasonllinux.com): \n')
#    thNum = int(raw_input('set num of threads： \n'))
    #url = 'http://www.2tu.cc/'
    #url = 'http://mobile.zol.com.cn/photo.shtml'
    #url = 'http://dcbbs.zol.com.cn/'
    url = 'http://www.moko.cc/'
    #url = 'http://www.mmeinv.com/'
    thNum = 5
    #print 'url',url
    #print 'thNum',thNum

    wc = WebCrawler.WebCrawler(thNum)
    wc.Craw(url)
