#encoding=utf-8

from bs4 import BeautifulSoup

#正则表达式匹配

def getData(html_doc):
    soup = BeautifulSoup(html_doc)
    print soup.prettify()


def getUrl(html_doc):
    soup = BeautifulSoup(html_doc)
    for link in soup.find_all('a'):
        print(link.get('href'))
