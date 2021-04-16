import json

import scrapy

from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

from ..items import NedbankzaItem
from itemloaders.processors import TakeFirst


class NedbankzaSpider(scrapy.Spider):
	name = 'nedbankza'
	start_urls = ['https://www.nedbank.co.za/content/nedbank.remotenavigationcache.json']

	def parse(self, response):
		data = json.loads(response.text)
		for post in data['nodes'][6]['nodes'][1:]:
			try:
				for foo in post['nodes']:
					for nii in foo['nodes']:
						try:
							for url in nii['nodes']:
								url = 'https://www.nedbank.co.za' + url['path'] + '.filteredcontent.json'
								yield response.follow(url, self.parse_post)
						except:
							pass
			except:
				pass

	def parse_post(self, response):
		data = json.loads(response.text)

		title = data['jcr:title']
		try:
			description = data['detailnews']['parinfo']['responsivetitletext']['text']
		except:
			description = data['detailnews']['precontentpar']['responsivetitletext']['text']
		description = remove_tags(description)
		try:
			date = data['publishdate']
		except:
			date = None

		item = ItemLoader(item=NedbankzaItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
