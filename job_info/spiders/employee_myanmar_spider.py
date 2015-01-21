import sys,re
from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from scrapy.http import Response, Request, FormRequest
from scrapy import signals, log
from job_info.items import EmployeeInfoItem 
import pdb

'''

'''
def first_item(t,default_value = None):
                return t[0].strip('\r\n ') if t else default_value

class WorkMyanmarSpider(BaseSpider):
	name = "employee_myanmar"
	allowed_domains = ["work.com.mm"]
	#parse_url_pattern1 = re.compile(r'http://www.work.com.mm/job/(page-[0-9]+)\?sort=dataCreated')
	parse_url_pattern1 = re.compile(r'http://www.work.com.mm/people/page-$')
	parse_url_pattern2 = re.compile(r'http://www.work.com.mm/people/([a-z]+)\/([a-z\-]+)([0-9]+)$')
	def start_requests(self):
		#pdb.set_trace()
		yield FormRequest(url='http://www.work.com.mm/j_spring_security_check', formdata = {'j_username': 'online_zq@163.com', 'j_password': '369612458'}, callback = self.check_login_response)
	def check_login_response(self, response):
		#pdb.set_trace()
		if "Logout" in response.body and "Search for people" in response.body:
			log.msg('Login successfully', level = log.INFO)
			yield Request('http://www.work.com.mm/people', callback = self.parse_url)
		else:
			log.msg('Login failed', level = log.ERROR)
			return

	def parse_url(self, response):
		#pdb.set_trace()
		log.msg('parse list url : %s ' % response.url, level = log.INFO)
		hxs = HtmlXPathSelector(response)
	        n_url = lambda url: ('http://www.work.com.mm' + url) if not url.startswith('http://') else url
		# search all the list pages
		for url in hxs.select('//a/@href').extract():
			#print url
			new_url = n_url(url)
			p = self.parse_url_pattern1.match(new_url)
			#p2 = self.parse_url_pattern2.match(new_url)
			if p:
				print new_url
				yield Request(new_url, callback = self.parse_url, priority = 5)
			else:
				continue
		# search all the employees, and his/her gender, experiance, city
		#pdb.set_trace()
		node = hxs.select('//div[@class="search_table mt20"]')
		for sub_node in node.xpath('.//tbody/tr'):
			url = first_item(sub_node.select('.//td[@class="tl"]/p/a/@href').extract())
			user_name = first_item(sub_node.xpath('.//td[@class="tl"]/p[1]/a/text()').extract())
			cate_info = first_item(sub_node.xpath('.//td[@class="tl"]/p[2]/text()').extract())
			if cate_info:
				category = cate_info.split(',', 1)[0].strip('\r\n ')
				industry = cate_info.split(',', 1)[1].strip('\r\n ')
			gender = first_item(sub_node.xpath('.//td[@class="tc"][1]/p/text()').extract())
			experience = first_item(sub_node.xpath('.//td[@class="tc"][2]/p/text()').extract())
			city = first_item(sub_node.xpath('.//td[@class="tc"][3]/p/text()').extract())
			meta_data = {
				"user_name" : user_name,
				"category" : category,
				"industry" : industry,
				"gender" : gender,
				"experience" : experience,
				"city" : city
			}
			new_url = n_url(url)
			p2 = self.parse_url_pattern2.match(new_url)
			if p2:
				yield Request(new_url, meta = meta_data, callback = self.parse_item, priority = 0)
	def parse_item(self, response):
		#pdb.set_trace()
		hxs = HtmlXPathSelector(response)
		meta = response.meta
		item = EmployeeInfoItem()
		item['user_name'] = meta['user_name']
		item['category'] = meta['category']
		item['industry'] = meta['industry']
		item['gender'] = meta['gender']
		item['experience'] = meta['experience']
		item['city'] = meta['city']
		item['url'] = response.url
		node = hxs.select('//div[@class="deatil_container mt20 mb40 clearfix"]')
		top_info = node.select('.//div[@class="resume_work_people"]')
		lang_ages = top_info.select('.//div[@class="mt48"]')
		lan = ''
		age = None
		for sub_info in lang_ages.xpath('.//p'):
			s = first_item(sub_info.select('.//text()').extract())
			if s.find("years old") == -1:
				lan += s
			else:
				age = s
		item['age'] = age
		item['language'] = lan
		item['email'] = None
		item['phone'] = None
		node = hxs.select('//div[@class="resume_work_content"]')
		basic_infos = node.select('.//div[@class="row_e"]')
		for basic_info in basic_infos:
			detail_name = first_item(basic_info.select('.//div[@class="label_cont tl "]/span/text()').extract())
			detail_value = first_item(basic_info.select('.//strong/text()').extract())
			self.write_item(item, detail_name, detail_value)
		print item
		return item

	def write_item(self, item, detail_name, detail_value):
                if detail_name == 'Job Type':
                        item['job_type'] = detail_value
		if detail_name == 'Location':
			item['location'] = None
		if detail_name == 'Nationality':
			item['nationality'] = detail_value
		if detail_name == 'Start Date':
			item['start_date'] = detail_value
		if detail_name == 'Desired Salary':
			item['desired_salary'] = detail_value

