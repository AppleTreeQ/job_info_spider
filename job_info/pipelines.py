# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from job_info.items import JobInfoItem, EmployeeInfoItem
import sqlite3
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals
from os import path
import pdb

class JobInfoPipeline(object):
	filename = '/home/qzhai/spider_study/job_info_spider/job_info/sqlitedb/jobinfo.db'
	sqlfile = '/home/qzhai/spider_study/job_info_spider/job_info/jobdb.sql'
	def __init__(self):
		self.conn = None
		dispatcher.connect(self.initialize, signals.engine_started)
	        dispatcher.connect(self.finalize, signals.engine_stopped)

    	def process_item(self, item, spider):
		if not item: return None
		if isinstance(item, JobInfoItem):
			self.__store_job_company_item(item, spider)
        	return item

	def __store_job_company_item(self, item, spider):
		if not item: return None
		if isinstance(item, JobInfoItem):
			jobinfosql = """INSERT INTO JobInfo(Title, Company, Category, Location, JobType, CareerLevel, Educational, RecruitNum, Experience, Language, Description, Requirement, Time, City, Salary, URL, CompanyURL) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");""" % (item['title'], item['company'], item['job_category'], item['location'], item['job_type'], item['career_level'], item['educational'], item['recruiting_num'], item['experience'], item['language'], item['job_description'], item['requirement'], item['time'], item['city'], item['salary'], item['url'], item['company_url'])
			companysql = """INSERT INTO Company(Name, Category, Employee, Description) VALUES ("%s", "%s", "%s", "%s");""" % (item['company'], item['company_category'], item['company_employees'], item['company_description'])
			try:
				self.conn.execute(jobinfosql)
			except:
				print 'Failed to insert item: ' + jobinfosql
			try:
				self.conn.execute(companysql)
			except:
				print 'Failed to insert item: ' + companysql
		pdb.set_trace()
		if isinstance(item, EmployeeInfoItem):
			employeesql = """INSERT INTO Employee(Name, Category, Industry, Gender, Experience, City, Language, Age, Email, Phone, JobType, Nationality, StartDate, DesiredSalary, URL) VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s");""" % ( item['user_name'], item['category'], item['industry'], item['gender'], item['experience'], item['city'], item['language'], item['age'], item['email'], item['phone'], item['job_type'], item['nationality'], item['start_date'], item['desired_salary'], item['url'])
			try:
				self.conn.execute(employeesql)
			except:
				print 'Failed to insert item: ' + employeesql
		return item

	def initialize(self):
#		pdb.set_trace()
		if path.exists(self.filename):
			self.conn = sqlite3.connect(self.filename)
		else:
			self.conn = self.createdb(self.filename)

	def finalize(self):
		if self.conn is not None:
			self.conn.commit()
			self.conn.close()
			self.conn = None

	def createdb(self, filename):
		conn = sqlite3.connect(filename)
		sql = open(self.sqlfile, 'r')
		for line in sql.readline():
			conn.execute(line)
		conn.commit()
		return conn

