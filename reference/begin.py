from bs4 import BeautifulSoup
import urllib

#web_site = raw_input("Input the website: ")
#print web_site
#f = urllib.urlopen('web_site')
f = urllib.urlopen('http://www.qq.com')
s = f.read()
print s
