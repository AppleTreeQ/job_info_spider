# Scrapy settings for job_info project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'job_info'

SPIDER_MODULES = ['job_info.spiders']
NEWSPIDER_MODULE = 'job_info.spiders'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'job_info (+http://www.yourdomain.com)'

#pipeline setting
ITEM_PIPELINES = {
	'job_info.pipelines.JobInfoPipeline': 300,
}
