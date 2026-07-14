#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
猎聘网爬虫 - 第二步
功能：验证step1生成的URL是否有数据，并标记状态

主要步骤：
1. 从MongoDB加载step1生成的URL组合
2. 使用Playwright对每个URL组合进行请求验证
3. 根据返回的职位数量判断URL是否有效
   - 职位数量 > 400：标记为success
   - 职位数量 <= 400：标记为failed
4. 将验证结果保存到MongoDB

数据存储：
- 输入集合：liepin_step1_urls_part1
- 输出集合：liepin_step1_urls_202504_log_part1
- 索引：
  * (industry_parent_code, industry_child_code, job_industry, job_category, job_type_name) - 复合索引
  * status - 状态索引
  * crawl_time - 爬取时间索引

请求配置：
- 基础URL：https://www.liepin.com
- 请求方法：GET
- 浏览器：Chromium
- 请求参数：包含职位类型、行业类型等搜索条件

注意事项：
1. 使用随机延迟(2-5秒)避免请求过快
2. 使用批量处理(1000条/批)提高效率
3. 记录详细的日志信息
4. 支持断点续传（通过检查已爬取记录）
"""

import json
import logging
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List
from pymongo import MongoClient
from tqdm import tqdm
from playwright.sync_api import sync_playwright, Page, Browser, BrowserContext
import random
import sys
import os
from urllib.parse import unquote

# 将项目根目录添加到Python路径中
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent.parent  # 从当前文件向上找三层到项目根目录
sys.path.append(str(project_root))

# 导入日志管理模块
try:
    from recruitment_spider.utils.log_manager import get_logger
    logger = get_logger(__name__, "liepin_spider_step2")
except ImportError:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    logger = logging.getLogger(__name__)

class LiepinSpiderStep2:
    """猎聘网爬虫 - Playwright版本"""
    
    def __init__(self):
        # 基础URL
        self.base_url = "https://www.liepin.com"
        
        # MongoDB配置
        self.mongo_uri = "mongodb://da_test:3g398GJIaaV43gEW@210.14.140.50:10387/da_test"
        self.mongo_db = "da_test"
        self.mongo_progress_collection = "liepin_step1_urls_202504_log_part1"  # 进度记录集合        
        self.liepin_url_part = "liepin_step1_urls_part1"  # URL集合名称
        self.mongo_client = None
        self.db = None
        self.progress_collection = None
        
        # URL缓存
        self.crawled_urls = {}
        
        # Playwright相关
        self.playwright = None
        self.browser = None
        self.context = None
        self.page = None
        
        # 初始化MongoDB连接
        self._init_mongodb()
        
        # 加载已爬取的URL
        self._load_crawled_urls()
        
        # 初始化Playwright
        self._init_playwright()
        
        logger.info("初始化完成")
    
    def _init_mongodb(self):
        """初始化MongoDB连接"""
        try:
            self.mongo_client = MongoClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            self.progress_collection = self.db[self.mongo_progress_collection]
            logger.info("MongoDB连接初始化成功")
        except Exception as e:
            logger.error(f"MongoDB连接初始化失败: {str(e)}")
            raise

    def _init_playwright(self):
        """初始化Playwright"""
        try:
            self.playwright = sync_playwright().start()
            
            # 浏览器启动参数
            browser_args = [
                '--disable-gpu',
                '--no-sandbox',
                '--disable-dev-shm-usage',
                '--disable-blink-features=AutomationControlled',
                '--disable-infobars',
                '--window-size=1024,768',
                '--start-maximized',
                '--disable-notifications',
                '--disable-popup-blocking',
                '--disable-extensions',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process',
                '--disable-site-isolation-trials'
            ]
            
            # 启动浏览器
            self.browser = self.playwright.chromium.launch(
                headless=False,  # 有头模式，方便调试
                args=browser_args
            )
            
            # 创建上下文，增加常见请求头
            self.context = self.browser.new_context(
                viewport={'width': 1024, 'height': 768},
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36',
                locale='zh-CN',
                timezone_id='Asia/Shanghai',
                geolocation={'latitude': 39.9042, 'longitude': 116.4074},  # 北京坐标
                permissions=['geolocation'],
                color_scheme='light',
                device_scale_factor=1,
                is_mobile=False,
                has_touch=False,
                java_script_enabled=True,
                ignore_https_errors=True,
                extra_http_headers={
                    "accept": "application/json, text/plain, */*",
                    "accept-language": "zh-CN,zh;q=0.9",
                    "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
                    "sec-ch-ua-mobile": "?0",
                    "sec-ch-ua-platform": '"Windows"',
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "same-site",
                    "x-client-type": "web",
                    "x-requested-with": "XMLHttpRequest"
                }
            )
            
            # 创建新页面
            self.page = self.context.new_page()
            
            # 注入反检测脚本
            self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {get: () => undefined});
                Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]});
                Object.defineProperty(navigator, 'languages', {get: () => ['zh-CN', 'zh']});
                window.chrome = { runtime: {} };
                Object.defineProperty(navigator, 'platform', {get: () => 'Win32'});
                Object.defineProperty(navigator, 'userAgent', {get: () => 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36'});
            """)
            
            # 设置页面超时
            self.page.set_default_timeout(30000)
            self.page.set_default_navigation_timeout(30000)
            
            logger.info("Playwright初始化成功")
        except Exception as e:
            logger.error(f"Playwright初始化失败: {str(e)}")
            raise

    def _random_sleep(self, min_seconds=2, max_seconds=5):
        """随机等待一段时间"""
        time.sleep(random.uniform(min_seconds, max_seconds))

    def _simulate_human_behavior(self):
        """模拟人类行为"""
        try:
            # 随机滚动
            for _ in range(random.randint(2, 4)):
                self.page.mouse.wheel(0, random.randint(100, 500))
                self._random_sleep(0.2, 0.5)
            
            # 随机移动鼠标
            for _ in range(random.randint(2, 4)):
                x = random.randint(100, 800)
                y = random.randint(100, 600)
                self.page.mouse.move(x, y)
                self._random_sleep(0.2, 0.5)
                
        except Exception as e:
            logger.warning(f"模拟人类行为时出错: {str(e)}")

    def _load_crawled_urls(self):
        """加载已爬取的URL记录"""
        try:
            # 创建索引
            self.progress_collection.create_index([
                ('industry_parent_code', 1),
                ('industry_child_code', 1),
                ('job_industry', 1),
                ('job_category', 1),
                ('job_type_name', 1)
            ], unique=True)
            self.progress_collection.create_index([('status', 1)])
            self.progress_collection.create_index([('crawl_time', 1)])
            
            # 加载已爬取的URL
            cursor = self.progress_collection.find({}, {'_id': 0})
            for doc in cursor:
                key = (
                    doc['industry_parent_code'],
                    doc['industry_child_code'],
                    doc['job_industry'],
                    doc['job_category'],
                    doc['job_type_name']
                )
                self.crawled_urls[key] = 1
            
            logger.info(f"已加载 {len(self.crawled_urls)} 条爬取记录")
        except Exception as e:
            logger.error(f"加载已爬取URL失败: {str(e)}")
            raise

    def is_combination_crawled(self, url: dict) -> bool:
        """检查URL组合是否已爬取"""
        key = (
            url['industry_parent_code'],
            url['industry_child_code'],
            url['job_industry'],
            url['job_category'],
            url['job_type_name']
        )
        return key in self.crawled_urls

    def get_job_count(self, url: str) -> int:
        """
        获取职位数量
        :param url: 职位列表URL
        :return: 职位数量，如果被ban返回-1
        """
        try:
            # 简单处理URL，只替换#为%23
            encoded_url = url.replace('#', '%23')
            
            logger.info(f"原始URL: {url}")
            logger.info(f"处理后URL: {encoded_url}")
            
            # 创建响应监听器
            response_data = None
            def handle_response(response):
                nonlocal response_data
                if ("api-c.liepin.com/api/com.liepin.searchfront4c.pc-search-job" in response.url 
                    and response.status == 200):
                    try:
                        response_data = response.json()
                    except json.JSONDecodeError as e:
                        logger.error(f"解析API响应JSON失败: {str(e)}, URL: {response.url}")
                    except Exception as e:
                        logger.error(f"处理API响应时发生未知错误: {str(e)}, URL: {response.url}")

            # 添加响应监听器
            self.page.on("response", handle_response)
            
            try:
                # 设置必要的cookie
                cookies = [
                    {
                        "name": "XSRF-TOKEN",
                        "value": "ArB1SMFrRZO18mxbOOdPOQ",
                        "domain": ".liepin.com",
                        "path": "/"
                    },
                    {
                        "name": "__gc_id",
                        "value": "3dad4c755de14778bdf9438f7a067a0e",
                        "domain": ".liepin.com",
                        "path": "/"
                    },
                    {
                        "name": "__uuid",
                        "value": "1748395987113.72",
                        "domain": ".liepin.com",
                        "path": "/"
                    }
                ]
                self.context.add_cookies(cookies)
                
                # 访问目标页面
                max_retries = 3
                retry_count = 0
                while retry_count < max_retries:
                    try:
                        # 先尝试等待页面加载
                        response = self.page.goto(encoded_url, wait_until='domcontentloaded', timeout=60000)  # 增加超时时间到60秒
                        
                        # 检查响应状态
                        if response and response.status == 200:
                            # 等待页面加载完成，但使用更短的超时时间
                            try:
                                # 先等待页面基本元素加载
                                self.page.wait_for_selector('body', timeout=30000)
                                # 再等待网络请求完成
                                self.page.wait_for_load_state('networkidle', timeout=30000)
                            except TimeoutError as te:
                                # 如果networkidle超时，但页面基本内容已加载，继续执行
                                logger.warning(f"等待页面加载超时，但继续执行: {str(te)}, URL: {encoded_url}")
                            break
                        else:
                            logger.warning(f"页面响应状态码异常: {response.status if response else 'None'}, URL: {encoded_url}")
                            retry_count += 1
                            if retry_count == max_retries:
                                logger.error(f"页面加载失败(已重试{max_retries}次): {encoded_url}")
                                return -1
                            time.sleep(10)  # 增加重试间隔到10秒
                            
                    except TimeoutError as te:
                        retry_count += 1
                        if retry_count == max_retries:
                            logger.error(f"页面加载超时(已重试{max_retries}次): {str(te)}, URL: {encoded_url}")
                            return -1
                        logger.warning(f"页面加载超时,正在进行第{retry_count}次重试: {str(te)}, URL: {encoded_url}")
                        time.sleep(10)  # 增加重试间隔到10秒
                    except Exception as e:
                        logger.error(f"页面加载出错: {str(e)}, URL: {encoded_url}")
                        retry_count += 1
                        if retry_count == max_retries:
                            return -1
                        time.sleep(10)
                        continue
                
                # 检查URL是否被重定向
                final_url = self.page.url
                # 将两个URL都解码后再比较，避免中文编码导致的误判
                decoded_encoded_url = unquote(encoded_url)
                decoded_final_url = unquote(final_url)
                
                if decoded_encoded_url != decoded_final_url:
                    logger.error(f"URL被重定向，可能被ban。原始URL: {decoded_encoded_url}, 重定向到: {decoded_final_url}")
                    return -1
                
                # 模拟人类行为
                self._simulate_human_behavior()
                
                # 等待API响应
                time.sleep(2)  # 给API请求一些时间
                
                # 检查响应数据
                if response_data and 'data' in response_data:
                    total_count = response_data['data'].get('pagination', {}).get('totalCounts', 0)
                    logger.info(f"获取到职位数量: {total_count}")
                    return total_count
                
                # 检查是否被限制访问
                if response_data and 'code' in response_data and response_data['code'] != 0:
                    logger.error(f"API返回错误码: {response_data['code']}, 可能被ban")
                    return -1
                
                logger.warning(f"未获取到职位数量数据，URL: {encoded_url}")
                return 0
            finally:
                # 移除响应监听器
                self.page.remove_listener("response", handle_response)
                
        except Exception as e:
            logger.error(f"获取职位数量失败: {str(e)}, URL: {url}")
            return -1

    def mark_url_crawled(self, url: dict, status: str, job_count: int):
        """
        标记URL为已爬取
        :param url: URL信息
        :param status: 爬取状态
        """
        try:
            # 更新缓存
            key = (
                url['industry_parent_code'],
                url['industry_child_code'],
                url['job_industry'],
                url['job_category'],
                url['job_type_name']
            )
            self.crawled_urls[key] = 1
            
            # 更新数据库
            self.progress_collection.update_one(
                {
                    'industry_parent_code': url['industry_parent_code'],
                    'industry_child_code': url['industry_child_code'],
                    'job_industry': url['job_industry'],
                    'job_category': url['job_category'],
                    'job_type_name': url['job_type_name']
                },
                {
                    '$set': {
                        'url': url['url'],
                        'industry_parent_name': url['industry_parent_name'],
                        'industry_child_name': url['industry_child_name'],
                        'status': status,
                        'job_count': job_count,
                        'crawl_time': datetime.now()
                    }
                },
                upsert=True
            )
        except Exception as e:
            logger.error(f"标记URL爬取状态失败: {str(e)}")

    def close(self):
        """关闭所有连接"""
        try:
            # 关闭Playwright
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            if self.playwright:
                self.playwright.stop()
            logger.info("Playwright连接已关闭")
            
            # 关闭MongoDB
            if self.mongo_client:
                self.mongo_client.close()
                logger.info("MongoDB连接已关闭")
        except Exception as e:
            logger.error(f"关闭连接失败: {str(e)}")

    def run(self):
        """运行爬虫"""
        try:
            # 获取所有待处理的URL
            cursor = self.db[self.liepin_url_part].find({},{"_id":0,"status":0,'create_time':0})
            urls = list(cursor)
            
            if not urls:
                logger.warning("没有找到待处理的URL")
                return
            
            logger.info(f"开始处理 {len(urls)} 个URL")
            
            # 使用tqdm显示进度
            for url in tqdm(urls, desc="处理URL"):
                # 检查是否已爬取
                if self.is_combination_crawled(url):
                    logger.info(f"URL {url['url']} 已爬取，跳过")
                    continue
                
                # 获取职位数量
                job_count = self.get_job_count(url['url'])
                
                # 如果返回-1，说明可能被ban，停止爬取
                if job_count == -1:
                    logger.error("检测到可能被ban，停止爬取")
                    break
                
                # 根据职位数量判断状态
                status = 'success' if job_count > 400 else 'failed'
                
                # 标记URL状态
                self.mark_url_crawled(url, status, job_count)
                
                # 随机延迟2-3秒
                self._random_sleep(2, 3)
            
            logger.info("URL处理完成")
            
        except Exception as e:
            logger.error(f"爬虫运行出错: {str(e)}")
            raise
        finally:
            self.close()

def main():
    """主函数"""
    try:
        # 创建爬虫实例
        spider = LiepinSpiderStep2()
        # 运行爬虫
        spider.run()
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())

if __name__ == "__main__":
    main()
