import scrapy
import pandas
from urllib.parse import urlparse


class ShopsSpider(scrapy.Spider):
    name = 'shops'
    df = pandas.read_csv("blocks.csv")
    start_urls = df["url"].array
    for_index = []
    for base_url in df["url"].array:
        base_url = urlparse(base_url)
        base_url = base_url.hostname
        for_index.append(base_url)

    allowed_domains = for_index

    def parse(self, response):
        for url in response.css("a::attr(href)"):
            href_url = url.get()
            if href_url is not None:
                if self.is_valid_url(href_url):
                    yield {
                        "source": response.request.url,
                        "href": response.urljoin(href_url)
                    }

    def is_valid_url(self, url):
        url_parts = urlparse(url)
        exclude = ["#", "/", ""]
        regex_exclude = ["google", "javascript", "mailto:", "tel:", "facebook", "pinterest", "youtube", "instagram",
                         "linkedin", "alibaba", "vk.com", "twitter", "search", "/news", "envato", "/blog", "/contact",
                         "shopify", "cart", "account", "login", "skype", "faq", "wp-content", "subscribe"]

        if url_parts.path.lower() in exclude:
            return False

        for word in regex_exclude:
            if word in url.lower():
                return False

        return True
