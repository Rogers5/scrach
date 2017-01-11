#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import scrapy
import re
import urlparse
import cookielib
import urllib2
from scrapy.selector import Selector  
from datetime import datetime
from scrach.items import DmozItem
from bs4 import BeautifulSoup


class DmozSpider(scrapy.Spider):  
    name = "dmoz"  
    allowed_domains = [""]
    #new_url=None
    start_urls = [  
        
    ]
    headers_19lou={
        }
    headers_jxr={
        }

    cookies_19lou={
        '_Z3nY0d4C_':'37XgPK9h'
    }
    def start_requests(self):
        for url in self.start_urls:
            if url.find('0573') < 0:
                yield scrapy.Request(url,cookies=self.cookies_19lou,headers=self.headers_19lou)
            else:
                yield scrapy.Request(url,headers=self.headers_jxr)
    
    #通过一览页获取当日帖子列表
    def parse(self, response):
        url = urlparse.urlparse(response.url)
        sel = Selector(response)
        now = datetime.now()
        if url[1].find('0573') < 0:
            for site in sel.xpath('//tr'):
                catch_url = site.xpath('th[@class="title"]/div/a/@href').extract()
                datenow = site.xpath('td/span[@class="color9"]/text()').extract()
                if len(datenow)>0:
                    if now.strftime('%Y-%m-%d') == str(datenow[0][0:10]).strip():
                        catch_url[0] = catch_url[0].replace('http:','')
                        yield scrapy.Request('http:'+catch_url[0],headers=self.headers_19lou,callback=self.parse_contents)
        else:
            for site in sel.xpath('//tr'):
                catch_url = site.xpath('th/a[@class="s xst"]/@href').extract()
                datenow = site.xpath('td/em/span/text()').extract()
                if len(datenow)>0:
                    str_end = len(datenow[0])-6
                    if now.strftime('%Y-%m-%d').replace('-0','-') == str(datenow[0][0:str_end]).strip():
                        yield scrapy.Request(catch_url[0],headers=self.headers_jxr,callback=self.parse_contents)
    #解析帖子详细页内容
    def parse_contents(self,response):
        if response.status == 200:
            sel = Selector(response)
            url = urlparse.urlparse(response.url)
            if url[1].find('0573') < 0:
                try:
                    title = sel.xpath('//h1[@class="fl f14 link1"]/a/span/text()').extract()
                    con = sel.xpath('//td/div/div[@class="thread-cont"]').extract()
                    author = sel.xpath('//div[@class="side"]/div/div/a/span/text()').extract()
                    soup = BeautifulSoup(con[0], "lxml")
                    srcList = []
                    for link in soup.find_all('img'):
                        srcList.append('http:'+link.get('src').replace('http:','').replace('https:',''))
                    tid = url[2][18:36]
                    i = 0
                    for str_add in soup.find_all(re.compile("^img")):
                        str_add.replace_with('<br/><img max-width="720px" src="'+srcList[i]+'"/><br/>')
                        i = i + 1
                    #附件图片抓取
                    attImg = sel.xpath('//ul[@class="view-unit-bd"]').extract()
                    if len(attImg):
                        attsoup = BeautifulSoup(attImg[0], "lxml")
                        attsrcList = []
                        for link in attsoup.find_all('img'):
                            if link.get('src').find('middle') > 0:
                                attsrcList.append('http:'+link.get('src'))
                    item = DmozItem()
                    link = re.compile("\\[.*?\\]")
                    if soup.get_text().find('zzd-wrap') < 0:
                        item['title'] = str(title[0]).replace('-\xe6\x88\x91\xe4\xb9\x9f\xe6\x9d\xa5\xe4\xbe\x83\xe4\xbe\x83-\xe8\xae\xb2\xe7\xa9\xba\xe5\xa4\xb4-\xe5\x98\x89\xe5\x85\xb419\xe6\xa5\xbc','').replace('-\xe8\xae\xb2\xe7\xa9\xba\xe5\xa4\xb4-\xe5\x98\x89\xe5\x85\xb419\xe6\xa5\xbc','').replace('-\xe6\x97\xa9\xe7\x9f\xa5\xe9\x81\x93','').replace('-\xe6\x88\x91\xe7\x9c\x8b\xe8\xa7\x81\xe7\x9a\x84','').strip()
                        #item['content'] = soup.get_text().replace(u'\xa0',u'').replace('http://att2.citysbs.com','http://cs.jx09.com.cn/attachment/collect/19lou').strip()
                        item['tid'] = tid
                        if len(attImg):
	                        if len(attsrcList):
	                            item['images'] = '|'.join(attsrcList)
	                            item['content'] = re.sub(link,'',soup.get_text().replace(u'\xa0',u'').replace('http://att2.citysbs.com','http://cs.jx09.com.cn/attachment/collect/19lou').strip()) + '<br/><img src="' + item['images'].replace('|','"/><br/><br/><img src="').replace('http://att2.citysbs.com','http://cs.jx09.com.cn/attachment/collect/19lou') + '"/><br/>'
    	                        item['flag'] = '2'
    	                        item['author'] = author[0].strip()
    	                        yield item
                        else:
                            item['images'] = '|'.join(srcList)
                            item['content'] = re.sub(link,'',soup.get_text().replace(u'\xa0',u'').replace('http://att2.citysbs.com','http://cs.jx09.com.cn/attachment/collect/19lou').strip())
                            item['flag'] = '2'
                            item['author'] = author[0].strip()
                            yield item
                except Exception,e:
                    print e
            else:
                try:
                    title = sel.xpath('//title/text()').extract()
                    con = sel.xpath('//td[@class="t_f"]').extract()
                    author = sel.xpath('//div[@class="authi"]/a/text()').extract()
                    soup = BeautifulSoup(con[0], "lxml")
                    srcList = []
                    for link in soup.find_all('img'):
                        srcList.append(link.get('zoomfile'))
                    i = 0
                    for str_add in soup.find_all('ignore_js_op'):
	                    str_add.replace_with('<br/><img max-width="720px" src="'+srcList[i]+'"/><br/>')
	                    i = i + 1
                    tid = url[4][19:26]
                    item = DmozItem()
                    item['title'] = str(title[0]).replace(' - \xe7\x99\xbe\xe5\xa7\x93\xe8\xaf\x9d\xe9\xa2\x98 - \xe5\x98\x89\xe8\xae\xba\xe7\xbd\x91|\xe5\x98\x89\xe5\x85\xb4\xe4\xba\xba\xe8\xae\xba\xe5\x9d\x9b','').strip()
                    link = re.compile("\\[.*?\\]")
                    item['content'] = re.sub(link,'',soup.td.get_text().replace(u'\xa0',u'').replace('http://attach.0573ren.com','http://cs.jx09.com.cn/attachment/collect/jxr').strip())
                    item['tid'] = tid
                    item['images'] = '|'.join(srcList)
                    item['flag'] = '1'
                    item['author'] = author[0].strip()
                    yield item
                except Exception,e:
                    print e