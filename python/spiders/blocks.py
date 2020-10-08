import scrapy
import pandas
from urllib.parse import urlparse


class BlocksSpider(scrapy.Spider):
    name = 'blocks'
    start_urls = pandas.read_json("test.json")
    start_urls = start_urls["href"].array

    for_index = []
    df = pandas.read_csv("blocks.csv")
    for base_url in df["url"].array:
        base_url = urlparse(base_url)
        base_url = base_url.hostname
        for_index.append(base_url)

    allowed_domains = for_index
    done_list = []

    def parse(self, response):
        base = urlparse(response.request.url)
        try:
            index = self.for_index.index(base.hostname)
        except ValueError:
            print(base.hostname + " cannot be found")
            return False
        done = False
        try:
            done = self.done_list.index(response.request.url)
        except ValueError:
            if not done:
                print("site can be processed")

        if done:
            return False

        blocks = {
            "path": response.request.url,
            "href": self.df["url-block"][index],
            "image": self.df["image"][index],
            "title": self.df["title"][index],
            "wrapper": None
        }

        blocks["wrapper"] = self.get_wrapper(response, blocks)

        if blocks["wrapper"]:
            yield blocks

    def get_path(self, response, block):
        full_path = []
        excluded = ["unknown", None, "other"]
        for node in response.xpath("//*[@class='" + block.replace(".", " ").strip() + "']/ancestor::*"):
            class_name = node.xpath("@class").get()
            excluded = ["unknown", None, "other"]
            for item in excluded:
                if item in full_path:
                    break
            if class_name not in full_path:
                if class_name:
                    class_name = "." + class_name.strip().replace(" ", ".")
                full_path.append(class_name)

        del full_path[0:2]
        return full_path

    def get_wrapper(self, response, blocks):
        url_path = self.get_path(response, blocks["href"])
        title_path = self.get_path(response, blocks["title"])
        path = set(url_path).intersection(title_path)
        return " ".join(path)
