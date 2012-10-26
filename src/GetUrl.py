#encoding=utf-8
'''
Created on 2012-10-26

@author: arch
'''

'''
它里面的GetUrl从一个存有网页内容的字符串中获取所有url并以一个list返回
'''
urlSep = ['<','>','\\','(',')', r'"', ' ', '\t', '\n']
urlTag = ['http://']

def is_sep(ch):
    for c in urlSep:
        if c == ch:
            return True
    return False

def find_first_sep(i,s):
    while i < len(s):
        if is_sep(s[i]):
            return i
        i+=1
    return len(s)

def GetUrl(strPage):
    rtList = []
    for tag in urlTag:
        i = 0
        i = strPage.find(tag, i, len(strPage))
        while i != -1:
            begin = i
            end = find_first_sep(begin+len(tag),strPage)
            rtList.append(strPage[begin:end])
            i = strPage.find(tag, end, len(strPage))

    return rtList

def getlink1(data):
    pass