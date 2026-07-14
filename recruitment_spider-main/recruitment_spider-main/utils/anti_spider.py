import time
from scrapy.exceptions import IgnoreRequest
import random

class AntiSpider:
    def __init__(self):
        self.ban_patterns = [
            '访问太频繁',
            '请输入验证码',
            '系统检测到异常访问'
        ]
    
    def is_banned(self, response):
        """检查是否被反爬"""
        # 检查状态码
        if response.status in [403, 401, 407]:
            return True
            
        # 检查页面内容是否包含反爬提示
        for pattern in self.ban_patterns:
            if pattern in response.text:
                return True
                
        return False
    
    @staticmethod
    def handle_ban(response):
        """处理反爬措施"""
        # 随机延迟
        time.sleep(60)
        
        # 可以在这里添加:
        # 1. 更换代理IP
        # 2. 更换User-Agent
        # 3. 处理验证码
        # 4. 降低爬取频率
        
        raise IgnoreRequest("检测到反爬，请求已忽略")
        
    def get_random_delay(self):
        """获取随机延迟时间"""
        return random.uniform(1, 5) 