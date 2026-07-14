#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
前程无忧 Step5 爬虫 - 简化版本
用于爬取前程无忧职位详情数据
"""

import asyncio
import json
import time
import random
from datetime import datetime
from typing import Dict, List, Optional
import logging
import traceback

from playwright.async_api import async_playwright, Browser, Page, BrowserContext
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f'qcwy_spider_step5_simple_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class QCWYSpiderStep5Simple:
    def __init__(self):
        # MongoDB配置
        try:
            self.mongo_client = MongoClient("mongodb://da_test:3g398GJIaaV43gEW@210.14.140.50:10387/da_test")
            self.db = self.mongo_client["da_test"]
            self.source_collection = self.db["qcwy_step2_urls_part1"]  # 源数据集合
            self.target_collection = self.db["qcwy_step2_job_raw_part1"]  # 目标集合（职位数据）
            self.log_collection = self.db["qcwy_step2_urls_202505_log_part1"]  # 日志集合
            logger.info("MongoDB连接成功")
        except Exception as e:
            logger.error(f"MongoDB连接失败: {str(e)}")
            raise
        
        # Playwright配置
        self.playwright = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        
        # 爬取配置
        self.delay_range = (2, 4)  # 随机延迟范围（秒）
        self.timeout = 30000  # 页面加载超时时间（毫秒）
        
        # 反爬虫配置
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0',
        ]
        
        # 统计信息
        self.stats = {
            'total_processed': 0,
            'success_count': 0,
            'error_count': 0,
            'duplicate_count': 0,
            'blocked_count': 0
        }

    def get_random_user_agent(self) -> str:
        """获取随机User-Agent"""
        return random.choice(self.user_agents)

    async def init_browser(self):
        """初始化浏览器"""
        try:
            logger.info("开始初始化浏览器...")
            
            # 启动Playwright
            self.playwright = await async_playwright().start()
            logger.info("Playwright启动成功")
            
            # 启动浏览器
            self.browser = await self.playwright.chromium.launch(
                headless=False,  # 有头模式，方便调试
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-gpu',
                    '--disable-web-security',
                    '--disable-extensions',
                    '--disable-plugins',
                    '--disable-background-timer-throttling',
                    '--disable-backgrounding-occluded-windows',
                    '--disable-renderer-backgrounding',
                ]
            )
            logger.info("浏览器启动成功")
            
            # 创建上下文
            user_agent = self.get_random_user_agent()
            self.context = await self.browser.new_context(
                viewport={'width': 1024, 'height': 768},
                user_agent=user_agent,
                locale='zh-CN',
                timezone_id='Asia/Shanghai',
            )
            logger.info("浏览器上下文创建成功")
            
            # 创建页面
            self.page = await self.context.new_page()
            await self.page.set_default_timeout(self.timeout)
            logger.info("页面创建成功")
            
            # 设置额外的页面属性（简化版本）
            self.page.add_init_script("""
                Object.defineProperty(navigator, 'webdriver', {
                    get: () => undefined,
                });
            """)
            logger.info("页面脚本设置成功")
            
            logger.info(f"浏览器初始化成功 - User-Agent: {user_agent}")
            
        except Exception as e:
            logger.error(f"浏览器初始化失败: {str(e)}\n{traceback.format_exc()}")
            await self.close_browser()
            raise

    async def close_browser(self):
        """关闭浏览器"""
        try:
            if self.page:
                await self.page.close()
                self.page = None
            if self.context:
                await self.context.close()
                self.context = None
            if self.browser:
                await self.browser.close()
                self.browser = None
            if self.playwright:
                await self.playwright.stop()
                self.playwright = None
            logger.info("浏览器已关闭")
        except Exception as e:
            logger.error(f"关闭浏览器失败: {str(e)}")
        finally:
            self.page = None
            self.context = None
            self.browser = None
            self.playwright = None

    async def get_source_urls(self) -> List[Dict]:
        """获取源URL数据，过滤掉已爬取的URL"""
        try:
            logger.info("开始获取源URL数据...")
            
            # 获取已爬取的URL集合
            crawled_urls = set()
            cursor = self.log_collection.find({}, {"source_url": 1, "_id": 0})
            for doc in cursor:
                if doc.get("source_url"):
                    crawled_urls.add(doc["source_url"])
            
            logger.info(f"已爬取URL数量: {len(crawled_urls)}")
            
            # 获取所有源URL
            all_urls = list(self.source_collection.find({}).limit(10))  # 先只取10个测试
            logger.info(f"源集合总URL数量: {len(all_urls)}")
            
            # 过滤掉已爬取的URL
            filtered_urls = []
            for url_data in all_urls:
                if url_data.get("url") not in crawled_urls:
                    filtered_urls.append(url_data)
            
            logger.info(f"需要爬取的URL数量: {len(filtered_urls)}")
            return filtered_urls
            
        except Exception as e:
            logger.error(f"获取源URL数据失败: {str(e)}")
            return []

    async def crawl_page(self, url_data: Dict) -> Optional[Dict]:
        """爬取单个页面"""
        try:
            url = url_data['url']
            logger.info(f"开始爬取: {url}")
            
            # 访问页面
            await self.page.goto(url, wait_until='networkidle')
            await asyncio.sleep(random.uniform(*self.delay_range))
            
            # 获取页面信息
            page_data = {
                'source_url': url,
                'source_data': url_data,
                'crawl_time': datetime.now(),
                'page_title': await self.page.title(),
                'page_content_length': len(await self.page.content()),
            }
            
            logger.info(f"页面爬取成功: {url}")
            return page_data
            
        except Exception as e:
            logger.error(f"页面爬取失败 {url_data.get('url', 'unknown')}: {str(e)}")
            return None

    async def save_data(self, data: Dict, log_data: Dict) -> bool:
        """保存数据到MongoDB"""
        try:
            # 保存职位数据到目标集合
            job_result = self.target_collection.insert_one(data)
            logger.info(f"职位数据保存成功: {job_result.inserted_id}")
            
            # 保存日志到日志集合
            log_result = self.log_collection.insert_one(log_data)
            logger.info(f"日志保存成功: {log_result.inserted_id}")
            
            self.stats['success_count'] += 1
            return True
            
        except DuplicateKeyError:
            self.stats['duplicate_count'] += 1
            logger.info(f"数据重复，跳过: {data.get('source_url', 'unknown')}")
            return False
        except Exception as e:
            self.stats['error_count'] += 1
            logger.error(f"数据保存失败: {str(e)}")
            return False

    async def process_url(self, url_data: Dict) -> bool:
        """处理单个URL"""
        try:
            # 爬取页面
            page_data = await self.crawl_page(url_data)
            if not page_data:
                self.stats['error_count'] += 1
                return False
            
            # 准备日志数据
            log_data = {
                'source_url': url_data['url'],
                'source_data': url_data,
                'crawl_time': datetime.now(),
                'status': 'success',
                'job_count': 0
            }
            
            # 保存数据
            success = await self.save_data(page_data, log_data)
            return success
            
        except Exception as e:
            logger.error(f"处理URL失败 {url_data.get('url', 'unknown')}: {str(e)}")
            self.stats['error_count'] += 1
            return False

    async def run(self):
        """运行爬虫"""
        try:
            logger.info("开始运行前程无忧Step5爬虫（简化版本）")
            
            # 初始化浏览器
            await self.init_browser()
            
            # 获取源URL数据
            urls = await self.get_source_urls()
            if not urls:
                logger.warning("没有获取到需要爬取的URL数据")
                return
            
            # 处理每个URL
            for i, url_data in enumerate(urls, 1):
                try:
                    logger.info(f"处理进度: {i}/{len(urls)}")
                    
                    success = await self.process_url(url_data)
                    self.stats['total_processed'] += 1
                    
                    # 显示统计信息
                    if i % 5 == 0:
                        self.print_stats()
                    
                except Exception as e:
                    logger.error(f"处理URL时发生异常: {str(e)}")
                    self.stats['error_count'] += 1
                    continue
            
            # 最终统计
            self.print_stats()
            logger.info("爬虫运行完成")
            
        except Exception as e:
            logger.error(f"爬虫运行失败: {str(e)}")
        finally:
            await self.close_browser()

    def print_stats(self):
        """打印统计信息"""
        logger.info(f"统计信息: 总数={self.stats['total_processed']}, "
                   f"成功={self.stats['success_count']}, "
                   f"错误={self.stats['error_count']}, "
                   f"重复={self.stats['duplicate_count']}, "
                   f"封禁={self.stats['blocked_count']}")

async def main():
    """主函数"""
    spider = QCWYSpiderStep5Simple()
    await spider.run()

if __name__ == "__main__":
    asyncio.run(main()) 