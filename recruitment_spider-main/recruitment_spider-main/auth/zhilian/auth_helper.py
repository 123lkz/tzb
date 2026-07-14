import json
import time
import random
import base64
import hashlib
import re
from typing import Tuple
from recruitment_spider.auth.base import BaseAuthHelper

class ZhilianAuthHelper(BaseAuthHelper):
    def __init__(self):
        super().__init__()
        self.domains = [".zhaopin.com", ".zhaopin.cn"]
    
    def get_auth_info(self) -> Tuple[str, dict]:
        """
        生成认证信息
        返回: (cookies_str, url_params)
        """
        try:
            # 生成基础参数
            client_id = self._generate_client_id()
            timestamp = int(time.time() * 1000)
            
            # 生成 cookies
            cookies = {
                "x-zp-client-id": client_id,
                "at": self._generate_token(timestamp),
                "rt": self._generate_token(timestamp + 1000),
                "sensorsdata2015jssdkcross": self._generate_sensors_data(client_id)
            }
            
            # 生成请求参数
            params = {
                "MmEwMD": self._generate_param1(timestamp, client_id),
                "c1K5tw0w6_": self._generate_param2(timestamp, client_id)
            }
            
            cookies_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
            return cookies_str, params
            
        except Exception as e:
            self.logger.error(f"生成认证信息失败: {e}")
            return None, None
    
    def refresh_auth(self):
        """刷新认证信息"""
        return self.get_auth_info()
    
    def is_valid(self, response_data: dict) -> bool:
        """检查认证是否有效"""
        return not ('unauthorized' in str(response_data).lower())
    
    def _generate_client_id(self) -> str:
        """生成客户端ID"""
        timestamp = time.time() * 1000
        
        def replace_char(match):
            t = int(timestamp + 16 * random.random()) % 16
            if match.group(0) == 'x':
                return hex(t)[2:]
            else:  # y
                return hex((t & 0x3) | 0x8)[2:]
        
        return re.sub(r'[xy]', replace_char, "xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx")
    
    def _generate_token(self, timestamp: int) -> str:
        """生成认证令牌"""
        data = f"zp_token_{timestamp}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def _generate_param1(self, timestamp: int, client_id: str) -> str:
        """生成第一个参数"""
        seed = f"zp_{timestamp}_{client_id}"
        return base64.b64encode(seed.encode()).decode()
    
    def _generate_param2(self, timestamp: int, client_id: str) -> str:
        """生成第二个参数"""
        seed = f"zp_{timestamp}_2_{client_id}"
        return hashlib.md5(seed.encode()).hexdigest()
    
    def _generate_sensors_data(self, client_id: str) -> str:
        """生成 sensors data"""
        data = {
            "distinct_id": client_id,
            "first_id": "",
            "props": {
                "$latest_traffic_source_type": "直接流量",
                "$latest_search_keyword": "未取到值_直接打开",
                "$latest_referrer": ""
            }
        }
        return base64.b64encode(json.dumps(data).encode()).decode()
    
    def _generate_request_params(self) -> dict:
        """生成请求参数"""
        client_id = self._generate_client_id()
        page_request_id = f"aebde5b9f4c64a1e836d54a99d18aeec-{int(time.time() * 1000)}-{random.randint(100000, 999999)}"
        
        return {
            "x-zp-client-id": client_id,
            "x-zp-page-request-id": page_request_id
        } 