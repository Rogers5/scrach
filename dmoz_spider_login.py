#coding=utf-8
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
import scrapy
import re
import urlparse
import base64
from scrapy.selector import Selector  
from datetime import datetime
from scrach.items import DmozItem
from bs4 import BeautifulSoup
from scrapy.http import Request, FormRequest

class DmozSpider(scrapy.Spider):  
    name = "dmoz"  
    allowed_domains = ["jiaxing.19lou.com"]
    #new_url=None
    start_urls = [  
        #"http://www.0573ren.com/forum-5-1.html"
        "http://jiaxing.19lou.com/forum-778-1.html?order=createdat"
        #"http://jiaxing.19lou.com/forum-778-thread-225621481236505467-1-1.html"
        #"http://www.0573ren.com/forum.php?mod=forumdisplay&fid=194&filter=author&orderby=dateline"
        #"http://www.0573ren.com/forum.php?mod=viewthread&tid=1509210&extra=page%3D1%26filter%3Dauthor%26orderby%3Ddateline"
    ]
    headers_19lou={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,ja;q=0.2',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0',
        'Cookie':'BIGipServersbs_jiaxing_pool=2717974794.20480.0000; _DM_S_=30bc1a1bb2474ca5089f16b45068d89d; f8big=ip48; _Z3nY0d4C_=37XgPK9h; bdshare_firstime=1477888582768; PHPSESSID=41a51348461be79b79cb43bc4c9a55db; BIGipServertopic_pool=1997209866.20480.0000; reg_source=jiaxing.19lou.com; reg_first=http%253A//www.19lou.com/; Hm_lvt_5185a335802fb72073721d2bb161cd94=1479113811; Hm_lpvt_5185a335802fb72073721d2bb161cd94=1479113811; reg_step=5; fr_adv_last=crown_thread_pc; fr_adv=bbs_top_20161031_224501477869714609; _DM_SID_=62e6f52501ffeb15d252738ed15414a1; screen=841; _dm_tagnames=%5B%7B%22k%22%3A%22%E5%98%89%E5%85%B4%22%2C%22c%22%3A20%7D%2C%7B%22k%22%3A%22%E6%97%A9%E7%9F%A5%E9%81%93%22%2C%22c%22%3A17%7D%2C%7B%22k%22%3A%22%E5%A4%AA%E9%98%B3%22%2C%22c%22%3A13%7D%2C%7B%22k%22%3A%22%E8%AE%B0%E8%80%85%22%2C%22c%22%3A13%7D%2C%7B%22k%22%3A%22%E7%A9%BA%E9%97%B4%22%2C%22c%22%3A13%7D%2C%7B%22k%22%3A%22%E7%A9%BA%E8%B0%83%22%2C%22c%22%3A13%7D%2C%7B%22k%22%3A%22%E7%8E%AF%E4%BF%9D%22%2C%22c%22%3A13%7D%2C%7B%22k%22%3A%22%E6%89%8B%E6%9C%BA%22%2C%22c%22%3A12%7D%2C%7B%22k%22%3A%22%E5%B0%8F%E5%8C%BA%22%2C%22c%22%3A12%7D%2C%7B%22k%22%3A%22%E8%88%92%E9%80%82%22%2C%22c%22%3A12%7D%2C%7B%22k%22%3A%22Calvin%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22Klein%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22%E5%98%89%E5%85%B4%E6%B6%88%E6%81%AF%22%2C%22c%22%3A20%7D%2C%7B%22k%22%3A%22%E5%98%89%E5%85%B4%E6%96%B0%E9%97%BB%E7%BD%91%22%2C%22c%22%3A20%7D%2C%7B%22k%22%3A%22%E5%98%89%E5%85%B4%E6%9C%80%E6%96%B0%E6%96%B0%E9%97%BB%22%2C%22c%22%3A20%7D%2C%7B%22k%22%3A%22%E7%88%86%E6%96%99%22%2C%22c%22%3A7%7D%2C%7B%22k%22%3A%22%E6%88%B7%E5%8F%A3%22%2C%22c%22%3A3%7D%2C%7B%22k%22%3A%22%E6%AF%81%E5%AE%B9%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E6%8D%B7%E8%B1%B9%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E8%B1%AA%E8%BD%A6%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%96%9C%E5%89%A7%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E6%B5%99%E6%B1%9F%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%B0%8F%E5%AD%A6%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E6%95%B0%E5%AD%A6%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%B0%8F%E5%A4%AB%E5%A6%BB%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E8%A1%8C%E6%94%BF%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E6%B5%B7%E5%AE%81%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E9%94%80%E5%94%AE%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E6%97%85%E9%A6%86%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%89%8D%E5%8F%B0%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E4%B8%88%E6%AF%8D%E5%A8%98%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E7%A6%BB%E5%A9%9A%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E7%8C%A5%E4%BA%B5%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E6%88%91%E7%9C%8B%E8%A7%81%E7%9A%84%22%2C%22c%22%3A1%7D%5D; Hm_lvt_e2f79d52e017ad2831fdfc0084d9ad64=1480554756; Hm_lpvt_e2f79d52e017ad2831fdfc0084d9ad64=1480568670; JSESSIONID=4AB9F4CE7A9D1CE20AFECF124E64753D; _dm_userinfo=%7B%22uid%22%3A0%2C%22stage%22%3A%22%E5%B0%8F%E5%AD%A6%22%2C%22city%22%3A%22%22%2C%22ip%22%3A%22106.184.5.113%22%2C%22sex%22%3A%222%22%2C%22frontdomain%22%3A%22jiaxing.19lou.com%22%2C%22category%22%3A%22%E6%88%BF%E4%BA%A7%2C%E5%AE%B6%E5%B1%85%2C%E6%95%99%E8%82%B2%2C%E6%83%85%E6%84%9F%2C%E5%A9%9A%E5%BA%86%2C%E6%B1%82%E8%81%8C%2C%E6%97%85%E6%B8%B8%22%7D; pm_count=%7B%22pc_allCity_threadView_button_adv_190x205_1%22%3A5%7D; dayCount=%5B%7B%22id%22%3A78784%2C%22count%22%3A5%7D%5D',
        'Host':'jiaxing.19lou.com',
        'Referer':'http://jiaxing.19lou.com/forum-778-1.html?order=createdat',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }

    headers_19lou_login={
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip,deflate,sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,ja;q=0.2',
        'Connection':'keep-alive',
        'Cache-Control':'max-age=0',
        'Cookie':'BIGipServersbs_jiaxing_pool=2717974794.20480.0000; _DM_S_=30bc1a1bb2474ca5089f16b45068d89d; f8big=ip48; _Z3nY0d4C_=37XgPK9h; bdshare_firstime=1477888582768; PHPSESSID=41a51348461be79b79cb43bc4c9a55db; BIGipServertopic_pool=1997209866.20480.0000; reg_source=jiaxing.19lou.com; reg_first=http%253A//www.19lou.com/; Hm_lvt_5185a335802fb72073721d2bb161cd94=1479113811; Hm_lpvt_5185a335802fb72073721d2bb161cd94=1479113811; reg_step=5; fr_adv_last=crown_thread_pc; fr_adv=bbs_top_20161031_224501477869714609; _DM_SID_=62e6f52501ffeb15d252738ed15414a1; screen=841; _dm_tagnames=%5B%7B%22k%22%3A%22%E5%98%89%E5%85%B4%22%2C%22c%22%3A20%7D%2C%7B%22k%22%3A%22%E6%97%A9%E7%9F%A5%E9%81%93%22%2C%22c%22%3A17%7D%2C%7B%22k%22%3A%22%E5%A4%AA%E9%98%B3%22%2C%22c%22%3A13%7D%2C%7B%22k%22%3A%22%E8%AE%B0%E8%80%85%22%2C%22c%22%3A13%7D%2C%7B%22k%22%3A%22%E7%A9%BA%E9%97%B4%22%2C%22c%22%3A13%7D%2C%7B%22k%22%3A%22%E7%A9%BA%E8%B0%83%22%2C%22c%22%3A13%7D%2C%7B%22k%22%3A%22%E7%8E%AF%E4%BF%9D%22%2C%22c%22%3A13%7D%2C%7B%22k%22%3A%22%E6%89%8B%E6%9C%BA%22%2C%22c%22%3A12%7D%2C%7B%22k%22%3A%22%E5%B0%8F%E5%8C%BA%22%2C%22c%22%3A12%7D%2C%7B%22k%22%3A%22%E8%88%92%E9%80%82%22%2C%22c%22%3A12%7D%2C%7B%22k%22%3A%22Calvin%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22Klein%22%2C%22c%22%3A2%7D%2C%7B%22k%22%3A%22%E5%98%89%E5%85%B4%E6%B6%88%E6%81%AF%22%2C%22c%22%3A20%7D%2C%7B%22k%22%3A%22%E5%98%89%E5%85%B4%E6%96%B0%E9%97%BB%E7%BD%91%22%2C%22c%22%3A20%7D%2C%7B%22k%22%3A%22%E5%98%89%E5%85%B4%E6%9C%80%E6%96%B0%E6%96%B0%E9%97%BB%22%2C%22c%22%3A20%7D%2C%7B%22k%22%3A%22%E7%88%86%E6%96%99%22%2C%22c%22%3A7%7D%2C%7B%22k%22%3A%22%E6%88%B7%E5%8F%A3%22%2C%22c%22%3A3%7D%2C%7B%22k%22%3A%22%E6%AF%81%E5%AE%B9%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E6%8D%B7%E8%B1%B9%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E8%B1%AA%E8%BD%A6%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%96%9C%E5%89%A7%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E6%B5%99%E6%B1%9F%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%B0%8F%E5%AD%A6%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E6%95%B0%E5%AD%A6%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%B0%8F%E5%A4%AB%E5%A6%BB%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E8%A1%8C%E6%94%BF%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E6%B5%B7%E5%AE%81%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E9%94%80%E5%94%AE%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E6%97%85%E9%A6%86%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E5%89%8D%E5%8F%B0%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E4%B8%88%E6%AF%8D%E5%A8%98%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E7%A6%BB%E5%A9%9A%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E7%8C%A5%E4%BA%B5%22%2C%22c%22%3A1%7D%2C%7B%22k%22%3A%22%E6%88%91%E7%9C%8B%E8%A7%81%E7%9A%84%22%2C%22c%22%3A1%7D%5D; Hm_lvt_e2f79d52e017ad2831fdfc0084d9ad64=1480554756; Hm_lpvt_e2f79d52e017ad2831fdfc0084d9ad64=1480568670; JSESSIONID=4AB9F4CE7A9D1CE20AFECF124E64753D; _dm_userinfo=%7B%22uid%22%3A0%2C%22stage%22%3A%22%E5%B0%8F%E5%AD%A6%22%2C%22city%22%3A%22%22%2C%22ip%22%3A%22106.184.5.113%22%2C%22sex%22%3A%222%22%2C%22frontdomain%22%3A%22jiaxing.19lou.com%22%2C%22category%22%3A%22%E6%88%BF%E4%BA%A7%2C%E5%AE%B6%E5%B1%85%2C%E6%95%99%E8%82%B2%2C%E6%83%85%E6%84%9F%2C%E5%A9%9A%E5%BA%86%2C%E6%B1%82%E8%81%8C%2C%E6%97%85%E6%B8%B8%22%7D; pm_count=%7B%22pc_allCity_threadView_button_adv_190x205_1%22%3A5%7D; dayCount=%5B%7B%22id%22%3A78784%2C%22count%22%3A5%7D%5D',
        'Host':'jiaxing.19lou.com',
        'Referer':'http://jiaxing.19lou.com/login',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }

    cookies_19lou={
        '_Z3nY0d4C_':'37XgPK9h'
    }

    def start_requests(self):
        for url in self.start_urls:
            if url.find('0573') < 0:
                # print 'Preparing login'
                # #下面这句话用于抓取请求网页后返回网页中的_xsrf字段的文字, 用于成功提交表单
                # #FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
                # #登陆成功后, 会调用after_login回调函数
                # return [FormRequest.from_response(response,   
                #                     formdata = {
                #                     'userName': '13857395225',
                #                     'userPass': '8698b92d95506f8d3e9a6fc5834b9d51',
                #                     'remember': '1',
                #                     'ssl': 'true',
                #                     'refererUrl':'aHR0cDovL2ppYXhpbmcuMTlsb3UuY29tL2ZvcnVtLTc3OC0xLmh0bWw=',
                #                     'checked':'0'
                #                     },
                #                     callback = self.after_login
                #                     )]
                #yield scrapy.Request(url,cookies=self.cookies_19lou,headers=self.headers_19lou)
                yield scrapy.Request("https://jiaxing.19lou.com/login",cookies=self.cookies_19lou,headers=self.headers_19lou_login,callback = self.post_login)
            else:
                yield scrapy.Request(url,headers=self.headers_jxr)
        # yield scrapy.Request("https://jiaxing.19lou.com/login",cookies=self.cookies_19lou,headers=self.headers_19lou, callback = self.post_login)

    def post_login(self, response):
        # yield scrapy.Request(url,cookies=self.cookies_19lou,headers=self.headers_19lou)
        print 'Preparing login'
                #下面这句话用于抓取请求网页后返回网页中的_xsrf字段的文字, 用于成功提交表单
                #FormRequeset.from_response是Scrapy提供的一个函数, 用于post表单
                #登陆成功后, 会调用after_login回调函数
        return [FormRequest.from_response(response,   
                            formdata = {
                            'userName': '13857395225',
                            'userPass': '8698b92d95506f8d3e9a6fc5834b9d51',
                            'remember': '1',
                            'ssl': 'true',
                            'refererUrl':'aHR0cDovL2ppYXhpbmcuMTlsb3UuY29tL2ZvcnVtLTc3OC0xLmh0bWw=',
                            'checked':'0'
                            # 'geetest_challenge':'a9c0486fe318ad5ff33733713379aa45lh',
                            # 'geetest_validate':'38aec9ab654520138f830c4a579ac286',
                            # 'geetest_seccode':'38aec9ab654520138f830c4a579ac286|jordan'
                            },
                            callback = self.after_login
                            )]
        # yield scrapy.Request(url,cookies=self.cookies_19lou,headers=self.headers_19lou)

    def after_login(self, response):
        # sel = Selector(response)
        # url = urlparse.urlparse(response.url)
        # yield scrapy.Request('http://jiaxing.19lou.com/forum-778-thread-225621481236505467-1-1.html',headers=self.headers_19lou,callback=self.parse_19lou)
        yield scrapy.Request('http://jiaxing.19lou.com/forum-778-1.html?order=createdat',cookies=self.cookies_19lou,headers=self.headers_19lou)
        # yield scrapy.Request(base64.b64decode(url[4].split('&')[2].split('=')[1]),cookies=self.cookies_19lou,headers=self.headers_19lou, callback = self.post_login)

    def parse(self, response):
        url = urlparse.urlparse(response.url)
        sel = Selector(response)
        now = datetime.now()
        if url[1].find('0573') < 0:
            # yield scrapy.Request("https://jiaxing.19lou.com/login",cookies=self.cookies_19lou,headers=self.headers_19lou_login,callback = self.post_login)
            for site in sel.xpath('//tr'):
                catch_url = site.xpath('th[@class="title"]/div/a/@href').extract()
                print catch_url
                datenow = site.xpath('td/span[@class="color9"]/text()').extract()
                if len(datenow)>0:
                    if now.strftime('%Y-%m-%d') == str(datenow[0][0:10]).strip():
                        yield scrapy.Request(catch_url[0],headers=self.headers_19lou,callback=self.parse_contents)
        else:
            for site in sel.xpath('//tr'):
                catch_url = site.xpath('th/a[@class="s xst"]/@href').extract()
                datenow = site.xpath('td/em/span/text()').extract()
                if len(datenow)>0:
                    if now.strftime('%Y-%m-%d').replace('-0','-') == str(datenow[0][0:10]).strip():
                        yield scrapy.Request(catch_url[0],headers=self.headers_jxr,callback=self.parse_contents)


    # def parse_19lou(self, response):
        
    #     sel = Selector(response)
    #     for site in sel.xpath('//tr'):
    #             catch_url = site.xpath('th[@class="title"]/div/a/@href').extract()
    #             datenow = site.xpath('td/span[@class="color9"]/text()').extract()
    #             if len(datenow)>0:
    #                 if now.strftime('%Y-%m-%d') == str(datenow[0][0:10]).strip():
    #                     yield scrapy.Request(catch_url[0],headers=self.headers_19lou,callback=self.parse_contents)
    # def parse(self, response):
    #     title = sel.xpath('//title/text()').extract()
    #     con = sel.xpath('//td/div/div[@class="thread-cont"]').extract()
    #     author = sel.xpath('//div[@class="side"]/div/div/a/span/text()').extract()
    #     soup = BeautifulSoup(con[0], "lxml")
    #     srcList = []
    #     for link in soup.find_all('img'):
    #         srcList.append(link.get('src'))
    #     tid = url[2][18:36]
    #     i = 0
    #     for str_add in soup.find_all(re.compile("^img")):
    #         str_add.replace_with('<img src="'+srcList[i]+'"/>')
    #         i = i + 1
    #     item = DmozItem()
    #     if soup.get_text().find('zzd-wrap') < 0:
    #         item['title'] = str(title[0]).replace('-\xe6\x88\x91\xe4\xb9\x9f\xe6\x9d\xa5\xe4\xbe\x83\xe4\xbe\x83-\xe8\xae\xb2\xe7\xa9\xba\xe5\xa4\xb4-\xe5\x98\x89\xe5\x85\xb419\xe6\xa5\xbc','').strip()
    #         item['content'] = soup.get_text().replace(u'\xa0',u'').replace('http://att2.citysbs.com','http://cs.jx09.com.cn/attachment/collect/19lou').strip()
    #         item['tid'] = tid
    #         item['images'] = '|'.join(srcList)
    #         item['flag'] = '2'
    #         item['author'] = author[0].strip()
    #         print tid
            
    #         yield item
    	# sel = Selector(response)
    	# now = datetime.now()
     #    for site in sel.xpath('//tr'):
     #        catch_url = site.xpath('th/a[@class="s xst"]/@href').extract()
            
     #        datenow = site.xpath('td/em/span/text()').extract()
     #        if len(datenow)>0:
     #            #result = urlparse.urlparse(catch_url[0])
     #            #item = DmozItem()
     #            #item['tid']
     #            #print result[4][19:26]
     #            if(now.strftime('%Y-%m-%d') == datenow[0][0:10]):
     #                yield scrapy.Request(catch_url[0],headers=self.headers,callback=self.parse_contents)

    def parse_contents(self,response):
        if response.status == 200:
            sel = Selector(response)
            url = urlparse.urlparse(response.url)
            if url[1].find('0573') < 0:
                try:
                    title = sel.xpath('//title/text()').extract()
                    con = sel.xpath('//td/div/div[@class="thread-cont"]').extract()
                    author = sel.xpath('//div[@class="side"]/div/div/a/span/text()').extract()
                    soup = BeautifulSoup(con[0], "lxml")
                    srcList = []
                    for link in soup.find_all('img'):
                        srcList.append(link.get('src'))
                    tid = url[2][18:36]
                    i = 0
                    for str_add in soup.find_all(re.compile("^img")):
                        str_add.replace_with('<img src="'+srcList[i]+'"/>')
                        i = i + 1
                    attImg = sel.xpath('//ul[@class="view-unit-bd"]').extract()
                    if len(attImg):
                        attsoup = BeautifulSoup(attImg[0], "lxml")
                        attsrcList = []
                        for link in attsoup.find_all('img'):
                            if link.get('src').find('middle') > 0:
                                attsrcList.append(link.get('src'))
                        print attsrcList
                        print '00000000000000000000'
                    item = DmozItem()
                    if soup.get_text().find('zzd-wrap') < 0:
                        item['title'] = str(title[0]).replace('-\xe6\x88\x91\xe4\xb9\x9f\xe6\x9d\xa5\xe4\xbe\x83\xe4\xbe\x83-\xe8\xae\xb2\xe7\xa9\xba\xe5\xa4\xb4-\xe5\x98\x89\xe5\x85\xb419\xe6\xa5\xbc','').strip()
                        item['tid'] = tid
                        if len(attsrcList):
                            item['images'] = '|'.join(attsrcList)
                            item['content'] = soup.get_text().replace(u'\xa0',u'').replace('http://att2.citysbs.com','http://cs.jx09.com.cn/attachment/collect/19lou').strip() + '<br/><img src="' + item['images'].replace('|','"/><br/><br/><img src="').replace('http://att2.citysbs.com','http://cs.jx09.com.cn/attachment/collect/19lou') + '"/><br/>'
                        else:
                            item['images'] = '|'.join(srcList)
                            item['content'] = soup.get_text().replace(u'\xa0',u'').replace('http://att2.citysbs.com','http://cs.jx09.com.cn/attachment/collect/19lou').strip()
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
                        srcList.append(link.get('zoomfile').replace('http://attach.0573ren.com','http://cs.jx09.com.cn/attachment/collect/jxr'))
                    i = 0
                    for str_add in soup.find_all('ignore_js_op'):
                        str_add.replace_with('<br/><img src="'+srcList[i]+'"/><br/>')
                        i = i + 1
                    tid = url[4][19:26]
                    item = DmozItem()
                    item['title'] = str(title[0]).replace(' - \xe7\x99\xbe\xe5\xa7\x93\xe8\xaf\x9d\xe9\xa2\x98 - \xe5\x98\x89\xe8\xae\xba\xe7\xbd\x91|\xe5\x98\x89\xe5\x85\xb4\xe4\xba\xba\xe8\xae\xba\xe5\x9d\x9b','').strip()
                    item['content'] = soup.td.get_text().replace(u'\xa0',u'').replace('http://attach.0573ren.com','http://cs.jx09.com.cn/attachment/collect/jxr').strip()
                    item['tid'] = tid
                    item['images'] = '|'.join(srcList)
                    item['flag'] = '1'
                    item['author'] = author[0].strip()
                    yield item
                except Exception,e:
                    print e
    	#if response.status == 200:
            #selCon = Selector(response)
            #for site in selCon.xpath('//div[@class="thread-cont"]'):
                #content = site.xpath('text()').extract()[0]
                #print(content)
        #filename = response.url.split("/")[-2]
        #open(filename, 'wb').write(response.body)
