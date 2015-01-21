import sys,re
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Response, Request
from scrapy import signals, log
from job_info.items import JobInfoItem 
import pdb

'''

'''
def first_item(t,default_value = None):
                return t[0].strip('\r\n ') if t else default_value

class WorkMyanmarSpider(BaseSpider):
	name = "work_myanmar"
	allowed_domains = ["work.com.mm"]
	#parse_url_pattern1 = re.compile(r'http://www.work.com.mm/job/(page-[0-9]+)\?sort=dateCreated')
	parse_url_pattern1 = re.compile(r'http://www.work.com.mm/job/page-\?sort=dateCreated')
	parse_url_pattern2 = re.compile(r'http://www.work.com.mm/job/(.+)type=search$')
	def start_requests(self):
		yield Request('http://www.work.com.mm/job?id=basicSearch', callback = self.parse_url)
	def parse_url(self, response):
		log.msg('parse list url : %s ' % response.url, level = log.INFO)
		hxs = HtmlXPathSelector(response)
	        n_url = lambda url: ('http://www.work.com.mm' + url) if not url.startswith('http://') else url
		for url in hxs.select('//a/@href').extract():
			#print url
			new_url = n_url(url)
			p = self.parse_url_pattern1.match(new_url)
			if p:
				yield Request(new_url, callback = self.parse_url, priority = 5)
			else:
				continue
		node = hxs.select('//div[@class="search_table"]')
		#pdb.set_trace()
		for sub_node in node.xpath('.//tbody/tr'):
                        url = first_item(sub_node.select('.//td[@class="tl"]/p/a/@href').extract())
                        city = ''.join(sub_node.xpath('.//td[3]/text()').extract()).strip('\r\n ')
                        time = first_item(sub_node.xpath('.//td[4]/p/text()').extract())
                        meta_data = {
                                "city" : city,
                                "time" : time
                        }
                        new_url = n_url(url)
			p2 = self.parse_url_pattern2.match(new_url)
			if p2:
				
				yield Request(new_url, meta = meta_data, callback = self.parse_item, priority = 0)

	def parse_item(self, response):
		hxs = HtmlXPathSelector(response)
		meta = response.meta
		item = JobInfoItem()
		item['city'] = meta['city']
		item['time'] = meta['time']
		item['company'] = first_item(hxs.select('//div[@class="fl"]/h1/span[@class="color_blue f16 pdt5"]/text()').extract())
#		node = hxs.select('//div[contain(@class,"jobDetails"]/text()').extract()
                item['title'] = first_item(hxs.select('//div[@class="fl"]/h1/span[@class="color_blue f16 fb"]/text()').extract())
#		sub_node = hxs.select('//div[@class="fl rightHl"]')
#		item['job_category'] = first_item(sub_node.select('.//div[@class="jobDetails"][1]/ul/li[1]/div[2]/text()').extract())
#		item['location'] = first_item(sub_node.select('.//div[@class="jobDetails"][1]/ul/li[2]/div[2]/text()').extract())
#		item['job_type'] = first_item(sub_node.select('.//div[@class="jobDetails"][1]/ul/li[3]/div[2]/text()').extract())
#		item['career_level'] = first_item(sub_node.select('.//div[@class="jobDetails"][2]/ul/li[1]/div[2]/text()').extract())
#		item['educational'] = first_item(sub_node.select('.//div[@class="jobDetails"][2]/ul/li[2]/div[2]/text()').extract())
#		item['recruiting_num'] = first_item(sub_node.select('.//div[@class="jobDetails"][2]/ul/li[3]/div[2]/text()').extract())
#		item['experience'] = first_item(sub_node.select('.//div[@class="jobDetails"][2]/ul/li[4]/div[2]/text()').extract())
#		item['language'] = first_item(sub_node.select('.//div[@class="jobDetails"][2]/ul/li[5]/div[2]/text()').extract())
                item['job_description'] = ''.join(hxs.select('//div[@class="info_detail mt20"][1]/p/text()').extract())
                item['requirement'] = ''.join(hxs.select('//div[@class="info_detail mt20"][2]/p/text()').extract())
		job_details = hxs.select('//div[@class="fl rightHl"]')
		for job_detail in job_details.xpath('.//div[@class="jobDetails"]'):
			for job_detail_li in job_detail.xpath('.//li'):
				detail_name = first_item(job_detail_li.select('.//div[1]/text()').extract())
				detail_value = first_item(job_detail_li.select('.//div[2]/text()').extract())
				if detail_name:
					self.write_item(item, detail_name, detail_value)
				else:
					continue
		item['salary'] = None
		sub_node = hxs.select('//div[@class="informationC"]')
		item['company_category'] = first_item(sub_node.select('.//table/tr[1]/td[2]/text()').extract())
		item['company_employees'] = first_item(sub_node.select('.//table/tr[3]/td[2]/text()').extract())
		item['company_description'] = ''.join( sub_node.select('.//div[@class="ml20 pd_span mt10"]/div/text()').extract())
		item['company_url'] = first_item(sub_node.select('.//table/tr[2]/td/a/@href').extract())
		item['url'] = response.url
		if not item.get('language'):
                        item['language'] = None
                if not item.get('recruiting_num'):
                        item['recruiting_num'] = None
		print item
		return item

	def write_item(self, item, detail_name, detail_value):
		if detail_name == 'Job Category:':
			item['job_category'] = detail_value
		if detail_name == 'Location:':
			item['location'] = detail_value
		if detail_name == 'Job Type:':
			item['job_type'] = detail_value
		if detail_name == 'Career Level:':
			item['career_level'] = detail_value
		if detail_name == 'Educational:':
			item['educational'] = detail_value
		if detail_name == 'Recruiting Number:':
			item['recruiting_num'] = detail_value
		if detail_name == 'Work Experience:':
			item['experience'] = detail_value
		if detail_name == 'Language:':
			item['language'] = detail_value
		if detail_name == 'Salary':
			item['salary'] = detail_value
