#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
代理管理器 - 负责获取和管理代理
"""

import os
import time
import random
import logging
import requests
from typing import Dict, Optional, List
from dotenv import load_dotenv

# 配置日志
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "proxy_manager")
except ImportError:
    # 配置基本日志，以防日志管理模块未安装
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

# 加载环境变量
load_dotenv()

class ProxyManager:
    """代理管理器，负责获取和管理代理"""
    
    def __init__(self):
        """初始化代理管理器"""
        # 代理API配置
        self.proxy_api_url = "https://share.proxy.qg.net/get"
        self.proxy_auth_key = "DTMIQ623"
        self.proxy_auth_pwd = "45D2CEB38959"
        
        # 代理缓存
        self.proxy_cache = None
        self.proxy_expiry = 0
        
        # 代理有效期（秒）
        self.proxy_lifetime = 300  # 5分钟
        
        # 代理测试URL
        self.test_urls = [
            "https://www.baidu.com",
            "https://www.qq.com",
            "https://www.163.com",
            "https://www.sina.com.cn"
        ]
        
        logger.info("代理管理器初始化成功")
    
    def _fetch_proxy_from_api(self) -> Dict:
        """从API获取代理"""
        # 最大重试次数
        max_retries = 3
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                # 构建请求参数
                params = {
                    "key": self.proxy_auth_key
                }
                
                # 发送请求
                logger.info(f"尝试从API获取代理 (尝试 {retry_count + 1}/{max_retries})...")
                response = requests.get(self.proxy_api_url, params=params, timeout=10)
                
                # 检查响应状态
                if response.status_code != 200:
                    logger.error(f"获取代理失败，状态码: {response.status_code}")
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = 2 ** retry_count  # 指数退避
                        logger.info(f"等待 {wait_time} 秒后重试...")
                        time.sleep(wait_time)
                    continue
                
                # 解析响应
                data = response.json()
                
                # 检查响应数据
                if data.get("code") != "SUCCESS":
                    logger.error(f"获取代理失败，错误信息: {data}")
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = 2 ** retry_count  # 指数退避
                        logger.info(f"等待 {wait_time} 秒后重试...")
                        time.sleep(wait_time)
                    continue
                
                # 获取代理信息
                proxy_list = data.get("data", [])
                if not proxy_list:
                    logger.error("获取代理失败，代理列表为空")
                    retry_count += 1
                    if retry_count < max_retries:
                        wait_time = 2 ** retry_count  # 指数退避
                        logger.info(f"等待 {wait_time} 秒后重试...")
                        time.sleep(wait_time)
                    continue
                
                # 返回第一个代理
                proxy_info = proxy_list[0]
                
                # 构建代理URL (使用server字段，它包含IP和端口)
                server = proxy_info.get("server")
                
                # 使用账号密码认证模式构建代理URL
                proxy_url = "http://%(user)s:%(password)s@%(server)s" % {
                    "user": self.proxy_auth_key,
                    "password": self.proxy_auth_pwd,
                    "server": server
                }
                
                # 返回代理信息
                logger.info(f"成功获取代理: {server}, 有效期至: {proxy_info.get('deadline')}")
                return {
                    "http": proxy_url,
                    "https": proxy_url
                }
                
            except Exception as e:
                logger.error(f"获取代理失败: {str(e)}")
                retry_count += 1
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count  # 指数退避
                    logger.info(f"等待 {wait_time} 秒后重试...")
                    time.sleep(wait_time)
        
        # 所有重试都失败，直接使用固定代理
        logger.warning("API获取代理失败，使用固定代理")
        
        # 使用固定代理
        fixed_server = "60.188.79.125:20007"
        proxy_url = "http://%(user)s:%(password)s@%(server)s" % {
            "user": self.proxy_auth_key,
            "password": self.proxy_auth_pwd,
            "server": fixed_server
        }
        
        logger.info(f"使用固定代理: {fixed_server}")
        return {
            "http": proxy_url,
            "https": proxy_url
        }
    
    def get_proxy(self) -> Dict:
        """获取代理"""
        # 检查缓存是否有效
        current_time = time.time()
        if self.proxy_cache and current_time < self.proxy_expiry:
            logger.info(f"使用缓存的代理，剩余有效期: {int(self.proxy_expiry - current_time)}秒")
            return self.proxy_cache
        
        # 尝试从API获取新代理
        logger.info("从API获取新代理")
        proxy = self._fetch_proxy_from_api()
        
        # 设置缓存
        self.proxy_cache = proxy
        self.proxy_expiry = current_time + self.proxy_lifetime
        
        logger.info(f"成功获取新代理，有效期: {self.proxy_lifetime}秒")
        return proxy
    
    def test_proxy(self, proxy: Optional[Dict] = None) -> bool:
        """测试代理是否可用"""
        if not proxy:
            proxy = self.get_proxy()
        
        if not proxy:
            logger.error("没有可用的代理进行测试")
            return False
        
        # 随机选择一个测试URL
        test_url = random.choice(self.test_urls)
        
        try:
            # 设置超时时间
            timeout = 10
            
            # 发送请求
            response = requests.get(test_url, proxies=proxy, timeout=timeout)
            
            # 检查响应状态
            if response.status_code == 200:
                logger.info(f"代理测试成功，URL: {test_url}")
                return True
            else:
                logger.warning(f"代理测试失败，状态码: {response.status_code}，URL: {test_url}")
                return False
                
        except Exception as e:
            logger.error(f"代理测试失败: {str(e)}，URL: {test_url}")
            return False
    
    def clear_cache(self):
        """清除代理缓存"""
        self.proxy_cache = None
        self.proxy_expiry = 0
        logger.info("代理缓存已清除")

# 测试代码
if __name__ == "__main__":
    # 创建代理管理器
    proxy_manager = ProxyManager()
    
    # 获取代理
    proxy = proxy_manager.get_proxy()
    print(f"获取到的代理: {proxy}")
    
    # 测试代理
    is_valid = proxy_manager.test_proxy(proxy)
    print(f"代理是否有效: {is_valid}") 