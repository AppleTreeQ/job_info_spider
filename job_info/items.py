# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class JobInfoItem(Item):
    # define the fields for your item here like:
	title = Field()
	company = Field()
    	job_category = Field()
	location = Field()
	job_type = Field()
	career_level = Field()
	educational = Field()
	recruiting_num = Field()
	experience = Field()
	language = Field()
	salary = Field()
    	job_description = Field()
    	requirement = Field()
	time = Field()
	city = Field()
	company_category = Field()
	company_employees = Field()
	company_description = Field()
	url = Field()
	company_url = Field()

class EmployeeInfoItem(Item):
        user_name = Field()
        category = Field()
	industry = Field()
        gender = Field()
	experience = Field()
        city = Field()
	language = Field()
	age = Field()
	email = Field()  # todo
	phone = Field()  # todo
	job_type = Field() # full time or part time job
	location = Field() # address, leave it in sql
	nationality = Field()
	start_date = Field()
	desired_salary = Field()
	url = Field() ## end here
	experience_detail = Field()
        education = Field()
	skill = Field()
	certifications = Field()
        career_plan = Field()

