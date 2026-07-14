import random
from scrapy import signals
from ..config.settings import PROXY_POOL

class ProxyMiddleware:
    def __init__(self):
        self.proxies = PROXY_POOL
    
    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware
    
    def process_request(self, request, spider):
        if self.proxies:
            proxy = random.choice(self.proxies)
            request.meta['proxy'] = proxy
            spider.logger.debug(f'使用代理: {proxy}')
    
    def process_response(self, request, response, spider):
        # 检查响应是否正常
        if response.status in [403, 429, 503]:
            spider.logger.warning(f'代理被封禁: {request.meta.get("proxy")}')
            # 重新请求
            request.dont_filter = True
            return request
        return response
    
    def spider_opened(self, spider):
        spider.logger.info('代理中间件已启用') 