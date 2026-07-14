#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
拉勾网爬虫 - 第二步：URL验证器

功能说明：
1. 验证第一步生成的URL是否可访问
2. 检查URL对应的职位列表页面是否有效
3. 记录URL的验证状态和结果

处理流程：
1. 从MongoDB加载需要验证的URL列表
2. 使用Selenium模拟浏览器访问每个URL
3. 解析页面内容，检查职位列表数据
4. 根据职位数量判断URL是否有效
5. 将验证结果保存到MongoDB

主要组件：
- MongoDB连接：存储URL和验证结果
- Selenium：模拟浏览器访问
- BeautifulSoup：解析页面内容
- 进度条：显示验证进度

数据存储：
- lagou_step1_urls_part2：待验证的URL集合
- lagou_step1_urls_202504_log_part2：验证结果记录集合

验证规则：
- 职位数量 > 5：标记为成功
- 职位数量 <= 5：标记为失败
- 访问异常：标记为失败

注意事项：
1. 每验证20个URL自动重启浏览器
2. 使用随机User-Agent避免被封
3. 支持断点续传（记录已验证的URL）
4. 异步处理提高效率
"""

import json
import logging
import os
import random
import time
from datetime import datetime
from typing import Dict, List
import urllib.parse
from bs4 import BeautifulSoup
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from tqdm import tqdm

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger("spiders.lagou_spider_validator")

class LagouSpiderStep2:
    """拉勾网URL验证器"""
    
    def __init__(self, headless: bool = True):
        # MongoDB配置
        self.mongo_uri = "mongodb://mooc_da:6WLg29gu3014i@210.14.140.50:10387/MOOC123_DA"
        self.mongo_db = "MOOC123_DA"
        self.url_collection_name = "lagou_step1_urls_202504_log_part2"  # 已经爬取URL记录集合
        self.lagou_urls_part = "lagou_step1_urls_part2"  # 需要爬取URL集合名称
        self.lagou_urls = None
        self.mongo_client = None
        self.db = None
        
        # URL缓存字典
        self.crawled_urls = {}
        
        # Selenium配置
        self.headless = headless
        self.driver = None
        self.wait = None

    async def init_db(self):
        """初始化数据库连接"""
        try:
            self.mongo_client = AsyncIOMotorClient(self.mongo_uri)
            self.db = self.mongo_client[self.mongo_db]
            self.lagou_urls = self.db[self.lagou_urls_part]
            
            # 创建索引
            await self.db[self.url_collection_name].create_index([
                ("job_type_code", ASCENDING),
                ("job_type_name", ASCENDING),
                ("industry_name", ASCENDING)
            ], unique=True)
            await self.db[self.url_collection_name].create_index([("crawl_time", ASCENDING)])
            
            # 加载已爬取的URL到缓存
            await self.load_crawled_urls()
            
            logger.info("MongoDB连接和索引初始化成功")
        except Exception as e:
            logger.error(f"MongoDB初始化失败: {e}")
            raise

    async def close_db(self):
        """关闭数据库连接"""
        if self.mongo_client:
            self.mongo_client.close()
            logger.info("MongoDB连接已关闭")

    async def is_url_crawled(self, job_type_code: str, job_type_name: str, industry: str) -> bool:
        """检查URL是否已经爬取过"""
        url_key = f"{job_type_code}-{job_type_name}-{industry}"
        return url_key in self.crawled_urls

    async def mark_url_crawled(self, url_doc: dict, status: str):
        """标记URL为已爬取"""
        try:
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            document = {
                "job_type_code": url_doc['job_type_code'],
                "job_type_name": url_doc['job_type_name'],
                "industry_name": url_doc['industry_name'],
                "crawl_time": current_time,
                "page": '15',
                "status": status,
                "update_time": current_time
            }
            
            url_collection = self.db[self.url_collection_name]
            result = await url_collection.update_one(
                {
                    "job_type_code": url_doc['job_type_code'],
                    "job_type_name": url_doc['job_type_name'],
                    "industry_name": url_doc['industry_name']
                },
                {
                    "$set": document,
                    "$setOnInsert": {"first_crawl_time": current_time}
                },
                upsert=True
            )
            
            if result.upserted_id:
                logger.info(f"新增URL记录: {url_doc['job_type_name']}-{url_doc['industry_name']}, 状态: {status}")
            else:
                logger.info(f"更新URL记录: {url_doc['job_type_name']}-{url_doc['industry_name']}, 状态: {status}")
            
        except Exception as e:
            logger.error(f"标记URL状态失败: {str(e)}")

    async def load_crawled_urls(self):
        """加载已爬取的URL到缓存"""
        try:
            url_collection = self.db[self.url_collection_name]
            cursor = url_collection.find({}, {"_id": 0})
            
            self.crawled_urls.clear()
            async for doc in cursor:
                self.crawled_urls[f"{doc.get('job_type_code', '')}-{doc.get('job_type_name', '')}-{doc.get('industry_name', '')}"] = 1
            
            logger.info(f"已加载 {len(self.crawled_urls)} 个已爬取的URL到缓存")
        except Exception as e:
            logger.error(f"加载已爬取URL失败: {str(e)}")
            self.crawled_urls = {}

    def init_selenium(self):
        """初始化Selenium"""
        try:
            chrome_options = Options()
            if self.headless:
                chrome_options.add_argument('--headless')
            
            chrome_options.add_argument('--window-size=1920,1080')
            chrome_options.add_argument('--start-maximized')
            chrome_options.add_argument('--lang=zh-CN')
            
            user_agents = [
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
            ]
            chrome_options.add_argument(f'user-agent={random.choice(user_agents)}')
            
            self.driver = webdriver.Chrome(options=chrome_options)
            self.wait = WebDriverWait(self.driver, 30)
            
            self.driver.set_page_load_timeout(30)
            self.driver.set_script_timeout(30)
            
            logger.info("Selenium初始化成功")
            
        except Exception as e:
            logger.error(f"Selenium初始化失败: {e}")
            raise

    def parse_job_list(self, html_content: str) -> List[Dict]:
        """解析职位列表页面"""
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            script_tag = soup.find('script', {'id': '__NEXT_DATA__'})
            
            if not script_tag:
                logger.error("未找到职位数据")
                return []
                
            data = json.loads(script_tag.string)
            position_result = data['props']['pageProps']['initData']['content']['positionResult']
            
            if not position_result:
                logger.error("未找到职位数据")
                return []
            
            position_list = position_result.get('result', [])
            logger.info(f"成功解析到 {len(position_list)} 个职位信息")
            return position_list
            
        except Exception as e:
            logger.error(f"解析职位列表失败: {e}")
            return []

    async def handle_page_navigation(self, url: str, max_retries: int = 3) -> bool:
        """处理页面导航"""
        for attempt in range(max_retries):
            try:
                self.driver.get(url)
                return True
                
            except Exception as e:
                logger.error(f"访问页面失败 (尝试 {attempt + 1}/{max_retries}): {str(e)}")
                if attempt < max_retries - 1:
                    time.sleep(random.uniform(2, 4))
                    continue
                return False
        
        return False

    async def run(self):
        """运行验证器"""
        try:
            await self.init_db()
            logger.info("数据库初始化完成")

            self.init_selenium()
            logger.info("Selenium初始化完成")

            all_docs = await self.lagou_urls.find().to_list(length=None)
            pending_docs = [
                doc for doc in all_docs
                if not await self.is_url_crawled(doc.get('job_type_code', ''), doc.get('job_type_name', ''), doc.get('industry_name', ''))
            ]
            total_pending = len(pending_docs)
            logger.info(f"实际需要验证 {total_pending} 个URL组合")
            pbar = tqdm(total=total_pending, desc="验证进度")

            url_counter = 0

            for url_doc in pending_docs:
                job_type_name = url_doc.get('job_type_name', '')
                industry = url_doc.get('industry_name', '')
                try:
                    logger.info(f"开始验证URL组合: {job_type_name} - {industry}")

                    job_type_code = url_doc.get('job_type_code', '')
                    url_counter += 1
                    
                    if url_counter > 0 and url_counter % 20 == 0:
                        logger.info("已验证20个URL，准备重启浏览器...")
                        self.driver.quit()
                        self.init_selenium()
                        logger.info("浏览器重启完成")

                    base_url = "https://www.lagou.com/wn/jobs"
                    page = 15
                    job_type_name_enc = job_type_name.replace("/", "%2F")
                    params = {
                        'pn': page,
                        'kd': job_type_name_enc,
                        'hy': industry,
                        'px': 'new',
                        'cl': 'false',
                        'fromSearch': 'true',
                        'labelWords': 'sug',
                    }
                    query_string = urllib.parse.urlencode(params, safe='=')
                    full_url = f"{base_url}?{query_string}"
                    logger.info(f"正在验证第{page}页: {full_url}")

                    if not await self.handle_page_navigation(full_url):
                        logger.error(f"无法访问页面: {full_url}")
                        pbar.set_postfix({"当前任务": f"{job_type_name}-{industry}", "状态": "失败"})
                        pbar.update(1)
                        continue

                    page_source = self.driver.page_source
                    job_list = self.parse_job_list(page_source)
                    
                    if len(job_list) > 5:
                        await self.mark_url_crawled(url_doc, 'success')
                        pbar.set_postfix({"当前任务": f"{job_type_name}-{industry}", "状态": "成功", "职位数": len(job_list)})
                    else:
                        await self.mark_url_crawled(url_doc, 'fail')
                        pbar.set_postfix({"当前任务": f"{job_type_name}-{industry}", "状态": "无数据"})
                    pbar.update(1)
                    
                except Exception as e:
                    logger.error(f"验证页面失败: {str(e)}")
                    pbar.set_postfix({"当前任务": f"{job_type_name}-{industry}", "状态": "异常"})
                    pbar.update(1)
                    continue

            pbar.close()

        except Exception as e:
            logger.error(f"验证器运行出错: {e}")
            raise
        finally:
            if hasattr(self, 'driver'):
                self.driver.quit()
            await self.close_db()
            logger.info("验证器运行结束，资源已清理")

async def main():
    """主函数"""
    try:
        spider = LagouSpiderStep2(headless=True)
        await spider.run()
        
    except Exception as e:
        logger.error(f"程序运行出错: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
    finally:
        try:
            await spider.close_db()
        except Exception as e:
            logger.error(f"清理资源时出错: {str(e)}")

if __name__ == "__main__":
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("程序被用户中断")
    except Exception as e:
        logger.error(f"程序异常退出: {str(e)}")
        import traceback
        logger.error(traceback.format_exc()) 