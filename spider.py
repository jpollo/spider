import requests
from os.path import dirname, abspath
from extract import extract, extract_all

import re

RE_CN = re.compile(ur'[\u4e00-\u9fa5]+')
PREFIX = dirname(abspath(__file__))

with open("%s/down.bat"%PREFIX, "w") as down:
    for i in xrange(1, 396):
       for url in ('http://www.luoo.net/radio/radio%s/mp3.xml'%i, 'http://www.luoo.net/radio/radio%s/mp3player.xml'%i):
            r = requests.get(url)
            print url
            print r.status_code
            if r.status_code == 200:
                for path, name in zip(extract_all('path="', '"', r.content), extract_all('title="', '"', r.content)):
                            if RE_CN.match(name.decode('utf-8', 'ignore')):
                                print "to wget"
                                down.write('wget %s -O "%s/%s.mp3"\n' % (path, PREFIX, name.decode('utf-8', "ignore").encode("gb18030", "ingore")))
                            break