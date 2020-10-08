import json
import base64
import scrapy
from scrapy_splash import SplashRequest


class DownloadSpider(scrapy.Spider):
    name = 'download'

    def start_requests(self):
        url = 'https://stackoverflow.com/'
        splash_args = {
            'html': 1,
            'png': 1
        }
        yield SplashRequest(url, self.parse_result, endpoint='render.json', args=splash_args)

    def parse_result(self, response):
        print(response)
        # filename = 'some_image.png'
        # with open(filename, 'wb') as f:
        #     f.write(imgdata)
