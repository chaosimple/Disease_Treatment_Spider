#!/usr/bin/env python
#coding:utf-8
"""
  Author:   --<>
  Purpose: 
  Created: 2015/11/25
"""
from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http import Request
from sd_spider.items import JibingItem, ZhengzhuangItem


from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

########################################################################
class SDSpider(Spider):
	""""""
	name = 'JibingSpider'
	allowed_domains = ["pcbaby.com.cn"]
	start_urls = [
        "http://health.pcbaby.com.cn/jb/list.html"
    ]
	
	#----------------------------------------------------------------------
	def parse(self, response):
		""""""
		currentPage = response.xpath('//div[@class="page mb10"]/span/text()').extract()[0]
		print '---------------- Page: %s  ----------------' % str(currentPage)
		
		jbs = response.xpath('//i[@class="iDes"]')
		
		for jb in jbs:
			jburl = jb.xpath('em[@class="eName"]/span/a/@href').extract()[0] if jb.xpath('em[@class="eName"]/span/a/@href') else ''
			keshi = jb.xpath('em[@class="eSym"]/a/text()').extract() if jb.xpath('em[@class="eName"]/span/a/@href') else ''
			
			if jburl != '':
				request = Request(jburl, callback=self.parse_nav)
				request.meta['ks'] = keshi
				yield request
			
			#urlList = jb.xpath('a/@href').extract()
			#if len(urlList) > 0:
				#jb_url = urlList[0]
				#request = Request(jb_url, callback=self.parse_nav)
				#yield request               			
		
		# 循环爬取“下一页”
		nextpages = response.xpath('//div[@class="page mb10"]/a[@class="next"]/@href').extract()
		if len(nextpages) > 0:
			nextpage = nextpages[0]
			print '----- next page ------'
			print nextpage
			print '----- next page ------'
			
			req = Request(url=nextpage, callback=self.parse)
			yield req		
	
	#----------------------------------------------------------------------
	def parse_nav(self, response):
		""""""
		print '----- JiBing ------'
		print response.url
		print '-------------------'
		
		jb = JibingItem()
		jb['keshi'] = response.meta['ks']
		gss = response.xpath('//table[@class="gsText"]/tr/td')
		
		jb['name'] = gss[0].xpath('b/a/text()').extract()[0]
		
		temps = gss[0].xpath('b/a/text() | i/text()').extract()
		tt = ''
		for t in temps:
			tt += t
		jb['jibing'] = tt
		
		jb['gaishu'] = gss[1].xpath('div/i/text()').extract()[0].strip()
		jb['jiancha'] = gss[3].xpath('div/text()').extract()[0].strip() if gss[3].xpath('div/text()') else ''
		
		jb['zhengzhuang'] = gss[2].xpath('div/a/text()').extract()
		
		# 爬取其对应的症状页面
		zzurls = gss[2].xpath('div/a/@href').extract()		
		for zz in zzurls:
			req = Request(url=zz, callback=self.parse_zhengzhuang)
			yield req					
		
		yield jb
	
	#----------------------------------------------------------------------
	def parse_zhengzhuang(self, response):
		""""""
		print '----- ZhengZhuang ------'
		print response.url
		print '------------------------'
		
		zz = ZhengzhuangItem()
		gss = response.xpath('//table[@class="gsText"]/tr/td')
		
		zz['name'] = gss[0].xpath('b/a/text()').extract()[0]		
		temps = gss[0].xpath('b/a/text() | i/text()').extract()
		tt = ''
		for t in temps:
			tt += t
		zz['zhengzhuang'] = tt
		zz['gaishu'] = gss[1].xpath('text()').extract()[0].strip()
		zz['buwei'] = gss[2].xpath('a/text()').extract()[0] if gss[2].xpath('a/text()') else ''
		zz['renqun'] = gss[3].xpath('a/text()').extract() if gss[3].xpath('a/text()') else ''
		
		yield zz

if __name__ == '__main__':
	print 'over!'
	process = CrawlerProcess(get_project_settings())
	process.crawl('JibingSpider')
	process.start()	