import scrapy
import csv
from scrapy.crawler import CrawlerProcess
from scrapy.utils.reactor import install_reactor
from twisted.internet import reactor



class JobSpider(scrapy.Spider):
    name = "jobspider"
    print(name)

    def start_requests(self):
        # Read the company names from a CSV file
        print("hello")
        with open('companies.csv', 'r') as f:
            reader = csv.reader(f)
            companies = [
                row[0] for row in reader]
        print(companies)

        # Visit each company's career page
        for company in companies:
            url = f'https://www.{company}.com/careers'
            yield scrapy.Request(url=url, callback=self.parse, meta={'company': company})
            print(url)

    def parse(self, response):
      company_name = response.meta['company']
      careers_url = response.url
      yield {
          'company_name': company_name,
          'careers_url': careers_url
      }

process = CrawlerProcess({
    'FEED_URI': 'output.csv',
    'FEED_FORMAT': 'csv',
    'LOG_ENABLED': False
})

process.crawl(JobSpider)
process.start()
